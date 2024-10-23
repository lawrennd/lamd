#!/usr/bin/env python3

import sys
import os
import lynguine.util.talk as nt
import lynguine.util.yaml as ny

from lamd.config.interface import Interface

def main():
    field = sys.argv[1]
    filename = sys.argv[2]

    try:
        answer = nt.talk_field(field, filename, user_file=["_lamd.yml", "_config.yml"])
    except ny.FileFormatError:
        iface = Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
        if field in iface:
            answer = iface[field]
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
