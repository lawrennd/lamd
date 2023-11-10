#!/usr/bin/env python3

import sys
import os
import ndlpy.talk as nt
import ndlpy.yaml as ny
import ndlpy.config as cf


def main():
    field = sys.argv[1]
    filename = sys.argv[2]

    try:
        answer = nt.talk_field(field, filename)
    except ny.FileFormatError:
        config = cf.load_config(user_file=["_lamd.yml", "_config.yml"], directory=".")
        if field in config:
            answer= config[field]
        else:
            answer = ''

    answer = os.path.expandvars(answer)
    if field=='categories':
        print("['" + "', '".join(answer) + "']")
    else:
        print(answer)
            

if __name__ == "__main__":
    sys.exit(main())
