#!/usr/bin/env python3

import sys
import os
import ndlpy.talk as nt
import ndlpy.yaml as ny


def main():
    field = sys.argv[1]
    filename = sys.argv[2]

    try:
        answer = nt.talk_field(field, filename)
    except ny.FileFormatError:
        if field in ny.defaults:
            answer= ny.defaults[field]
        else:
            answer = ''

    if field=='categories':
        print("['" + "', '".join(answer) + "']")
    else:
        print(answer)
            

if __name__ == "__main__":
    sys.exit(main())
