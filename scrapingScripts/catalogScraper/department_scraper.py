import sys
from bs4 import BeautifulSoup       # Import BeautiflSoup4
import requests

import class_parser
import func

# Declare importation constants
PARSER = 'html.parser'                              # Parser for BeautifulSoup
BASE = "https://ucsd.edu/catalog"

useNext = True

# Declare page specific constants
course_name_id = "course-name"
course_desc_id = "course-descriptions"

def generateURL(link):
    return BASE + link[2:]

def scrape_department(url):
    html_page = requests.get(url)
    return scrape_dep_html(html_page.text)


def scrape_dep_html(html_page):
    soup = BeautifulSoup(html_page, PARSER)

    # Get all course names
    course_name = soup.find_all('p', attrs={ 'class':course_name_id })

    # Get all course descriptions
    course_desc = []
    if (useNext):
        for s in course_name:
            course_desc = course_desc + [ s.find_next_sibling('p') ]
    else:
        course_desc = soup.find_all('p', { 'class':course_desc_id })

    if (len(course_name) != len(course_desc)):
        printError("There were " + len(course_name) + " course names generated.")
        print("There were", len(course_desc), "course descriptions generated.")
        print("This was done for link", url, ".")
        print("These numbers must be equal for the program to function correctly")
        print("The program will now terminate")
        exit()

    classes = {}
    for i in range(len(course_desc)):   # Add to classes
        parsed = class_parser.parse(course_name[i], course_desc[i])
        classes[parsed['department_id'] + ' ' + parsed['number']] = parsed

    return classes

def checkCommandLineArguments():
    if (len(sys.argv) != 2):
        func.printError("Use: python3 " + sys.argv[0] + " [department_url]")
        exit()

if __name__ == "__main__":
    checkCommandLineArguments()
    scrape_department(sys.argv[1])
