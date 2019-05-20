import sys
import re
import func
import time


def condense_header_intro(sub_header):
    # Validate the min. length
    if (len(sub_header) < 2):
        return []

    # Combine into two parts

    part1 = sub_header[0]
    index = 1
    while ( index < len(sub_header) - 1 ):
        part1 += ' ' + sub_header[index]
        index += 1

    part2 = sub_header[index]

    return [ part1, part2 ]

# [department_id] [number]
def parse_part_one(header):
    dict = {}
    headers = condense_header_intro(re.split(" ", header))

    # Error checking
    if (len(headers) != 2):
        func.printError("Split header part one has " + str(len(headers)) + " elements rather than the expected 2. Exiting.")
        print("Header:",header)
        print("Split:", headers)
        exit()

    # Get the department id and number from the split
    dict['department_id'] = headers[0]
    dict['number'] = headers[1]
    return dict


header_delimeters = { " (", ")" }
headerRegex = '|'.join(map(re.escape, header_delimeters))

def parse_units(str):
    if "–" in str or "-" in str or " to " in str:
        return [ str ]

    if "S" in str or "W" in str or "F" in str:
        return []

    return re.split("\, or|\, | or |/", str)

def validate_units(units):
    if len(units) == 1 and ("–" in units[0] or "-" in units[0] or " to " in units[0]):
        return True

    for number in units:
        try:
            s = float(number)
        except ValueError:
            return False
    return True

# [name] [units]
def parse_part_two(header):
    #SEPS = ("\ \(", "\)")
    #rsplit = re.compile("|".join(SEPS)).split
    #headers = rsplit(header)
    headers = re.split("\ \(|\)", header)
    headers = headers[:-1]
    if (len(headers) == 0):        # Hardcode in edge case
        headers = [ header ]
    dict = {}

    if (len(headers) == 0):
        func.printError("Expected at least one part in part two of header, only got " + str(len(headers)) + ". Exiting.")
        print("Part Two:", header)
        print("Split:", headers)
        exit()
    elif (len(headers) == 1):
        dict['name'] = headers[0]
        return dict

    # At this point, we have at least two elements

    index = 1
    name = headers[0]
    useParen = True
    # Gather the class name with parenthesis as everything up until the last element
    while (index < len(headers) - 1):
        if (useParen):
            name += " (" + headers[index] + ")"
            useParen = False
        else:
            name += " " + headers[index]
            useParen = True
        index += 1

    # If the last element is units, add it to units, otherwise add it as part of the title
    units = parse_units(headers[index])
    if (len(units) > 0):
        if (not validate_units(units)):
            func.printError("Units were not valid. Exiting.")
            print("Units List:", units)
            exit()
    else:
        if (useParen):
            name += "(" + headers[index] + ")"
            useParen = False
        else:
            name += headers[index]
            useParen = True
    dict['units'] = units
    dict['name'] = name
    return dict

def cleanHeader(s):
    new_string = s

    # Checks for edge case of having ':' instead of '.' to sep. header
    if ':' in new_string and '.' not in new_string:
        new_string = new_string.replace(':', '.')

    # remove tabs
    new_string = new_string.replace('\t', '')

    # remove new lines (and all spaces after)
    pattern = re.compile('\n(\s | \t)*')
    new_string = re.sub(pattern, ' ', new_string)

    # remove all double or more lines
    pattern = re.compile('\s\s+')
    new_string = re.sub(pattern, ' ', new_string)

    # remove these weird \xa0 characters
    new_string = new_string.replace('\xa0', ' ')
    return new_string

# [part1]. [part2]
def split_header(header):
    split = header.split('.', 1)

    # Check if the second portion begins with a ' '
    if (len(split) < 2 or len(split[1]) == 0):
        func.printError("Was not able to split a header into two parts.")
        print("header:", header)
        print("split:", split)
        exit()

    split[1] = split[1][1:]

    return split

# A function to parse the header of a class entry in the following format
# "[ [dep_id] [number] ]. [name] ([units]) [garbage]"
def parse_header(header):
    clean_header = cleanHeader(header)
    print(clean_header)
    parts = split_header(clean_header)
    if (len(parts) != 2):
        func.printError("Header could not be split into two parts. Exiting.")
        print("Header:", header)
        print("Split Header:", parts)
        exit()

    return {**parse_part_one(parts[0]), **parse_part_two(parts[1])}
