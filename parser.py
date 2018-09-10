from __future__ import print_function

import sys, os
import numpy as np
from datetime import datetime
from operator import itemgetter

# Parse swf files
def parseSWF(filename, options=list()):

    # dictionary that maps column name to integer index
    clmn = {"#": 0,
          "submit": 1,
          "wait": 2,
          "wall.time": 3,
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
        
    # Convert data to ints, unless a valid string
    def parse(value):

        try: # for int
            new_value = int(value)
        except ValueError:
            try: # for float
                new_value = float(value)
            except ValueError:
                new_value = value
            
        return new_value
    
    # Filter function for each line to be used in list comprehension.
    # Specifying an option argument will filter for those options.
    # Format is (index, -/+value) per option, where -/+ mean exclude/include-only
    # Automatically filters out commented lines.
    def filter(line, options=None):
        
        # Parse line for ease of filtering
        string = parse_line(line)
        
        if ";" in str(line):
            return False # Skip commented lines

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
        
    # Filtering options
    #options.append( [ clmn["status"], "+1"] ) # Ignore cases where job didn't complete
    
    ### Begin Parsing
    #Read Dataset
    # datasets from http://www.cs.huji.ac.il/labs/parallel/workload/
    #filename = 'ANL-Intrepid-2009-1.swf'
    print( "Accessing {} dataset...".format( filename.strip(".swf") ) )
    file = open(filename, 'rb')
    
    # parse swf file line by line
    dataset = [parse_line(line) for line in file if filter(line, options=options)]
    
    job_count = len(dataset)
    print( "{} total jobs in the dataset".format(job_count) )

    ### Accumulate and Consolidate Data
    swf_dataset = {}
    for key in clmn.keys():
        swf_dataset[key] = [ parse( job[ clmn[key] ] ) for job in dataset ]
        
    return swf_dataset
    
# Remove invalid features
def pruneData(data):
  try:
    new_data = {}
    for key in data.keys():
        range = max(data[key]) - min(data[key])
        # If only 1 value within feature
        if range != 0:
            new_data[key] = data[key]
  except:
       import ipdb; ipdb.set_trace()
  return new_data
    
# Sort data by the provided key
def sortData(data, sort_key):

    # get position of the sort_key
    key_index = list(data.keys()).index(sort_key)
    # break dictionary out into lists
    sort_list = list()
    for key in data.keys():
        sort_list.append( data[key] )
        
    # format for sorting
    sort_list = list(zip(*sort_list))        
    # Sort
    sort_list.sort(key=itemgetter(key_index))
    # put into original format
    sort_list = list(zip(*sort_list)) 

    # Put lists back into dictionary
    sorted_data = {}
    index = 0
    for key in data.keys():
        sorted_data[key] = sort_list[index]
        index += 1
    
    return sorted_data


    
# Display histogram
def histogram(x, name, nbins=10):

    # the histogram of the data
    n, bins, patches = plt.hist(x, bins=nbins)

    plt.xlabel(name)
    plt.ylabel('Frequency')
    plt.grid(True)
    
    # Log y scale
    plt.yscale('log', nonposy='clip')
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    ### Acquire Data ###
    data = parseSWF("LANL-CM5-1994-4.1-cln.swf")
    data = pruneData(data)
    data = sortData(data, 'submit')

    ### Plot Data ###
    duration = ( max(data['submit'][0:5000]) - min(data['submit'][0:5000]) ) / 1e5
    plt.xticks(np.arange(0, duration+100, duration/5))
    plt.xlabel('time (s)')
    # Wall time
    plt.subplot(4, 1, 1)
    plt.plot(data['submit'][0:5000], data['wall.time'][0:5000], 'b-')
    plt.ylabel('walltime')
    # average response time per core
    plt.subplot(4, 1, 2)
    plt.plot(data['submit'][0:5000], data['time.cpu'][0:5000], 'b-')
    plt.ylabel('p index')
    # CPUs
    plt.subplot(4, 1, 3)
    plt.plot(data['submit'][0:5000], data['cpu'][0:5000], 'b-')
    plt.ylabel('cores')
    # Mem
    plt.subplot(4, 1, 4)
    plt.plot(data['submit'][0:5000], data['mem'][0:5000], 'b-')
    plt.ylabel('mem/core')
    
    fig2 = plt.figure(2)
    fig2.add_subplot(111)
    histogram(data['wall.time'], "Wall Time")

    plt.show()
