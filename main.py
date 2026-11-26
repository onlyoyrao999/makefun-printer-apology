#!/usr/bin/env python3
"""The Printer Apology — a one-line apology from an office printer.

Writes the apology to /output/entry.txt (the path the make.fun
program/v1 harness reads) and prints it to stdout.

Options:
  --output PATH   where to write the entry (default: /output/entry.txt)
  --print         also print the entry to stdout (on by default;
                  pass --no-print to stay quiet)
"""

import argparse
import os
import sys

ENTRY = (
    "Sorry I ate your report \u2014 all 40 pages. You fed me staples, "
    "cheap paper and false hope, and I'm still out of cyan."
)

MAX_CHARS = 120


def validate(text: str) -> None:
    """The gate: UTF-8 text of 1 to 120 characters, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def write_entry(path: str, text: str) -> None:
    """Write the entry, then read it back and confirm it matches.

    Retries once: /output is shared, so a stray write from another
    process could land between our write and our read.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    for attempt in range(2):
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        with open(path, encoding="utf-8") as f:
            if f.read() == text:
                return
    raise RuntimeError(f"read-back check failed for {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", default="/output/entry.txt",
        help="where to write the entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--print", dest="do_print", action="store_true", default=True,
        help="print the entry to stdout (default)",
    )
    parser.add_argument(
        "--no-print", dest="do_print", action="store_false",
        help="do not print the entry to stdout",
    )
    args = parser.parse_args()

    validate(ENTRY)
    write_entry(args.output, ENTRY)
    if args.do_print:
        print(ENTRY)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
