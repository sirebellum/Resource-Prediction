from __future__ import print_function

import sys, os
import swf # Custom swf reading code
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import sklearn.metrics as metrics
import models
from math import sqrt

# Returns 1 if dividing by 0
def safe_divide(value1, value2):

    if value2 == 0:
        return 1
    
    return value1/value2

# Predict response time based on weighted equations
counter = 0
def predict(data, model):
        
    w = model(*data)
    
    # Progress report
    global counter
    counter = counter + 1
    if counter % 10000 == 0:
        print (counter, "processed!")

    return w
    
def accuracy_dist(actual, pred):
    
    diff = [ abs(actual[x] - pred[x]) for x in range(0, len(actual)) ]
    # count of errors below times
    error = [0, 0, 0, 0]
    for item in diff:
        if item <= 10: # Less than 10 seconds
            error[0] = error[0] + 1
        if item <= 60: # Less than a minute
            error[1] = error[1] + 1
        if item <= 60*10: # Less than 10 minutes
            error[2] = error[2] + 1
        if item <= 60*60: # Less than an hour
            error[3] = error[3] + 1
    
    return error
    
def accuracy_ratio(actual, pred):

    def ratio(act, sup):
        if act == sup:  return 1
        elif act > sup: return sup/act
        elif act < sup: return act/sup
        
    ratios = [ ratio( actual[x], pred[x] ) for x in range(0, len(actual)) ]
    
    # Average ratio    
    return sum(ratios)/len(ratios)


# Get data
cpu = swf.cpu
mem = swf.mem
pindexreq= swf.pindexreq
wall_time = swf.wall_time
time = swf.time
cputime = swf.cputime
usr = swf.usr
exe = swf.exe

# Consolidate data
data = [ [cpu[x], mem[x], pindexreq[x], usr[x], exe[x] ] for x in range(swf.job_count) ]

# Predictions
#model = models.qrsm
model = models.supportvm
data = models.svm_preprocess(data)

w = [predict( job, model ) for job in data]


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    '''
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
    ax.scatter(mem, cpu, pindexreq, c=wall_time, cmap=plt.get_cmap('RdYlGn'), alpha=0.5)
    ax.scatter(x, y, z, c=c, cmap=plt.get_cmap('RdYlGn'), alpha=0.5)
    '''
    # Calculate MAE values 
    mean_time = sum(wall_time)/len(wall_time)
    actual = sqrt(metrics.mean_absolute_error(wall_time, w))
    print( "Mean error: {}, {:.2f}% of mean time" \
                    .format(actual, 100*actual/mean_time) )
   
    # Accuracy [below 10 seconds, below 1 minute, below 10 minutes, below 60 minutes]
    accuracy = accuracy_dist(wall_time, w)
    print( "{:.2f}% of errors below 10 seconds".format(100*accuracy[0]/swf.job_count) )
    print( "{:.2f}% of errors below 1  minute".format(100*accuracy[1]/swf.job_count) )
    print( "{:.2f}% of errors below 10 minutes".format(100*accuracy[2]/swf.job_count) )
    print( "{:.2f}% of errors below 60 minutes".format(100*accuracy[3]/swf.job_count) )
    
    # Accuracy metric from Trade-off between... runtime estimates Yuping et al.
    ratio = accuracy_ratio(wall_time, w)
    print( "Ratio accuracy is {}".format(ratio) )
   
    '''
    # Compute ratio of predicted time to requested runtime as in paper
    ratios = [ safe_divide( w[i], wall_time[i] ) for i in range(len(w[0:150000])) ]
    average_ratio = sum(ratios) / len(ratios)
    
    averages = [ sum(ratios[i:i+1000]) / len(ratios[i:i+1000]) \
                         for i in range(0, len(ratios), 1000) ]
    
    print("Average ratio of predicted to actual response time: {}".format(average_ratio))
    # Plot average response time ratio
    fig2 = plt.figure(2)
    fig2.add_subplot(111)
    plt.plot(averages[0:70])
    
    plt.show()
    '''
