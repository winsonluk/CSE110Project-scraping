#!/usr/bin/env python3

import re
import sys

from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


sys.path.insert(0, './scrapingScripts/catalogScraper')
import catalog_scraper

# CSE 100, 101, 110 -> CSE 100, CSE 101, CSE 110
def prepend(courses):
    prepended = [] # list of courses to return
    department = '' # current department we're iterating through
    for course in courses:
        number = course.strip()
        if course[0:1].isupper() or course[0:1].islower(): # if course is the first in a list (i.e., the 'CSE 100' in 'CSE 100, 101, 110')

            # Split string into department and number by finding the first occurrence of a digit in the string
            index = re.search('\d', course)
            if index:
                department = course[0:index.start()].strip() # set the current department for subsequent courses (i.e., the '101' and '110' in 'CSE 100, 101, 110')
                number = course[index.start():]
        prepended.append(department + number) # prepend the current department to the current course number
    return prepended

# Format courses as "[DEPARTMENT] [NUMBER]"
def cfilter(courses):
    filtered = []
    for course in courses:
        if type(course) is str:
            str_course = course
        else:
            str_course = course.find(text=True, recursive=False)
        if str_course is not None and '.' not in str(course):
            str_course = str_course.replace(' ', '').replace('globalseminar', '')

            # Split string into department and number by finding the first occurrence of a digit in the string
            index = re.search('\d', str_course)
            if index:
                department = str_course[0:index.start()].strip()
                number = re.sub(r'\([^)]*\)', '', str_course[index.start():]) # remove parentheses and stuff inside them
                title = department + ' ' + number
                if title not in filtered:
                    filtered.append(title)
    return filtered

application = Flask(__name__)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/scrape', methods = ['GET', 'POST'])
def scrape():


    if request.method == 'POST':

        # Save and open POSTed degree audit
        try:
            file = request.files['file']
            if file:

                file.save('audit.html')
                with open('audit.html', 'rb') as html_doc:

                    # Parse major and courses, using prepend() and cfilter() for formatting
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    major = [element for element in soup.find_all('div', class_='reqHeader') if 'B' in str(element)][0].find(text=True, recursive=False).strip()
                    ipCourses = cfilter(soup.select('.completedCourses .ip .course'))
                    completedCourses = [course for course in cfilter(soup.select('.completedCourses .takenCourse .course')) if course not in ipCourses]
                    missingCourses = [course for course in cfilter(prepend(cfilter(soup.select('.course .number')))) if course not in ipCourses and course not in completedCourses]

                    # Create JSON
                    to_return = {}
                    to_return['major'] = major
                    to_return['ip'] = ipCourses
                    to_return['completed'] = completedCourses
                    to_return['missing'] = missingCourses

                    print(to_return)
                    return jsonify(to_return)

        except Exception as e:
            return str(e.message)

    else:
        return '''
        <html>
        <form action="" method="POST" enctype="multipart/form-data">
          <div>
            <p>Upload your degree audit (HTML only)</p>
            <p><input type="file" name="file"></p>
            <p><input type="submit" value="Upload">
          </div>
        </form>
        </html>
        '''

@application.route('/classes')
def classes():
    return jsonify(catalog_scraper.get_classes(True))

if __name__ == '__main__':
    application.run(host="0.0.0.0")
