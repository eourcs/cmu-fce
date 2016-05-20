import sys, getopt
import os
import glob
from enum import Enum

# Calvin Giroud
# CMU-FCE
# Python script that allows users to look up FCE information quickly
# Returns a nicely formatted summary enumerating avg. hrs/week and avg. rating
# Last Updated : 5/19/2016

class Type(Enum):
    semester = 0
    year = 1
    instructor = 2
    department = 3
    courseno = 4
    coursename = 5
    section = 6
    hours = 11
    rating = 20

# Constants
INDICES = [0,1,2,11,20]
PADDING = 2

def parse_summary(coursedata, top):
    # Newest TOP entries
    return sorted(coursedata, 
		  key=lambda x : int(x[Type.year.value]), 
                  reverse=True)[:top]

def andf(f, g):
    return lambda s : f(s) and g(s)

def parse_data(data, courseno, exclude):
    # Ignores Qatar section and FCE entries in the old format
    f = lambda s : (s[Type.courseno.value] == courseno)   \
		   and ("W" not in s[Type.section.value]) \
                   and ("3" not in s[Type.section.value]) \
                   and (s[Type.rating.value] != "")
    if exclude:
        f = andf(f, lambda s : (s[Type.semester.value] != "Summer"))

    return list(filter(f, data))
    
def print_summary(summary):
    f = lambda t : sum(map(lambda s : float(s[t]), summary)) / len(summary)
    
    # Get statistics
    avghours = f(Type.hours.value)
    avgrating = f(Type.rating.value)
    coursename = summary[0][Type.coursename.value]
    courseno = summary[0][Type.courseno.value]
    dept = summary[0][Type.department.value]

    print("{} - {} -{}".format(int(courseno), coursename, dept))
    print("AVG. HOURS: {} hrs/wk".format(round(avghours, 1)))
    print("AVG. RATING: {}/5.0".format(round(avgrating, 1)))
    print("")

def print_info(data):
    data = [[item[i].strip(" ") for i in INDICES] for item in data]
    headers = [["SEMESTER", "YEAR", "INSTRUCTOR", "HRS/WK", "RATING"]]
    data = headers + data
    
    # Padding
    col_width = [len(x) + PADDING for x in data[0]]
    col_width[2] = max(list(map(lambda x : len(x[2]), data)))
   
    # Print table
    for elem in data:
        for i in range(len(elem)):
            elem[i] = "{0:^{1}}".format(elem[i], col_width[i])
        print (" ".join(elem))

def print_coursedata(coursedata, verbose, top):
    if not coursedata:
        print("No data for class")
        sys.exit(2)

    summary = parse_summary(coursedata, top)
    print_summary(summary)

    if (verbose):
        print_info(coursedata)
    else:
        print_info(summary)

def read_files():
    path = os.path.join(os.getcwd(), "data")
    # Read all csv files
    result = []
    for filename in glob.glob(os.path.join(path, '*.csv')):
        with open(filename, 'r') as f:
            lines = map(lambda l : l.rstrip('\n'), filter(lambda l : l.strip(), f))
            r = list(map(lambda l : l.split(","), lines))
            
	    # Silly formatting issue 
            for e in r:
                if "co-taught" in e[3]:
                    del e[3]
            result.extend(r)
    
    return result

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hvet:n:", ["courseno=", "excludesummer"])
    except getopt.GetoptError:
        print('example.py -n <coursenumber>')
        sys.exit(2)
    
    # Default no. of results in summary
    top = 6

    # Parse cmdline arguments
    exclude, verbose = False, False
    for (opt, arg) in opts:
        if (opt == '-h'):
            print('example.py -n <coursenumber>')
            print("")
            print('Flags:')
            print("-e exclude summer semester")
            print("-t no. of results in summary (default=6)")
            print("-v verbose")
            print("-h help")
            sys.exit(2)
        elif (opt == '-v'):
            verbose = True
        elif (opt == '-t'):
            top = int(arg)
        elif (opt in ('-e', "--excludesummer")):
            exclude = True
        elif (opt in ('-n', "--courseno")):
            courseno = arg

    # Parse and print data
    data = read_files()
    coursedata = parse_data(data, courseno, exclude)
    print_coursedata(coursedata, verbose, top)

if __name__ == "__main__":
   main(sys.argv[1:])
