#!/usr/bin/env python3
"""Entry point for news-image-20261120 (Python 3.13, standard library only).

Copies the repository's pre-built front page (entry.png) to the output
directory the harness provides. No network, no randomness: every run
writes the exact same bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    sys.exit(main())
