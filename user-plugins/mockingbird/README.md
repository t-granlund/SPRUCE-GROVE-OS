# Mockingbird plugin

Voice prompts for Spruce Grove OS — the "stop dictating into iOS Voice Memos
and shuttling files around" feature. Recorded at Bentonville Fire Department
Station 4, transcribed there too.

## What it does

```
/rec        (alias /r)
```

1. Opens a live **recording window** (elapsed time, size, take count).
2. Keys: `p` pause/resume · `s` stop & transcribe · `q` cancel (each + Enter).
3. Transcribes locally with the Mockingbird rig (ffmpeg -> whisper-cli ->
   `whisper-large-v3-turbo-q5_0` from `~/dev/mockingbird/models/`).
4. Review loop: **[s]end** the transcript as your prompt, **[e]dit** it in
   `$VISUAL`/`$EDITOR`, **[r]e-record** — the previous transcript stays pinned
   in the window so you can record *against* your draft — or **[q]uit**.
5. Sending returns a `CustomCommandResult`, so the transcript becomes the
   user prompt and is applied against the current working directory.

Everything (segments, master.wav, transcript.txt, your edits) is kept under
`~/.spruce_grove/mockingbird/<timestamp>/` (last 20 sessions).

## Requirements

- macOS (capture uses ffmpeg's avfoundation mic backend)
- `ffmpeg` — `brew install ffmpeg`
- `whisper-cli` — `brew install whisper-cpp`
- A whisper ggml model — Mockingbird's `scripts/download-models.sh` puts the
  turbo q5_0 in `~/dev/mockingbird/models/`
- macOS microphone permission for your terminal app

## Configuration (optional env vars)

| Variable | Meaning |
|----------|---------|
| `SPRUCE_MOCKINGBIRD_MODEL` | Path to a whisper-cpp ggml model |
| `SPRUCE_MOCKINGBIRD_WHISPER` | Path to the whisper-cli binary |
| `SPRUCE_MOCKINGBIRD_MIC` | Mic name substring (e.g. "Shure") or avfoundation index |
| `SPRUCE_MOCKINGBIRD_LANG` | Language hint for whisper (e.g. `en`) |

## Notes

- Keys need Enter because the window deliberately uses *line* input — the
  core app allows exactly one cbreak stdin listener and this plugin is not it.
- Upstream-ready: structured exactly like a `code_puppy_core_plugins` builtin
  (thin `register_callbacks.py` + sibling modules), so it can graduate to the
  official plugin pack unchanged.
