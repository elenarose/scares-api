# Title     : TODO
# Objective : TODO
# Created by: satwikkamarthi
# Created on: 10/4/20

import pandas as pd
# from sklearn.cross_decomposition import CCA
# from sklearn.datasets import make_multilabel_classification
# from sklearn.metrics import confusion_matrix
# from sklearn.svm import SVC
# import numpy as np

################################################################################
################################################################################

#Import data and create training and test data and labels

################################################################################
################################################################################
stress_drivers = pd.read_csv('./src/svm/scare_features_10212020.csv')

data = stress_drivers.drop(['Stimuli'], axis =1).drop(['Filename'], axis = 1).drop(['Subject'], axis = 1).values
target = stress_drivers['Stimuli'].values
from sklearn.model_selection import train_test_split

#80% training 20% test
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state = 0)
################################################################################
################################################################################
################################################################################
################################################################################









################################################################################
################################################################################

#fit the classifier to the training data, and check test data for prediction

################################################################################
################################################################################

from sklearn import svm
from sklearn.multiclass import OneVsRestClassifier

#create linear Kernel classifier
classifier_rbf = OneVsRestClassifier(svm.SVC(kernel='rbf',decision_function_shape = 'ovr')).fit(X_train, y_train)
classifier_linear = OneVsRestClassifier(svm.SVC(kernel='linear',decision_function_shape = 'ovr')).fit(X_train, y_train)
classifier_poly = OneVsRestClassifier(svm.SVC(kernel='poly',decision_function_shape = 'ovr')).fit(X_train, y_train)
classifier_sigmoid = OneVsRestClassifier(svm.SVC(kernel='sigmoid' ,decision_function_shape = 'ovr')).fit(X_train, y_train)
classifier_poly_gamma = OneVsRestClassifier(svm.SVC(kernel='poly',decision_function_shape = 'ovr', gamma='auto')).fit(X_train, y_train)

#prediction test
y_pred_rbf = classifier_rbf.predict(X_test)
y_pred_linear = classifier_linear.predict(X_test)
y_pred_poly = classifier_poly.predict(X_test)
y_pred_sigmoid = classifier_sigmoid.predict(X_test)
y_pred_poly_gamma = classifier_poly_gamma.predict(X_test)
################################################################################
################################################################################
################################################################################
################################################################################









################################################################################
################################################################################

#Predict new random data

################################################################################
################################################################################

#X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=1)
def get_prediction(data):
    ynew = classifier_linear.predict(data)
    for i in range(len(ynew)):
        return ynew[i]
################################################################################
################################################################################
################################################################################
################################################################################









################################################################################
################################################################################

#Some Analysis

################################################################################
################################################################################
#print("Precision:",metrics.precision_score(y_test, y_pred, average='micro'))
#print("Precision:",metrics.precision_score(y_test, y_pred, average='weighted'))
#print("Precision:",metrics.precision_score(y_test, y_pred, average='samples'))
#print("Precision:",metrics.precision_score(y_test, y_pred, average='weighted', zero_division=1))
#print("Precision:",metrics.precision_score(y_test, y_pred, average='samples'))
#print("Recall:",metrics.recall_score(y_test, y_pred, average='micro'))
#print("Recall:",metrics.recall_score(y_test, y_pred, average='weighted' , zero_division=1))
