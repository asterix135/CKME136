"""
Random Classifier of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
import pandas as pd
import time
from sklearn.ensemble import RandomForestClassifier


prep.SIZE = (231, 231)
data, labels = prep.get_data(250)

# split test & train sets
train_x, test_x, train_y, test_y = train_test_split(
    data, labels, test_size=0.3, random_state=28022016)

# pca = RandomizedPCA(n_components=100, whiten=False)
# train_x = pca.fit_transform(train_x)
# test_x = pca.transform(test_x)

print('starting rf')

start_time = time.time()


model = RandomForestClassifier()
model.fit(train_x, train_y)

pred_y = model.predict(test_x)

print(pd.crosstab(test_y, model.predict(test_x), rownames=['Actual'],
                  colnames=['Predicted']))

print('\nAccuracy: ' + str(accuracy_score(test_y, pred_y)))

print('processing time' + str(time.time() - start_time))
