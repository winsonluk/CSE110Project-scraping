import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import sys
from bs4 import BeautifulSoup       # Import BeautiflSoup4
import requests
import os
import json
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

number_field_id = "ctl00_ContentPlaceHolder1_txtCourse"
submit_button = "ctl00_ContentPlaceHolder1_btnSubmit"
table_id = "ctl00_ContentPlaceHolder1_gvCAPEs"
course_name_id = "ctl00_ContentPlaceHolder1_gvCAPEs_ctl2089_hlViewReport"
PARSER = 'html.parser'                              # Parser for BeautifulSoup
init_sleep_time = 2
sleep_time = 10

username_key = "kweeton"
username_password = ""

def parse_courses(soup):# Need to remove extra white space
    dict = {}
    for elem in soup(id=re.compile('\S*hlViewReport\S*')):
        course_dict = get_course_info(elem)
        dict[course_dict['course_id']] = course_dict
    return dict

def parse_course_id(text):
    return text.replace(" - ", ':').replace("\s\s- ", ':').split(":")[0]

def get_course_info(course):
    term = course.find_next('td')
    enroll = term.find_next('td')
    evals_made = enroll.find_next('td')
    recommend_class = evals_made.find_next('td')
    recommend_inst = recommend_class.find_next('td')
    hours = recommend_inst.find_next('td')
    avg_grade_expected = hours.find_next('td')


    dict = {    "course_id":parse_course_id(course.text).strip(),
                "term": term.text.strip(),
                "enrolled": enroll.text,
                "evaluations": evals_made.text.replace("\n", '').replace("%", '').strip(),
                "rec_class": recommend_class.text.replace("\n", '').replace("%", '').strip(),
                "rec_inst": recommend_inst.text.replace("\n", '').replace("%", '').strip(),
                "hours": hours.text.replace("\n", '').replace("%", '').strip(),
                "avg_grade": avg_grade_expected.text.replace("\n", '').replace("%", '').strip()}
    return dict

def parse_html(html_text):
    soup = BeautifulSoup(html_text, PARSER)
    return parse_courses(soup)

# ------------------------------------------------------------------------------

username_id = "ssousername"
password_id = "ssopassword"


def click_button(value, browser):
    browser.find_element_by_xpath("//input[@value='" + value + "']").click();

def login_to_cape(browser):
    username = browser.find_element_by_id(username_id)
    password = browser.find_element_by_id(password_id)
    username.send_keys(username_key)
    password.send_keys(username_password)
    button = browser.find_element_by_name("_eventId_proceed")
    button.click()

def wait_until_exists(element_id, browser, max_time):
    #print("Waiting for", str(element_id), "to be displayed. Maximum wait time:", max_time)
    try:
        myElem = WebDriverWait(browser, sleep_time).until(EC.presence_of_element_located((By.ID, element_id)))
    except TimeoutException:
        print("Loading took too much time. Exiting")
        exit()

def set_field(id, text, browser):
    field = browser.find_element_by_id(id)
    field.clear()
    field.send_keys(text)

def get_html(browser):
    return browser.page_source

def init_browser():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get('http://www.cape.ucsd.edu/')
    return browser


course_entry_id = "courseNumber"
search_value = "Search"

def get_all_class_info(browser):
    courses = {}

    first_time = True
    for i in range(0, 10):
        set_field(course_entry_id, str(i), browser)
        click_button(search_value, browser)
        if (first_time == True):
            wait_until_exists(username_id, browser, 10)
            login_to_cape(browser)
        wait_until_exists(table_id, browser, 60)
        #print("Getting course info for", i, "...")
        courses = {**courses, **parse_html(get_html(browser))}
        if (first_time):
            browser.back()
            first_time = False
        browser.back()
        time.sleep(2)
    return courses



if __name__ == "__main__":
    browser = init_browser()
    time.sleep(init_sleep_time)
    courses = get_all_class_info(browser)
    print(json.dumps(courses, indent = 2))
