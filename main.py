"""One Emoji, One Smile -- make.fun entry (program/v1).

Writes exactly one emoji to $MAKEFUN_OUTPUT_DIR/entry.txt: the hugging
face, chosen for the warmth judge's brief (warm at first glance,
universal, picked rather than the default smiley, right from a stranger).

Deterministic: no randomness, no network, no time, no environment input
beyond the output directory. Stdlib only.
"""

import os
import sys

# The entry: U+1F917 HUGGING FACE -- one character, four UTF-8 bytes.
EMOJI = "\U0001F917"

# Gate from the competition rules: /output/entry.txt must be UTF-8 text
# of 1 to 8 characters, not only white space.
MIN_CHARS = 1
MAX_CHARS = 8


def resolve_output_dir():
    """Output directory: $MAKEFUN_OUTPUT_DIR, else ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def validate(text):
    """Enforce the competition gate on the exact text to be written."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if text.strip() == "":
        raise ValueError("entry must not be only white space")
    if len(text) != 1:
        raise ValueError("entry must be exactly one emoji, got %d chars" % len(text))
    # Exactly one emoji, not a letter, digit or punctuation mark: the
    # single code point must sit outside the ASCII range, so a plain
    # smiley typed as text (":)") or a word can never slip through.
    code_point = ord(text)
    if code_point < 0x80:
        raise ValueError("entry must be a non-ASCII emoji character")
    if text in ("\ufe0f", "\u200d"):
        raise ValueError("entry must not be a bare modifier character")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable text
    return text


def main():
    validate(EMOJI)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(EMOJI)
    # Re-read and re-validate what was actually written, at byte level:
    # the file must hold exactly the emoji's UTF-8 bytes, nothing else
    # (no trailing newline, no BOM, no extra character).
    with open(path, "rb") as f:
        raw = f.read()
    if raw != EMOJI.encode("utf-8"):
        raise ValueError(
            "written bytes %r do not match the chosen emoji" % raw
        )
    written = raw.decode("utf-8")
    validate(written)
    if written != EMOJI:
        raise ValueError("written entry does not match the chosen emoji")
    print("entry.txt: %s (%d char, %d bytes)" % (written, len(written), len(raw)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
