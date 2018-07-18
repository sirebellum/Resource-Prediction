from __future__ import print_function

import sys, os, time
import swf # Custom swf reading code

# dictionary that maps column name to integer index
clmn  =  {"#": 0,
          "submit": 1,
          "wait": 2,
          "run": 3,
          "cpu": 4,
          "time.cpu": 5, #per core
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

# Total memory usage per job (kb)
mem = [int(job[ clmn["mem"] ])*int(job[ clmn["cpu" ] ]) for job in swf.dataset]
print( "Max memory allocated for a single job: {} MB".format( max(mem)/1024 ) )