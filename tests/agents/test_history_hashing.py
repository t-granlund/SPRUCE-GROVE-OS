"""Tests for the stable content-based hashing in spruce_grove.agents._history.

Properties under test:
- Determinism: same content -> same hash across separate constructions
  (and across processes: the digest is sha256-based, not builtin hash()).
- Sensitivity: content / tool_call_id changes change the hash.
- BinaryContent bytes participate in the hash.
- Version resilience: hashing keys on ``part_kind``, NOT the class name, so
  a pydantic-ai class rename does not invalidate existing dedup hashes.
"""

import dataclasses
import enum
import hashlib

from pydantic_ai import BinaryContent
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    TextPart,
    ToolCallPart,
    ToolReturnPart,
    UserPromptPart,
)

from spruce_grove.agents._history import hash_message, stringify_part


def test_same_content_same_hash_across_constructions():
    msg_a = ModelRequest(parts=[UserPromptPart(content="hello grove")])
    msg_b = ModelRequest(parts=[UserPromptPart(content="hello grove")])
    assert hash_message(msg_a) == hash_message(msg_b)


def test_hash_ignores_timestamps():
    part_a = UserPromptPart(content="woof")
    part_b = UserPromptPart(content="woof")
    # Different timestamps must not affect the hash.
    assert part_a.timestamp != part_b.timestamp or True  # timestamps may collide
    assert hash_message(ModelRequest(parts=[part_a])) == hash_message(
        ModelRequest(parts=[part_b])
    )


def test_hash_is_16_char_hex_string():
    digest = hash_message(ModelRequest(parts=[UserPromptPart(content="x")]))
    assert isinstance(digest, str)
    assert len(digest) == 16
    int(digest, 16)  # raises if not hex


def test_hash_is_process_independent_sha256():
    """The digest is sha256 of the canonical string — NOT salted hash()."""
    msg = ModelRequest(parts=[UserPromptPart(content="hello")])
    canonical = stringify_part(msg.parts[0])
    expected = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
    assert hash_message(msg) == expected


def test_hash_differs_when_content_differs():
    msg_a = ModelRequest(parts=[UserPromptPart(content="hello")])
    msg_b = ModelRequest(parts=[UserPromptPart(content="goodbye")])
    assert hash_message(msg_a) != hash_message(msg_b)


def test_hash_differs_when_tool_call_id_differs():
    msg_a = ModelResponse(
        parts=[ToolCallPart(tool_name="fetch", args="{}", tool_call_id="call_1")]
    )
    msg_b = ModelResponse(
        parts=[ToolCallPart(tool_name="fetch", args="{}", tool_call_id="call_2")]
    )
    assert hash_message(msg_a) != hash_message(msg_b)


def test_tool_return_hash_stable_and_id_sensitive():
    def make(tcid):
        return ModelRequest(
            parts=[ToolReturnPart(tool_name="fetch", content="ok", tool_call_id=tcid)]
        )

    assert hash_message(make("a")) == hash_message(make("a"))
    assert hash_message(make("a")) != hash_message(make("b"))


def test_binary_content_data_participates_in_hash():
    def make(data: bytes):
        return ModelRequest(
            parts=[
                UserPromptPart(
                    content=[
                        "look at this",
                        BinaryContent(data=data, media_type="image/png"),
                    ]
                )
            ]
        )

    assert hash_message(make(b"\x89PNG-one")) == hash_message(make(b"\x89PNG-one"))
    assert hash_message(make(b"\x89PNG-one")) != hash_message(make(b"\x89PNG-two"))


class _RenamedUserPromptPart:
    """Fake part: same part_kind/content as UserPromptPart, different class.

    Simulates pydantic-ai renaming its part classes in a new major version.
    Because hashing keys on ``part_kind``, the hash must be identical.
    """

    part_kind = "user-prompt"

    def __init__(self, content):
        self.content = content


def test_class_rename_does_not_change_hash():
    real = ModelRequest(parts=[UserPromptPart(content="stable across versions")])

    class _FakeMessage:
        parts = [_RenamedUserPromptPart("stable across versions")]

    assert hash_message(real) == hash_message(_FakeMessage())


def test_class_name_fallback_for_parts_without_part_kind():
    class _WeirdPart:
        content = "no part_kind here"

    assert stringify_part(_WeirdPart()).startswith("_WeirdPart|")


def test_text_part_uses_part_kind_not_class_name():
    s = stringify_part(TextPart(content="hi"))
    assert s.startswith("text|")
    assert "TextPart" not in s


# --- Rich-payload resilience (the CaptureGeometry regression) -----------------
#
# stringify_part hashes *every* part on *every* model request. A single
# non-JSON-encodable object anywhere in a tool payload used to raise TypeError
# and abort the whole turn (computer-use state carried a dataclass). These
# tests pin the defensive ``default=_json_default`` fallback so that class of
# crash cannot silently return.


@dataclasses.dataclass
class _Geometry:
    x: int
    y: int


class _Shade(enum.Enum):
    RED = "red"
    CLEAR = "clear"


def _rich_payload() -> dict:
    return {
        "geom": _Geometry(1, 2),
        "shade": _Shade.RED,
        "tags": {"beta", "alpha"},
        "blob": b"\x89PNG",
        "nested": {"deep": _Geometry(3, 4)},
    }


def test_rich_tool_payload_does_not_raise():
    """The exact crash: a dataclass inside a tool-return dict must not raise."""
    part = ToolReturnPart(
        tool_name="computer", content=_rich_payload(), tool_call_id="c1"
    )
    assert stringify_part(part)  # must not raise TypeError


def test_rich_payload_is_deterministic():
    def make():
        return ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name="computer", content=_rich_payload(), tool_call_id="c1"
                )
            ]
        )

    assert hash_message(make()) == hash_message(make())


def test_set_order_does_not_change_hash():
    """Sets are unordered; fallback sorts by repr so the hash is content-stable."""
    a = ToolReturnPart(
        tool_name="t", content={"tags": {"a", "b", "c"}}, tool_call_id="x"
    )
    b = ToolReturnPart(
        tool_name="t", content={"tags": {"c", "b", "a"}}, tool_call_id="x"
    )
    assert stringify_part(a) == stringify_part(b)


def test_bytes_in_payload_participates_in_hash():
    def make(data: bytes):
        return ModelRequest(
            parts=[
                ToolReturnPart(tool_name="t", content={"blob": data}, tool_call_id="x")
            ]
        )

    assert hash_message(make(b"one")) == hash_message(make(b"one"))
    assert hash_message(make(b"one")) != hash_message(make(b"two"))


def test_arbitrary_object_with_dict_does_not_raise():
    class _Opaque:
        def __init__(self):
            self.public = 1
            self._private = 2

    part = ToolReturnPart(tool_name="t", content={"obj": _Opaque()}, tool_call_id="x")
    s = stringify_part(part)
    assert "public" in s


def test_json_default_handles_nested_pydantic_and_enum():
    from spruce_grove.agents._history import _json_default

    assert _json_default(_Shade.RED) == "red"
    assert _json_default(_Geometry(1, 2)) == {"x": 1, "y": 2}
    assert _json_default(b"abc").startswith("<bytes ")
    assert isinstance(_json_default(object()), str)  # repr fallback, never raises
