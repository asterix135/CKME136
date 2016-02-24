"""
Logistics Regression Analysis of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.linear_model import logistic
import numpy as np
import pandas as pd
import time

data, labels = prep.get_data(500)

# split test & train sets
np.random.seed(2322016)
is_train = np.random.uniform(0, 1, len(data)) <= 0.7
train_x, train_y = data[is_train], labels[is_train]
test_x, test_y = data[is_train==False], labels[is_train==False]