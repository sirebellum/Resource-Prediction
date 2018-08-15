from __future__ import print_function
import os
from sklearn import svm
from sklearn.metrics import accuracy_score
import numpy as np
import random
import pickle
import pandas

### TODO: Implement model that takes window of previous usage for each user
### TODO: Implement easy multithreading interface for functions

# QRSM model from paper
def qrsm(mem, cpu, pindex, usr):

    b0, b1, b2, b3, b12, b13, b23, b11, b22, b33 = \
        929.25, 2.832, -1.764e-4, 1.420, 1.272e-4, \
        -3.666e-4, -6.989e-6, -6.903e-3, -1.087e-6, -6.075e-6
        
    # List of equations to be summed
    equation = [b0, b1*cpu, b2*mem, b3*pindex, b12*cpu*mem, b13*cpu*pindex, \
                b23*mem*pindex, b11*cpu*cpu, b22*mem*mem, b33*pindex*pindex]
                
    w = sum(equation)

    return w

#Pickle dictionary for use in svm
def store_data(data, filename):
    
    pickle.dump(data, open( filename, "wb" ))
    print( "Wrote file to", filename )
    
def scale_data(input):

    minimum = min(input)
    range = max(input) - min(input)
    temp = [ (item - minimum) / range for item in input ]
        
    return temp

# SVM Data Preprocess
def svm_preprocess(x, y=None):
    
    # Normalize features between 0 and 1
    feature_sets = list(zip(*x))
    X = [ scale_data(input) for input in feature_sets ]
    X = list(zip(*X))
    
    # For training
    if y is not None:
        # Bin labels
        nbins = 10
        Y, bins = bin_stuff(y, nbins)
        return X, Y
    
    return X

# Bin time into specified number of bins
def bin_stuff(stuff, nbins):

    # Quantized binning
    pandas_object = pandas.qcut(stuff, nbins)
    codes = pandas_object.codes # Integer code corresponding to each bin
    bins = pandas_object.categories # Actual bin ranges
    bins = [ [bin.left, bin.right] for bin in bins ]

    # Equidistant binning
    #hist, bin_edges = np.histogram(stuff, bins=nbins)
    # Create list of bins
    #bins = [ [bin_edges[i], bin_edges[i+1]] for i in range(0, len(bin_edges)-1) ]
    # Classify stuff into bins
    #codes = list()
    #for thing in stuff:
    #    for x in range(0, len(bins)):
    #        if bins[x][0] <= thing <= bins[x][1]:
    #            codes.append(x)
    #            break
    
    return codes, bins
    
# SVM training
def train_svm(x, y):

    Y = y
    X = x
    
    #Shuffle dataset
    combined = list(zip(X, Y))
    random.shuffle(combined)
    X, Y = zip(*combined)
    
    #Train
    print( "Training SVM..." )
    clf = svm.SVC(kernel='rbf', cache_size=2048)
    dataset_size = len(Y)
    train_size = int(dataset_size*0.8)
    train_size = 30000
    clf.fit(X[0:train_size], Y[0:train_size])

    #Predict
    eval_size = dataset_size - train_size
    y_pred = clf.predict(X[train_size:])
    y_true = Y[train_size:]

    print("Accuracy:", accuracy_score(y_true, y_pred))

    store = input("Store model?(y/n): ")
    if store == "y":
        store_data(clf, "svm.p")
        
def supportvm(mem, cpu, pindex, usr):
    global svm_model, ranges
    
    if svm_model is None:
        exit("Please train svm model first!")
    
    # Reshaped for svm_model's pleasure
    data = [cpu, mem, pindex, usr]
    prediction = svm_model.predict([data])[0]
    
    # Turn class into actual value
    result = classify_bin(prediction, ranges)
    
    return result

# Returns median value of bin for clazz
def classify_bin(clazz, bins):

    bin = bins[clazz]
    value = (bin[1]-bin[0]) / 2 + bin[0]

    return value

    
### Module set-up ###
# Check for svm model
svm_file = "svm.p"
if os.path.isfile(svm_file):
    svm_model = pickle.load(open(svm_file, "rb"))
else:
    print("Missing svm model \"svm.p\"") # SVM needs to be trained and pickled
    svm_model = None

    
if __name__ == "__main__":

    ### Train SVM ###
    import swf
    
    # Get data and normalize
    data = list(zip(swf.cpu, swf.mem, swf.pindex, swf.usr))
    # Train
    train_svm(*svm_preprocess(data, swf.wall_time))
    
elif svm_model is not None:
    ### TODO: Setup class for svm with nclasses and class ranges ###
    # SVM Model input info
    nclasses = len(svm_model.classes_)
    import swf
    _, ranges = bin_stuff(swf.wall_time, nclasses)