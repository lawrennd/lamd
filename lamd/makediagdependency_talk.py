#!/usr/bin/env python3

import sys
from typing import List

import lynguine.talk as nt


def main(args: List[str]) -> None:
    if not args:
        raise ValueError("Filename argument is required")
    filename = args[0]
    diagrams = nt.extract_diagrams(filename)
    print(" ".join(diagrams))


if __name__ == "__main__":
    main(sys.argv[1:])
