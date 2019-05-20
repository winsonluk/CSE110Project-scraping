#!/usr/bin/env python3

import re
import sys
from bs4 import BeautifulSoup

def prepend(courses):
    prepended = []
    department = ''
    for course in courses:
        number = course.strip()
        if course[0:1].isupper() or course[0:1].islower():
            index = re.search('\d', course)
            if index:
                department = course[0:index.start()].strip()
                number = course[index.start():]
        prepended.append(department + number)
    return prepended

def cfilter(courses):
    filtered = []
    for course in courses:
        if type(course) is str:
            str_course = course
        else:
            str_course = course.find(text=True, recursive=False)
        if str_course is not None and '.' not in str(course):
            str_course = str_course.replace(' ', '')
            index = re.search('\d', str_course)
            if index:
                department = str_course[0:index.start()].strip()
                number = re.sub(r'\([^)]*\)', '', str_course[index.start():])
                filtered.append(department + ' ' + number)
    return filtered

to_open = 'audits/audit_' + sys.argv[1] + '.html'

with open(to_open, 'rb') as html_doc:
    soup = BeautifulSoup(html_doc, 'html.parser')
    major = [element for element in soup.find_all('div', class_='reqHeader') if 'B' in str(element)][0].find(text=True, recursive=False)
    completedCourses = cfilter(soup.select('.completedCourses .takenCourse .course'))
    missingCourses = cfilter(prepend(cfilter(soup.select('.course .number'))))
    print('MAJOR: ' + str(major))
    print('COMPLETED COURSES: ' + str(completedCourses))
    print('MISSING COURSES: ' + str(missingCourses))
