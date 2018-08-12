from __future__ import print_function

import sys, os
import numpy as np
from datetime import datetime
from operator import itemgetter
import scipy.stats as stats

# dictionary that maps column name to integer index
clmn = {"#": 0,
          "submit": 1,
          "wait": 2,
          "run": 3,
          "cpu": 4,
          "time.cpu": 5,
          "mem": 6,
          "cpu.req": 7,
          "time.req": 8,
          "mem.req": 9,
          "status": 10,
          "usr": 11,
          "grp": 12,
          "exec": 13,
          "queue": 14,
          "partition": 15}

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
        return -1.0
        
    return elapsed.total_seconds()
    
# Calculate memory per core
def mempercore(total_mem, cpus):

    try:
        mem = int(total_mem) / int(cpus)
    except ValueError: # if unknown
        return float(0)
        
    return mem
    
# handle "unknown" fields
def parse(value):

    if value == "unknown":
        return 0
        
    return value
    
# Filter function for each line to be used in list comprehension.
# Specifying an option argument will filter for those options.
# Format is (index, -/+value) per option, where -/+ mean exclude/include-only
# Automatically filters out commented lines.
def filter(line, options=None):
    global clmn
    
    # Parse line for ease of filtering
    string = parse_line(line)
    
    if ";" in str(line):
        return False # Skip commented lines
    if parse_duration(string[ clmn["start"] ], string[ clmn["end"] ]) < 0:
        return False # Skip jobs with negative run-time

    # Parse with options
    if options is not None:
        for option in options:
        
            if option[1][0] == "-": #Exclude
                if string[ option[0] ] == option[1][1:]:
                    return False
                    
            elif option[1][0] == "+": #Include only
                if string[ option[0] ] != option[1][1:]:
                    return False
                    
            else:
                exit("Please specify +/- before option: \"{}\"".format(option[1]))
        
    return True

# Display histogram
def histogram(x, name):

    # the histogram of the data
    n, bins, patches = plt.hist(x, bins=50)

    plt.xlabel(name)
    plt.ylabel('Frequency')
    plt.grid(True)

    plt.show()
        

### Read Dataset ###
# dataset from http://www.cs.huji.ac.il/labs/parallel/workload/
filename = 'LANL-CM5-1994-4.1-cln.swf'
print( "Accessing {} dataset...".format( filename.strip(".swf") ) )
file = open(filename, 'rb')

# Filtering options
options = list()
#options.append( [ clmn[""], ""] ) # Ignore cases where # of used CPUs is unknown

# parse swf file line by line
dataset = [parse_line(line) for line in file if filter(line, options=options)]

# Cursory test of dataset/clmn structure
#for job in dataset[0:10]:
#    print( "Job {}: {} cores requested, {} cores allocated".format(job[ clmn["#"] ],
#                                                                   job[ clmn["cpu.req"] ],
#                                                                   job[ clmn["cpu"] ]) )

job_count = len(dataset)
print( "{} total jobs in the dataset".format(job_count) )

### Accumulate Data ###
# relative time to first job for each job
first_job = dataset[0][ clmn[ "start" ] ]
time = [ parse_duration( first_job, job[ clmn["start"] ] ) \
            for job in dataset ]
# Memory consumption of each job per cpu
mem = [ mempercore( job[ clmn["mem"] ], job[ clmn["cpu"] ] ) \
            for job in dataset ]
# CPUs used for each job
cpu = [ int( parse( job[ clmn["cpu"] ] ) ) \
            for job in dataset ]
# Wall time per job
wall_time = [ parse_duration( job[ clmn["start"] ], job[ clmn["end"] ] ) \
            for job in dataset ]
# Parallelism affinity per job cpu.time/CPUs
pindex = [ float(parse(job[ clmn["time.cpu"] ])) \
            for job in dataset ]
# Total cpu time
cputime = [ float(parse(job[ clmn["time.cpu"] ])) * float(parse(job[ clmn["cpu"] ]))\
            for job in dataset ]
            
# Requested resources:
# Memory consumption of each job per cpu
memreq = [ mempercore( job[ clmn["mem.req"] ], job[ clmn["cpu.req"] ] ) \
            for job in dataset ]
# CPUs used for each job
cpureq = [ int( parse( job[ clmn["cpu.req"] ] ) ) \
            for job in dataset ]
# Parallelism affinity per job cpu.time/CPUs
pindexreq = [ float(parse(job[ clmn["time.req"] ])) \
            for job in dataset ]
# Total cpu time requested
cputimereq = [ float(parse(job[ clmn["time.req"] ])) * float(parse(job[ clmn["cpu.req"] ]))\
            for job in dataset ]

### Sort Data ###
# Normalize time to start at 0
min_time = min(time)
time = list(map(lambda x: x - min_time, time))
# sort by time
data = list(zip(mem,
                cpu,
                pindex,
                memreq,
                cpureq,
                pindexreq,
                wall_time,
                time,
                cputime,
                cputimereq))
data.sort(key=itemgetter(7))
# Unzip
mem = list(zip(*data))[0]
cpu = list(zip(*data))[1]
pindex = list(zip(*data))[2]
memreq = list(zip(*data))[3]
cpureq = list(zip(*data))[4]
pindexreq = list(zip(*data))[5]
wall_time = list(zip(*data))[6]
time = list(zip(*data))[7]
cputime = list(zip(*data))[8]
cputimereq = list(zip(*data))[9]

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    ### Plot Data ###
    duration = ( max(time[0:5000]) - min(time[0:5000]) ) / 1e5
    plt.xticks(np.arange(0, duration+100, duration/5))
    plt.xlabel('time (s)')
    # Wall time
    plt.subplot(4, 1, 1)
    plt.plot(time[0:5000], wall_time[0:5000], 'b-')
    plt.ylabel('walltime')
    # average response time per core
    plt.subplot(4, 1, 2)
    plt.plot(time[0:5000], pindex[0:5000], 'b-')
    plt.ylabel('p index')
    # CPUs
    plt.subplot(4, 1, 3)
    plt.plot(time[0:5000], cpu[0:5000], 'b-')
    plt.ylabel('cores')
    # Mem
    plt.subplot(4, 1, 4)
    plt.plot(time[0:5000], mem[0:5000], 'b-')
    plt.ylabel('mem/core')
    
    fig2 = plt.figure(2)
    fig2.add_subplot(111)
    histogram(wall_time, "Wall Time")
    
    plt.show()
