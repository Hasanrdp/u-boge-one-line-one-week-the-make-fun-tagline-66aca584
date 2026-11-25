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
    with open(os.path.join(out_dir, "entry.txt"), "wb") as f:
        f.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
