import sys
import re
import class_parser

if __name__ == '__main__':
    print("OUTPUT")
    print(repr(class_parser.cleanHeader(sys.argv[1])))
