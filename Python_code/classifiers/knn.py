"""
KNN Analysis of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
import time

start_time = time.time()
prep.SIZE = (300,300)
# data, labels = prep.get_data(2000)
cf_data, cf_labels = prep.get_crowdflower(2000)
print('load time: ' + str(time.time() - start_time))


# split test & train sets
# np.random.seed(2222016)
# is_train = np.random.uniform(0, 1, len(data)) <= 0.7
# train_x, train_y = data[is_train], labels[is_train]
# test_x, test_y = data[is_train==False], labels[is_train==False]

np.random.seed(2252016)
cf_is_train = np.random.uniform(0, 1, len(cf_data)) <= 0.7
cf_train_x, cf_train_y = cf_data[cf_is_train], cf_labels[cf_is_train]
cf_test_x, cf_test_y = cf_data[cf_is_train==False], \
                       cf_labels[cf_is_train==False]

# pca = RandomizedPCA(n_components=100, whiten=False)
# train_x = pca.fit_transform(train_x)
# test_x = pca.transform(test_x)

print('starting knn')

def run_knn(trainx, trainy, testx, testy):
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(trainx, trainy)
    pred_y = knn.predict(testx)
    print(pd.crosstab(testy, pred_y, rownames=['Actual'],
                      colnames=['Predicted']))
    print('\nAccuracy: ' + str(accuracy_score(testy, pred_y)))

start_time = time.time()
print('\nKNN on Twitter images')
# run_knn(train_x, train_y, test_x, test_y)
print('\nprocessing time: ' + str(time.time() - start_time))

# Test crowdflower against itself
start_time = time.time()
print('\n\nKNN on Crowdflower images')
run_knn(cf_train_x, cf_train_y, cf_test_x, cf_test_y)
print('\nprocessing time: ' + str(time.time() - start_time))

# Test Twitter data against Crossflower
start_time = time.time()
print('\n\nKNN: Predictions on Crowdflower from Twitter Images')
# run_knn(data, labels, cf_data, cf_labels)
# print('\nprocessing time: ' + str(time.time() - start_time))

# Test Crowdflower data against Twitter
start_time = time.time()
print('\nKNN: Predictions on Crowdflower from Twitter Images')
# run_knn(cf_data, cf_labels, data, labels)
print('\nprocessing time: ' + str(time.time() - start_time))
