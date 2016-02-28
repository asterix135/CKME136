"""
Logistics Regression Analysis of image data

2 tests - against twitter data and against polarity list
"""

from Python_code.classifiers.preprocessing import img_preprocess as prep
from sklearn.decomposition import RandomizedPCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
import pandas as pd
import time

prep.SIZE = (250, 250)
data, labels = prep.get_data(500)

# split test & train sets
train_x, test_x, train_y, test_y = train_test_split(
    data, labels, test_size=0.3, random_state=2722016)

start_time = time.time()

pca = RandomizedPCA(n_components=100000)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)

print('starting logit')

model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit(train_x, train_y)
pred_y = model.predict(test_x)
print(pd.crosstab(test_y, pred_y, rownames=['Actual'],
                  colnames=['Predicted']))
print('\nAccuracy: ' + str(accuracy_score(test_y, pred_y)))
print('\nprocessing time: ' + str(time.time() - start_time))
