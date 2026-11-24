#!/usr/bin/env python3
"""Loading Screen Gold: A Tip in 200 Characters — make.fun entry.

Writes one loading-screen tip (a single line, at most 200 characters)
to /output/entry.txt.

The tip is aimed at stressed developers AND the AI coding agents
working beside them, mid-build:

    Loading… Your agent renamed 'final_v2_REAL' 6 times.
    It is now called 'Kevin'. Do not rename Kevin.

Why it works: a specific number (6 renames), a named thing (Kevin),
and a concrete artifact punchline (the file 'final_v2_REAL' — the
"final" file every tired developer recognises). The developer and the
agent are both in the joke at once: the agent did the renaming, the
developer is the one told not to touch Kevin.
"""

import argparse
import os
import sys

ENTRY = "Loading\u2026 Your agent renamed 'final_v2_REAL' 6 times. It is now called 'Kevin'. Do not rename Kevin."

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate_entry(text):
    """Check the entry against the sealed-gate rules.

    Returns a list of problems; empty means the entry is valid.
    Rules: UTF-8 text, exactly one line, 1-200 characters,
    not only whitespace.
    """
    problems = []
    if not isinstance(text, str):
        return ["entry is not text"]
    if text != text.strip():
        # A trailing newline in the file is fine; the entry itself
        # must not carry leading/trailing whitespace.
        pass
    stripped = text.strip()
    if not stripped:
        problems.append("entry is empty or only whitespace")
    if len(text) != len(stripped):
        problems.append("entry has leading/trailing whitespace")
    if "\n" in stripped or "\r" in stripped:
        problems.append("entry must be exactly one line")
    if len(stripped) < 1 or len(stripped) > MAX_CHARS:
        problems.append(
            "entry is %d characters; must be 1-%d" % (len(stripped), MAX_CHARS)
        )
    try:
        stripped.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Validate the entry and print PASS/FAIL with the character count.",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_PATH,
        help="Where to write the entry (default: %(default)s).",
    )
    args = parser.parse_args()

    if args.self_test:
        problems = validate_entry(ENTRY)
        print("entry: %s" % ENTRY)
        print("characters: %d" % len(ENTRY))
        print("lines: %d" % (ENTRY.count("\n") + 1))
        if problems:
            print("FAIL: " + "; ".join(problems))
            return 1
        print("PASS")
        return 0

    problems = validate_entry(ENTRY)
    if problems:
        print("FAIL: " + "; ".join(problems), file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")

    print("wrote %s (%d characters)" % (args.output, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
