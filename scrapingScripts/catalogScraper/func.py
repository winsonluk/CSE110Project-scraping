import sys
import re

verbose = False

def printError(s):
    print("ERROR")
    print("===========")
    print(s)

def outputInformation(dict):
    for entry in dict:
        print(entry, ":", dict[entry])
