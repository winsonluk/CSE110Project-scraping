import sys
import re
import func

from string import punctuation

preReqIden = ""
desc_delimeters = {". ", ".)"}
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
    while (index < len(desc_split) and not (desc_split[index] in descPNPSentences) and 'Prerequis' not in desc_split[index]):
        dict['class_description'] +=  " " + desc_split[index] + "."
        index = index + 1

    # There was no information on pass no pass options
    if (index < len(desc_split) and desc_split[index] == passNoPassOnly):
        dict['pnp_only'] = True
        index = index + 1
    else:
        dict['pnp_only'] = False

    # Get all other misc information
    while index < len(desc_split) and 'Prerequis' not in desc_split[index]:
        index = index + 1

    # Check if there is any more
    if (index == len(desc_split)):
        dict['recognized_prereqs'] = []
        dict['unrec_prereqs'] = []

    elif len(desc_split) > index:
        # Get the pre-requisites list
        req_str = desc_split[index:][0].replace('\n', '')

        # Separate into recognized and unreconized pre-requisites
        re_course = '\w*\s\w*[^\S]*\d[\w|-]*'

        prereqs = re.findall(re_course, req_str)
        split = re.split(re_course, req_str)
        dict['unrec_prereqs'] = []

        # find prereqs
        if prereqs:

            total_prereqs = [] # comprehensive list of ands (made up of running lists of ors)
            curr_prereqs = [] # current running list of ors
            curr_dep = ''
            curr_conjunction = ''
            added = False

            for i, prereq in enumerate(prereqs):

                prereq = prereq.strip().upper()

                # GPA of 2.5 -!-> 'OF 2'
                if prereq[:4] == 'OF 2' or prereq[:4] == 'OF 3' or 'GPA' in prereq:
                    continue

                or_index = ''.join(prereqs[i:]).strip().upper().find('OR')
                and_index = ''.join(prereqs[i:]).strip().upper().find('AND')

                if or_index != -1 and (and_index == -1 or or_index < and_index):
                    curr_conjunction = 'OR'

                if and_index != -1 and (or_index == -1 or and_index < or_index):
                    if curr_conjunction == 'OR' and curr_prereqs:
                        total_prereqs.append(curr_prereqs)
                        added = True
                        curr_prereqs = []
                    curr_conjunction = 'AND'

                if ' AND ' not in req_str.upper() and prereq[:3] != 'OR ' and curr_prereqs:
                    total_prereqs.append(curr_prereqs)
                    added = True
                    curr_prereqs = []

                # One from VIS 164, 165, 168
                if prereq[:5] == 'FROM ' and not added:
                    total_prereqs.append(curr_prereqs)
                    curr_prereqs = []
                    added = True
                    prereq = prereq[4:].strip()

                # MAJORS WWW NNN AND WWW NNN, COURSES WWW NNN
                if prereq[:7] in ['MAJORS ', 'COURSES', 'EITHER ']:
                    prereq = prereq[7:].strip()

                # BOTH WWW NNN AND WWW NNN
                if prereq[:5] in ['BOTH ', 'FROM ']:
                    prereq = prereq[5:].strip()

                # WWW NNN and NNN -> WWW NNN and WWW NNN
                if prereq[:3] in ['AND', 'FOR']:
                    prereq = prereq[4:].strip()

                # WWW NNN or NNN -> WWW NNN or WWW NNN
                if prereq[:3] in ['OR ', 'TO ', 'OF ']:
                    prereq = prereq[3:].strip()

                # A grade of C or higher in CHEM 140A or 40A is strongly recommended
                if (prereq[:3] == 'IN '
                    or prereq[:9] == 'SAN DIEGO'
                    or prereq[:12] == 'PREREQUISITE'
                    or prereq[:10] == 'MATH LEVEL'
                    or prereq[:7] == 'MINIMUM'
                    or prereq[:8] == 'LANGUAGE'
                    or prereq[:8] == 'STUDENTS'
                    or prereq[:5] == 'MAJOR'
                    or prereq[:7] == 'STUDIES'
                    or prereq[:8] == 'ENROLLED'
                    or prereq[:9] == 'COMPLETED'
                    or prereq[:8] == 'STANDING'
                    or prereq[:7] == 'OVERALL'
                    or prereq[:4] == 'ERLY'
                    or prereq[:6] == 'RESULT'
                    or prereq[:5] == 'SCORE'
                    or prereq[:4] == 'WITH'
                    or prereq[:4] == 'TEST'
                    or prereq[:4] == 'CODE'
                    or prereq[:4] == 'NONE'
                    or prereq[:3] == 'AT '
                    or prereq[:3] == 'II '
                    or prereq[:3] == 'AN '
                    or prereq[:6] == 'ONLINE'
                    or (prereq.strip().split(' ')[0].isdigit() and len(prereq.strip().split(' ')) > 1 )):

                    continue

                # WWW NNN, NNN, and NNN -> WWW NNN and WWW NNN and WWW NNN
                if not any([c.isspace() for c in prereq.strip()]):
                    prereq = curr_dep + ' ' + prereq

                # CS26 EC26
                if len(prereq.split(' ')) == 2 and ('CS' in prereq.split(' ')[1] or 'EC' in prereq.split(' ')[1]):
                    continue

                # WWW NNN or NNN -> WWW NNN or WWW NNN
                if len(prereq.split(' ')[0]) == 1:
                    prereq = prereq[2:].strip()

                prereq = prereq.replace('PHYSICS', 'PHYS')
                prereq = prereq.replace('COG SCI', 'COGS')
                prereq = prereq.replace('PSYCHOLOGY', 'PSYC')
                prereq = prereq.replace('COGNITIVE SCIENCE', 'COGS')
                prereq = prereq.replace('PHILOSOPHY', 'PHIL')
                prereq = prereq.replace('POLITICAL SCIENCE', 'POLI')
                prereq = prereq.strip().replace('\t','')
                prereq = ' '.join(prereq.split())

                if prereq.strip().isdigit():
                    continue

                if len(prereq.strip().split(' ')) > 2:
                    print(prereq.strip())
                    raise Exception

                curr_prereqs.append(prereq.strip())

                this_dep = curr_prereqs[0].split(' ')[0]
                if all(not c.isdigit() for c in this_dep):
                    curr_dep = this_dep

                if i < len(split) - 1:

                    # current running list of ors ended, so append to list of ands
                    if curr_conjunction == 'AND' and not added and and_index != 0:
                        for p in curr_prereqs:
                            total_prereqs.append([p])
                        curr_prereqs = []

                    added = False

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
