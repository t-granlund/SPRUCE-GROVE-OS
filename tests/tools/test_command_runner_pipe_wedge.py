"""Regression tests for the detached-grandchild pipe-inheritance wedge.

An agent command like ``start /B python -m http.server ... && timeout /t 1``
leaves a grandchild that outlives cmd.exe *and* inherits the runner's
stdout/stderr pipe write-handles (CreateProcess with bInheritHandles=TRUE
copies every inheritable handle, including the ones cmd no longer uses as
its std handles). EOF therefore never arrives:

1. the reader thread wedged in the post-exit "final drain" ``read()``;
2. ``process.stdout.close()`` from the executor thread then deadlocked on
   the io buffer lock held by that wedged read — the shell tool call never
   returned;
3. the Ctrl+C sweep (``kill_all_running_shell_processes``) ran the same
   ``close()`` on the key-listener thread, wedging IT before
   ``agent_task.cancel`` could be scheduled — the app froze in
   "cancelling" forever while the spinner kept animating.

These tests pin the three layers of the fix: EOF-independent drain,
lock-safe pipe closes, and a never-blocking cancel sweep.
"""

import io
import os
import subprocess
import sys
import threading
import time
from types import SimpleNamespace

import pytest

from spruce_grove.tools import command_runner
from spruce_grove.tools.command_runner import (
    _close_pipes_best_effort,
    _close_process_pipes,
    _drain_available,
    run_shell_command_streaming,
)


class _OnceBuffer:
    """read1 returns a payload once; a second call would hang forever."""

    def __init__(self, payload: bytes):
        self.payload = payload
        self.calls = 0

    def read1(self, size=-1):
        self.calls += 1
        return self.payload


class _OnceStream:
    def __init__(self, payload: bytes):
        self.buffer = _OnceBuffer(payload)


def test_drain_available_never_waits_for_eof():
    """Data present + write-end never closing must still return immediately."""
    lines = []
    stream = _OnceStream(b"gamma\ndelta")
    # has_data flips to False after the single read — EOF never came.
    _drain_available(stream, lines.append, _has_data=lambda s: s.buffer.calls == 0)
    assert lines == ["gamma", "delta"]
    assert stream.buffer.calls == 1


def test_drain_available_flushes_partial_trailing_line():
    """Complete lines sink as they arrive; a trailing partial line flushes
    as-is instead of being waited for."""
    lines = []
    data = b"alpha\nbeta\r\npart"
    stream = SimpleNamespace(buffer=io.BytesIO(data))
    total = len(data)
    _drain_available(stream, lines.append, _has_data=lambda s: s.buffer.tell() < total)
    assert lines == ["alpha", "beta", "part"]


class _Raw:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True


class _Buffered:
    def __init__(self):
        self.raw = _Raw()


class _WrappedStream:
    """Mimics TextIOWrapper(BufferedReader(FileIO)) close surface."""

    def __init__(self):
        self.buffer = _Buffered()
        self.raw = self.buffer.raw
        self.closed = False

    def close(self):
        self.closed = True


def test_close_process_pipes_falls_back_to_raw_when_reader_wedged():
    """A live reader thread holding the io lock must not deadlock close:
    only the raw handles get closed, the wrapper is left alone."""
    wedged = threading.Thread(target=time.sleep, args=(30,), daemon=True)
    wedged.start()
    proc = SimpleNamespace(stdout=_WrappedStream(), stderr=_WrappedStream(), stdin=None)
    _close_process_pipes(proc, wedged)
    assert proc.stdout.buffer.raw.closed is True
    assert proc.stderr.buffer.raw.closed is True
    # Wrapper close was skipped — calling it would block on the io lock.
    assert proc.stdout.closed is False

    # Readers finished -> normal wrapped close.
    done = threading.Thread(target=lambda: None)
    done.start()
    done.join()
    proc2 = SimpleNamespace(stdout=_WrappedStream(), stderr=None, stdin=None)
    _close_process_pipes(proc2, done)
    assert proc2.stdout.closed is True


def test_close_pipes_best_effort_returns_while_reader_holds_lock():
    """The cancel sweep runs on the key-listener thread: closing pipes must
    be bounded even when a reader is wedged mid-read on the io lock."""
    r, w = os.pipe()
    reader = io.open(r, "rb", closefd=True)
    holder = threading.Thread(target=reader.read, daemon=True)
    holder.start()
    time.sleep(0.2)  # let the holder acquire the buffer lock inside read()

    proc = SimpleNamespace(stdout=reader, stderr=None, stdin=None)
    start = time.monotonic()
    _close_pipes_best_effort(proc, timeout=0.25)
    elapsed = time.monotonic() - start
    assert elapsed < 2.0, "pipe close blocked the calling thread"

    # Release the holder: EOF arrives, the daemon closer finishes.
    os.close(w)
    holder.join(timeout=2)
    assert not holder.is_alive()


@pytest.mark.skipif(
    not sys.platform.startswith("win"),
    reason="Windows pipe-handle inheritance wedge (start /B grandchild)",
)
def test_streaming_survives_detached_grandchild_pipe_inheritance():
    """The incident, end to end.

    cmd.exe exits in ~1s (``timeout /t`` fails under redirected stdin) but
    the ``start /B`` grandchild sleeps 10s while holding the pipe
    write-ends. Streaming must return WITHOUT waiting for that EOF; before
    the fix this deadlocked in process.stdout.close() forever.
    """
    python = sys.executable
    # Note the empty title arg: start treats the first quoted token as the
    # window title, so the executable must come second.
    cmd = (
        f'start /B "" "{python}" -c "import time; time.sleep(10)" > nul 2>&1 '
        "&& timeout /t 1 /nobreak > nul"
    )
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
        | subprocess.CREATE_NO_WINDOW,  # type: ignore[attr-defined],
    )
    # Mirror _run_command_sync: the streaming reader works on wrapped
    # text streams (raw bytes would crash _truncate_line with TypeError).
    process.stdout = io.TextIOWrapper(
        process.stdout, newline="", encoding="utf-8", errors="replace"
    )
    process.stderr = io.TextIOWrapper(
        process.stderr, newline="", encoding="utf-8", errors="replace"
    )
    command_runner._register_process(process)
    outcome = {}

    def _run():
        outcome["result"] = run_shell_command_streaming(
            process, timeout=10, command=cmd, silent=True
        )

    worker = threading.Thread(target=_run, daemon=True)
    start = time.monotonic()
    worker.start()
    # 20s bound: pre-fix this never returns (deadlock), so the test FAILS
    # loudly instead of hanging the suite. Post-fix it lands in ~2-4s —
    # well before the grandchild's 10s sleep ends, proving no EOF wait.
    worker.join(timeout=20)
    elapsed = time.monotonic() - start
    try:
        assert not worker.is_alive(), (
            "streaming wedged on detached-grandchild pipe inheritance "
            "(EOF never arrived and close() deadlocked)"
        )
        result = outcome.get("result")
        assert result is not None
        assert elapsed < 9.0, (
            f"streaming took {elapsed:.1f}s — it waited for the grandchild "
            "(EOF) instead of draining and moving on"
        )
        assert process.poll() is not None
        # timeout.exe's complaint came through the pipes before cmd died.
        assert "Input redirection is not supported" in (result.stderr or "")
    finally:
        command_runner._unregister_process(process)
