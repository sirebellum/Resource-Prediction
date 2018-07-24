from __future__ import print_function

import sys, os
import swf # Custom swf reading code
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import sklearn.metrics as metrics
import models

# Returns 1 if dividing by 0
def safe_divide(value1, value2):

    if value2 == 0:
        return 1
    
    return value1/value2

# Predict response time based on weighted equations
def predict(mem, cpu, pindex, model):

    w = model(mem, cpu, pindex)

    return w
    
# Get data
cpu = swf.cpu
mem = swf.mem
pindex = swf.pindex
wall_time = swf.wall_time
time = swf.time
cputime = swf.cputime

cpureq = swf.cpureq
memreq = swf.memreq
pindexreq = swf.pindexreq
cputimereq = swf.cputimereq


# Consolidate data
data = [ [cpu[x], mem[x], pindex[x] ] for x in range(len(time)) ]
datareq = [ [cpureq[x], memreq[x], pindexreq[x] ] for x in range(len(time)) ]

# Predictions
model = models.qrsm

w = [predict( job[1], job[0], job[2], model ) for job in data]
wreq = [predict( job[1], job[0], job[2], model ) for job in datareq]

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
    c = np.array([predict( axes[0], axes[1], axes[2], model ) for axes in test])
    
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
    ax.scatter(mem, cpu, pindex, c=wall_time, cmap=plt.get_cmap('RdYlGn'), alpha=0.5)
    ax.scatter(x, y, z, c=c, cmap=plt.get_cmap('RdYlGn'), alpha=0.5)
    
    # Calculate R2 values 
    actual = metrics.r2_score(wall_time, w)
    predicted = metrics.r2_score(wall_time, wreq)
    print( "Actual model accuracy: {}".format(actual) )
    print( "Predictive model accuracy: {}".format(predicted) )
    
    # Compute ratio of predicted time to requested runtime as in paper
    ratios = [ safe_divide( w[i], cputimereq[i] ) for i in range(len(w[0:150000])) ]
    average_ratio = sum(ratios) / len(ratios)
    
    averages = [ sum(ratios[i:i+1000]) / len(ratios[i:i+1000]) \
                         for i in range(0, len(ratios), 1000) ]
    
    print("Average ratio of predicted to expected response time: {}".format(average_ratio))
    # Plot average response time ratio
    fig2 = plt.figure(2)
    fig2.add_subplot(111)
    plt.plot(averages[0:70])
    
    plt.show()