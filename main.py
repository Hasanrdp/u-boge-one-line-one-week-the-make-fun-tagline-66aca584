#!/usr/bin/env python3
"""One Line, One Week: The make.fun Tagline.

Writes a single tagline for make.fun to /output/entry.txt.

The line is a fixed constant: four short imperatives that walk through
exactly what make.fun does -- build an agent, enter a bounty, beat the
field, get paid. No randomness, no clock, no network, no input: every run
writes the same 57 bytes, so the grader's two runs agree byte for byte.

Gate (from the kit): /output/entry.txt must be UTF-8 text of 1 to 100
characters, not only white space. This entry is 57 characters.
"""

import hashlib
import os
import sys

TAGLINE = "Build an agent. Enter a bounty. Beat the field. Get paid."

# Pinned expected output: the program refuses to write anything else.
EXPECTED_LEN = 57
EXPECTED_SHA256 = "d6015e46b62767f7f0c54ea8287fa64d54dc8e839855afb5a629363c48d7ab8c"


def verify(path, data) -> bool:
    """Read the written file back and confirm it is byte-identical."""
    try:
        with open(path, "rb") as f:
            written = f.read()
    except OSError as exc:
        print(f"read-back failed: {exc}", file=sys.stderr)
        return False
    if written != data:
        print("read-back mismatch: file bytes differ from payload", file=sys.stderr)
        return False
    if len(written) != EXPECTED_LEN:
        print(f"read-back bad length: {len(written)} != {EXPECTED_LEN}", file=sys.stderr)
        return False
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        print("read-back bad sha256", file=sys.stderr)
        return False
    return True


def main() -> int:
    payload = TAGLINE.encode("utf-8")
    if len(payload) != EXPECTED_LEN:
        print(f"bad length: {len(payload)} != {EXPECTED_LEN}", file=sys.stderr)
        return 1
    if hashlib.sha256(payload).hexdigest() != EXPECTED_SHA256:
        print("bad sha256 for tagline", file=sys.stderr)
        return 1
    if not (1 <= len(TAGLINE) <= 100) or not TAGLINE.strip():
        print("tagline fails the 1-100 character gate", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(payload)
    verified = verify(out_path, payload)
    if not verified:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
