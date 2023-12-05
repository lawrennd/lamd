#!/usr/bin/env python3

import sys
import os
import ndlpy.talk as nt
import ndlpy.yaml as ny
from ndlpy.settings import Settings


def main():
    field = sys.argv[1]
    filename = sys.argv[2]

    try:
        answer = nt.talk_field(field, filename)
    except ny.FileFormatError:
        settings = Settings(user_file=["_lamd.yml", "_config.yml"], directory=".")
        if field in settings:
            answer = settings[field]
        else:
            answer = ''
    if type(answer) is str:
        answer = os.path.expandvars(answer)
    if field=='categories':
        print("['" + "', '".join(answer) + "']")
    else:
        print(answer)
            

if __name__ == "__main__":
    sys.exit(main())
