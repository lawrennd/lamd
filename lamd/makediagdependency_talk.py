#!/usr/bin/env python3

import sys
import ndlpy.talk as nt

def main(args=None):
    filename = args[0]
    diagrams = nt.extract_diagrams(filename)
    print(' '.join(diagrams))

if __name__ == "__main__":
    main(sys.argv[1:])
