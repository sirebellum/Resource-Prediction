from __future__ import print_function

import sys, os, time
import swf # Custom swf reading code

# dictionary that maps column name to integer index
clmn = swf.clmn

# Total memory usage per job (kb)
mem_total = [ int(job[ clmn["mem"] ]) * int(job[ clmn["cpu" ] ]) \
            for job in swf.dataset ]
print( "Max memory allocated for a single job: {} MB".format( max(mem_total)/1024 ) )

#swf.dataset = swf.dataset[0:1000] # for testing

# Clustering data:
# from Towards Autonomic Workload Provisioning for Enterprise Grids and Clouds, Quiroz et. al.
mem = [ int(job[ clmn["mem.req"] ]) \
            for job in swf.dataset ]
cpu = [ float(job[ clmn["cpu.req"] ]) * float(job[ clmn["time.req"] ]) / 100.0 \
            for job in swf.dataset ]
             
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    plt.plot(mem, cpu, 'ro')
    plt.show()