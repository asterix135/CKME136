"""
Support Vector Machine Classifier of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import time

data, labels = prep.get_data(500)

# split test & train sets
np.random.seed(2722016)
is_train = np.random.uniform(0, 1, len(data)) <= 0.7
train_x, train_y = data[is_train], labels[is_train]
test_x, test_y = data[is_train == False], labels[is_train == False]


pca = RandomizedPCA(n_components=10)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)

print('starting logit')

start_time = time.time()
model = LogisticRegression(multi_class='multinomial')
model.fit(train_x, train_y)
print(pd.crosstab(test_y, model.predict(test_x), rownames=['Actual'],
                  colnames=['Predicted']))
print('processing time' + str(time.time() - start_time))
