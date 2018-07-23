from __future__ import print_function

import sys, os
import swf # Custom swf reading code
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Returns 1 if dividing by 0
def safe_divide(value1, value2):

    if value2 == 0:
        return 1
    
    return value1/value2

# Predict response time based on weighted equations
def predict(mem, cpu, pindex):

    b0, b1, b2, b3, b12, b13, b23, b11, b22, b33 = \
        929.25, 2.832, -1.764e-4, 1.420, 1.272e-4, \
        -3.666e-4, -6.989e-6, -6.903e-3, -1.087e-6, -6.075e-6
        
    # List of equations to be summed
    equation = [b0, b1*cpu, b2*mem, b3*pindex, b12*cpu*mem, b13*cpu*pindex, \
                b23*mem*pindex, b11*cpu*cpu, b22*mem*mem, b33*pindex*pindex]
                
    w = sum(equation)

    return w
    
 # Get data
cpu = swf.cpu
mem = swf.mem
pindex = swf.pindex
wall_time = swf.wall_time
time = swf.time

cpureq = swf.cpureq
memreq = swf.memreq
pindexreq = swf.pindexreq

# Consolidate data
data = [ [cpureq[x], memreq[x], pindexreq[x] ] for x in range(len(pindexreq)) ]

# Predict
w = [predict( job[1], job[0], job[2] ) for job in data]

if __name__ == "__main__":

    # Plot prediction surface
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')

    # Generate axes
    x = np.arange(0, 3.5e4, 0.25e4) # mem
    y = np.arange(0, 1100, 100)     # cpu
    z = np.arange(0, 5e4, 0.5e4)    # pindex
    
    # Generate points and calculate points' values
    test = np.array(np.meshgrid(x, y, z)).T.reshape(-1,3)
    c = np.array([predict( axes[0], axes[1], axes[2] ) for axes in test])
    
    # Retrieve data points
    x = [ entry[0] for entry in test ]
    y = [ entry[1] for entry in test ]
    z = [ entry[2] for entry in test ]
    
    # label axes
    ax.set_xlabel('Memory/VM')
    ax.set_ylabel('#VMs')
    ax.set_zlabel('pindex')
    
    # Match paper's orientation
    ax.invert_xaxis()
    # Plot real data over response surface
    ax.scatter(memreq, cpureq, pindexreq, c=pindex, cmap=plt.get_cmap('RdYlGn'), alpha=0.75)
    ax.scatter(x, y, z, c=c, cmap=plt.get_cmap('RdYlGn'), alpha=0.35)
    
    
    # Compute accuracy
    ratios = [ safe_divide( w[i], pindexreq[i] ) for i in range(len(w)) ]
    average_ratio = sum(ratios) / len(ratios)
    
    averages = [ sum(ratios[i:i+1000]) / len(ratios[i:i+1000]) \
                         for i in range(0, len(ratios), 1000) ]
    
    print("Average ratio of predicted to expected response time: {}".format(average_ratio))
    # Plot average response time ratio
    fig2 = plt.figure(2)
    fig2.add_subplot(111)
    plt.plot(averages)
    
    plt.show()