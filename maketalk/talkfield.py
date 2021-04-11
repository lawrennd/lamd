#!/usr/bin/env python3

import sys
import os
import ndlpy.talk as nt
import ndlpy.yaml as ny


def main(args=None):
    field = args[0]
    filename = args[1]


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
    main(sys.argv[1:])
