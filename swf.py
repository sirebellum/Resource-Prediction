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
filename = 'LANL-CM5-1994-4.1-cln.swf'
print( "Accessing {} dataset...".format( filename.strip(".swf") ) )
file = open(filename, 'rb')

# Set filter options (tbi) #

# parse swf file line by line
dataset = [parse_line(line) for line in file if filter(line)]

# dictionary that maps column name to integer index
clmn  =  {"#": 0,
          "submit": 1,
          "wait": 2,
          "run": 3,
          "cpu": 4,
          "time.cpu": 5, # per core
          "mem": 6,
          "cpu.req": 7,
          "time.req": 8, # requested cpu time
          "mem.req": 9,
          "status": 10,
          "usr": 11,
          "grp": 12,
          "exec": 13,
          "queue": 14,
          "partition": 15}


# Cursory test of dataset/clmn structure
#for job in dataset[0:10]:
#    print( "Job {}: {} cores requested, {} cores allocated".format(job[ clmn["#"] ],
#                                                                   job[ clmn["Req CPUs"] ],
#                                                                   job[ clmn["CPUs"] ]) )

job_count = len(dataset)
print( "{} total jobs in the dataset".format(job_count) )