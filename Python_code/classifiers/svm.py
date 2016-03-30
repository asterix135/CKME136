"""
Support Vector Machine Classifier of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cross_validation import train_test_split
import pandas as pd
import time
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC

APPLY_PCA = False
prep.SIZE = (250, 250)
data, labels = prep.get_data(1000)

# split test & train sets
train_x, test_x, train_y, test_y = train_test_split(
    data, labels, test_size=0.3, random_state=28022016)

if APPLY_PCA:
    pca = RandomizedPCA(n_components=100, whiten=False)
    train_x = pca.fit_transform(train_x)
    test_x = pca.transform(test_x)

print('starting svm')

start_time = time.time()

parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

# model = GridSearchCV(SVC(), parameters)
model = SVC(kernel='linear')
model.fit(train_x, train_y)

pred_y = model.predict(test_x)

print('\nLinear SVM results')
print('==================\n')
print('Confusion Matrix')
print('----------------')
print(pd.crosstab(test_y, model.predict(test_x), rownames=['Actual'],
                  colnames=['Predicted']))

print('\nAccuracy: ' + str(accuracy_score(test_y, pred_y)))
print()
print(classification_report(test_y, pred_y))
print()

print('processing time' + str(time.time() - start_time))

# Polynomial SVC
start_time = time.time()
model = SVC(kernel='poly')
model.fit(train_x, train_y)

pred_y = model.predict(test_x)

print('\nPolynomial SVM results')
print('======================\n')
print('Confusion Matrix')
print('----------------')
print(pd.crosstab(test_y, model.predict(test_x), rownames=['Actual'],
                  colnames=['Predicted']))

print('\nAccuracy: ' + str(accuracy_score(test_y, pred_y)))
print()
print(classification_report(test_y, pred_y))
print()

print('processing time' + str(time.time() - start_time))

# Radial Basis Function SVC
start_time = time.time()
model = SVC(kernel='rbf')
model.fit(train_x, train_y)
pred_y = model.predict(test_x)

print('\nRBF SVM results')
print('===============\n')
print('Confusion Matrix')
print('----------------')
print(pd.crosstab(test_y, model.predict(test_x), rownames=['Actual'],
                  colnames=['Predicted']))

print('\nAccuracy: ' + str(accuracy_score(test_y, pred_y)))
print()
print(classification_report(test_y, pred_y))
print()

print('processing time' + str(time.time() - start_time))

