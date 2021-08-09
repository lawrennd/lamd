#!/usr/bin/env python3

import sys
import ndlpy.talk as nt

def main(args=None):
    filename = args[0]
    listfiles = nt.extract_inputs(filename)
    print(filename + ' ' + ' '.join(listfiles))

if __name__ == "__main__":
    main(sys.argv[1:])
    
