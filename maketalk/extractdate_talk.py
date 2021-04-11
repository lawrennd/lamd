#!/usr/bin/env python3

import sys
import ndlpy.talk as nt

def main(args=None):
    filename = args[0]
    fields = nt.header_fields(filename)
    print(fields['date'])

if __name__ == "__main__":
    main(sys.argv[1:])

    
