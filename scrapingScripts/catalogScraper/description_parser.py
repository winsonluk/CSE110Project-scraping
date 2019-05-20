import sys
import re
import func

from string import punctuation

preReqHeader = "Prerequisites: "
preReqIden = ""
desc_delimeters = {". "}
descRegex = '|'.join(map(re.escape, desc_delimeters))

passNoPassOnly = "P/NP grades only"
descPNPSentences = { passNoPassOnly, preReqIden}

def parse_description(description):
    dict = {}

    desc_split = re.split(descRegex, description)

    # Ensure a minimum length
    if (len(desc_split) == 0):
        func.printError("Length of desc_split was 0, and must be positive.")
        exit()

    index = 0
    # Iterate forward until we are done with the description
    dict['class_description'] = desc_split[0] + "."
    while (index < len(desc_split) and not (desc_split[index] in descPNPSentences) and 'requis' not in desc_split[index]):
        dict['class_description'] +=  " " + desc_split[index] + "."
        index = index + 1

    # There was no information on pass no pass options
    if (index < len(desc_split) and desc_split[index] == passNoPassOnly):
        dict['pnp_only'] = True
        index = index + 1
    else:
        dict['pnp_only'] = False

    # Get all other misc information
    while index < len(desc_split) and 'requis' not in desc_split[index]:
        index = index + 1

    # Check if there is any more
    if (index == len(desc_split)):
        dict['recognized_prereqs'] = []
        dict['unrec_prereqs'] = []

    elif len(desc_split) > index:
        # Get the pre-requisites list
        req_str = desc_split[index:][0].replace('\n', '')

        # Separate into recognized and unreconized pre-requisites
        re_course = '\w+\s\d\w*'

        prereqs = re.findall(re_course, req_str)
        split = re.split(re_course, req_str)
        dict['unrec_prereqs'] = []

        # find prereqs
        if prereqs:

            total_prereqs = [] # comprehensive list of ands (made up of running lists of ors)
            curr_prereqs = [] # current running list of ors

            for i, prereq in enumerate(prereqs):

                # append to current running list of ors
                curr_prereqs.append(prereq.upper())

                if i < len(split) - 1:
                    separator = split[i + 1]

                    # current running list of ors ended, so append to list of ands
                    if 'and' in separator:
                        total_prereqs.append(curr_prereqs)
                        curr_prereqs = []

            # append remaining courses
            if curr_prereqs:
                total_prereqs.append(curr_prereqs)

            dict['recognized_prereqs'] = total_prereqs

        else:
            dict['recognized_prereqs'] = []

        # Append rest of the description (which should be prereqs separated by periods)
        unrec_prereqs = ''
        while (index < len(desc_split)):
            index = index + 1
            next_sentence = desc_split[index - 1:][0].replace('\n', '').strip()
            if next_sentence and next_sentence[-1].isalnum():
                next_sentence = next_sentence + '. '
            unrec_prereqs = unrec_prereqs + next_sentence

        dict['unrec_prereqs'] = unrec_prereqs

    return dict
