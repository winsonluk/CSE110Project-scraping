#!/usr/bin/env python3

import sys
from bs4 import BeautifulSoup       # Import BeautiflSoup4
import requests
import os
import department_scraper
import json
import func


# Declare important constants
URL = "https://ucsd.edu/catalog/front/courses.html" # URL to start from
PARSER = 'html.parser'                              # Parser for BeautifulSoup

COURSE_IDEN = "courses"
HREF = 'href'

# Get HTML page
html_page = requests.get(URL)

# Convert into BeautifulSoup
soup = BeautifulSoup(html_page.text, PARSER)


def convToFileName(url):
    return url[2:]

def checkCommandLineArguments():
    if (len(sys.argv) == 2):
        if (sys.argv[1] == "-v"):
            return True
    return False

def final_print(classes):
    print(json.dumps(classes, indent=2))

def get_classes(verbose):
    func.verbose = verbose

    # Gets all relevant links to departmental pages
    links = soup.find_all('a', href=True)

    # For each link, explore it and get the information
    classes = {}
    for s in links:
        if (s.text == COURSE_IDEN):
            if (func.verbose):
                print(s)
            url = department_scraper.generateURL(s[HREF])

            # Check if the element is founud in the stored HTML files
            path = os.path.join(os.path.dirname(__file__),
                'resources/stored_pages' + convToFileName(s[HREF]))
            if os.path.isfile(path):
                classes.update(department_scraper.scrape_dep_html(open(path)))
            else:
                classes.update(department_scraper.scrape_department(url))

            if (func.verbose):
                print(s)
                print("Length:", len(classes))
                print("\n =-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")

    return classes


if __name__ == "__main__":
    classes = get_classes(checkCommandLineArguments())

    #final_print(classes)
