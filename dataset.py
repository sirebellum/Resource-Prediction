from __future__ import print_function

import sys, os, time

# Parse a single line from swf file, without filtering.
# Returns a list of all the elements in the line.
# Returns next uncommented line (skips lines beginning with ;)
def parse_line(line):
    
    string = line.decode("utf-8") # Convert to string type
    string = string.strip("\n")
    string = string.split() # Parse out white space

    return string
    
    
# Filter function for each line to be used in list comprehension.
# Not specifying an option argument puts the function in "parse" mode
# Specifying an option argument will set up filter options for the current session
# Automatically filters out commented lines.
def filter(line, options=None):

    # Filtering mode (no options for now)
    if options is None:
    
        if ";" in str(line):
            return False # Skip commented lines
            
        # other filtering logic (to be implemented [tbi]) #
    
        return True # Allow all for now

        
    # Options set up mode
    if len(options) == 0:
        
        # Options parsing (tbi) #
        
        return "Parsing unimplemented"

        
### MAIN ###
# dataset from http://www.cs.huji.ac.il/labs/parallel/workload/
file = open('LANL-CM5-1994-4.1-cln.swf', 'rb')

# Set filter options (tbi) #

# parse swf file line by line
dataset = [parse_line(line) for line in file if filter(line)]

# dictionary that maps column name to integer index
column = {"#": 0,
          "Submit Time": 1,
          "Wait Time": 2,
          "Run Time": 3,
          "CPUs": 4,
          "CPU Time": 5,
          "Mem": 6,
          "Req CPUs": 7,
          "Req Time": 8,
          "Req Mem": 9,
          "Status": 10,
          "User": 11,
          "Group": 12,
          "Exec": 13,
          "Queue": 14,
          "Partition": 15}
          
print( column )
          

job_count = len(dataset)
print( "{} total jobs in the dataset".format(job_count) )