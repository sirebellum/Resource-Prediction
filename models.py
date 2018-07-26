from __future__ import print_function
import os
from sklearn import svm
from sklearn.metrics import accuracy_score
import numpy as np
import random
import pickle

# QRSM model from paper
def qrsm(mem, cpu, pindex):

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

# SVM training
def train_svm(x, y):

    # Bin labels
    Y, bins = swf.bin_stuff(y, 10)
    X = x

    #Shuffle dataset
    combined = list(zip(X, Y))
    random.shuffle(combined)
    X, Y = zip(*combined)
    
    #Train
    print( "Training SVM..." )
    clf = svm.SVC(kernel='linear', cache_size=2048)
    dataset_size = len(Y)
    train_size = int(dataset_size*0.8)
    clf.fit(X[0:50000], Y[0:50000])

    #Predict
    eval_size = dataset_size - train_size
    y_pred = clf.predict(X[train_size:])
    y_true = Y[train_size:]

    print("Accuracy:", accuracy_score(y_true, y_pred))

    store = input("Store model?(y/n): ")
    if raw_input == "y":
        store_data(clf, "svm.p")
        
def supportvm(mem, cpu, pindex):
    
    global svm_model
    if svm_model is None:
        exit("Please train svm model first!")
        
    prediction = svm_model.predict(zip(mem, cpu, pindex))
    
    return prediction

    
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
    
    # Get data
    cpureq = swf.cpureq
    memreq = swf.memreq
    pindexreq = swf.pindexreq
    wall_time = swf.wall_time
    
    data = list(zip(cpureq, memreq, pindexreq))
    train_svm(data, wall_time)

