#!/usr/bin/env python3
"""Copy the entry image to the output directory.

The entry is a program that writes one image of the day's news to
/output/entry.png. The image itself (entry.png, beside this file) is
the rendered front page for Monday 23 November 2026; this program
simply copies it to the output directory the grader provides.
Standard library only, no network, deterministic.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    os.chmod(dst, 0o644)
    with open(dst, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    print("entry.png sha256=%s" % digest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
