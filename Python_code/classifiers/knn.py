"""
KNN Analysis of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd


data, labels = prep.get_data(100)

# split test & train sets
np.random.seed(2222016)
is_train = np.random.uniform(0, 1, len(data)) <= 0.7
train_x, train_y = data[is_train], labels[is_train]
test_x, test_y = data[is_train==False], labels[is_train==False]

print(type(data))
print(type(train_x))
print(type(labels))
print(type(train_y))
print(len(train_x), len(train_y))
print(len(test_x), len(test_y))
print()
print(train_x)
print()
print(test_x)

pca = RandomizedPCA(n_components=15)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)

knn = KNeighborsClassifier()
knn.fit(train_x, train_y)

pd.crosstab(test_y, knn.predict(test_x), rownames=['Actual'],
            colnames=['Predicted'])


