import sys
sys.path.insert(0, '..')

from class_parser import parse

with open('../resources/dep.txt', 'r') as f:
    while True:
        header = f.readline()
        description = f.readline()
        space = f.readline()
        parsed = parse(header, description)
        print('COURSE: ' + parsed['number'])
        print('RECOGNIZED PREREQUISITES: ' + str(parsed['recognized_prereqs']))
        print('UNRECOGNIZED PREREQUISITES: ' + str(parsed['unrec_prereqs']))
        if not header or not description or not space: break
