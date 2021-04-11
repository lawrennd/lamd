#!/usr/bin/env python3

import sys
import os
import ndlpy.talk as nt


def main(args=None):
    field = args[0]
    filename = args[1]


    try:
        answer = nt.talk_field(field, filename)
    except nt.FileFormatError:
        if field in defaults:
            answer= defaults[field]
        else:
            answer = ''

    if field=='categories':
        print("['" + "', '".join(answer) + "']")
    else:
        print(answer)
            

if __name__ == "__main__":
    main(sys.argv[1:])
