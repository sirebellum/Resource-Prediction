from __future__ import print_function

import sys, os, time
import numpy as np
from datetime import datetime

# dictionary that maps column name to integer index
clmn  =  {"#": 0,
          "submit": 1,
          "start": 2,
          "end": 3,
          "cpu": 5,
          "time.cpu": 7, # per core
          "mem": 9,
          "cpu.req": 4,
          "time.req": 6, # requested cpu time
          "mem.req": 8,
          "status": 15,
          "usr": 12,
          "grp": 13,
          "exec": 14,
          "queue": 10}

# Parse a single line from swf file, without filtering.
# Returns a list of all the elements in the line.
# Returns next uncommented line (skips lines beginning with ;)
def parse_line(line):
    
    string = line.decode("utf-8") # Convert to string type
    string = string.strip("\n")
    string = string.split() # Parse out white space

    return string

# Parses date strings into elapsed seconds for job
def parse_duration(start, end):

    try:
        s = datetime.strptime(start, '%y/%m/%d-%H:%M:%S')
        e = datetime.strptime(end, '%y/%m/%d-%H:%M:%S')
        elapsed = e - s
    except ValueError: # if unknown
        return -1
        
    return elapsed.total_seconds()
    
# Calculate memory per core
def mem_core(total_mem, cpus):

    try:
        mem = int(total_mem) / int(cpus)
    except ValueError: # if unknown
        return float(0)
        
    return mem
    
# Filter function for each line to be used in list comprehension.
# Not specifying an option argument puts the function in "parse" mode
# Specifying an option argument will set up filter options for the current session
# Automatically filters out commented lines and uncompleted jobs.
def filter(line, options=None):
    global clmn
    
    # Parse line for ease of filtering
    string = parse_line(line)
    
    # Filtering mode (no options for now)
    if options is None:
    
        if ";" in str(line):
            return False # Skip commented lines
        if string[ clmn["status"] ] != "0000":
            return False # Skip uncompleted jobs
            
        # other filtering logic (to be implemented [tbi]) #
    
        return True

        
    # Options set up mode
    if len(options) == 0:
        
        # Options parsing (tbi) #
        
        return "Parsing unimplemented"
        
        
### Read Dataset ###
# dataset from http://www.cs.huji.ac.il/labs/parallel/workload/
filename = 'LANL-CM5-1994-0b'
print( "Accessing {} dataset...".format( filename.strip(".swf") ) )
file = open(filename, 'rb')

# Set filter options (tbi) #

# parse swf file line by line
dataset = [parse_line(line) for line in file if filter(line)]

# Cursory test of dataset/clmn structure
#for job in dataset[0:10]:
#    print( "Job {}: {} cores requested, {} cores allocated".format(job[ clmn["#"] ],
#                                                                   job[ clmn["Req CPUs"] ],
#                                                                   job[ clmn["CPUs"] ]) )

job_count = len(dataset)
print( "{} total jobs in the dataset".format(job_count) )

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    # relative time to first job for each job
    first_job = dataset[0][ clmn[ "submit" ] ]
    time = [ parse_duration( first_job, job[ clmn["submit"] ] ) \
                for job in dataset[0:1000] ]
    duration = max(time)
    
    # Memory consumption of each job per cpu
    mem = [ mem_core( job[ clmn["mem"] ], job[ clmn["cpu.req"] ] ) \
                for job in dataset[0:1000] ]
    
    # sort by time
    time, mem = (list(t) for t in zip(*sorted(zip(time, mem))))

    # Format plot
    plt.xticks(np.arange(0, duration+100, duration/5))
    
    plt.plot(time, mem, 'b-')
    plt.show()