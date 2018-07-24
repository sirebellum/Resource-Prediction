from __future__ import print_function

import sys, os, time
import swf # Custom swf reading code

# dictionary that maps column name to integer index
clmn = swf.clmn

# Total memory usage per job (kb)
mem_total = [a*b for a,b in zip(swf.cpu,swf.mem)]
print( "Max memory allocated for a single job: {} MB".format( max(mem_total)/1024 ) )

#swf.dataset = swf.dataset[0:1000] # for testing

# Clustering data:
# from Towards Autonomic Workload Provisioning for Enterprise Grids and Clouds, Quiroz et. al.
mem = swf.memreq
cpu = [a*b/100.0 for a,b in zip(swf.cpureq,swf.cputimereq)]
             
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    plt.plot(mem, cpu, 'ro')
    plt.show()