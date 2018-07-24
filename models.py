from __future__ import print_function
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

if __name__ == "__main__":
    filename = "data_processing/data.p"
    keypoints = pickle.load(open(filename, "rb"))

    #Create dataset for svm
    X = list()
    Y = list()
    for clas in keypoints:
      for instance in keypoints[clas]:
        Y.append(clas)
        X.append(np.nan_to_num(np.concatenate((instance[0], instance[1]))))

    #Shuffle dataset
    combined = list(zip(X, Y))
    random.shuffle(combined)
    X[:], Y[:] = zip(*combined)

    #Train
    clf = svm.SVC(kernel='linear')
    dataset_size = len(Y)
    train_size = int(dataset_size*0.8)
    clf.fit(X[0:train_size], Y[0:train_size])

    #Predict
    eval_size = dataset_size - train_size
    y_pred = clf.predict(X[train_size:])
    y_true = Y[train_size:]

    print("Accuracy:", accuracy_score(y_true, y_pred))

    store = raw_input("Store model?(y/n): ")
    if store == "y":
        store_data(clf, "svm.p")