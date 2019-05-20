import sys
import re

import func
import header_parser
import description_parser

def parse(header, description):
    if type(header) is str:
        return {**header_parser.parse_header(header),
            **description_parser.parse_description(description)}
    if (func.verbose):
        print(header_parser.cleanHeader(header.text))
    return {**header_parser.parse_header(header.text),
        **description_parser.parse_description(description.text)}

def checkCommandLineArguments():
    if (len(sys.argv) != 3):
        func.printError("Use: python3" + sys.argv[0] + " [class_header] [class_description]")
        exit()

# if __name__ == '__main__':
#
#     # Check command line arguments
#     checkCommandLineArguments()
#
#     # Take command line arguments into string form
#     class_header = sys.argv[1]
#     class_desc = sys.argv[2]
#     class_dict = parse(class_header, class_desc)
#
#     # Final output
#     functionality.outputInformation(class_dict)
