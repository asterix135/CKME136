from sklearn_theano.feature_extraction import OverfeatTransformer
from sklearn_theano.utils import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report, accuracy_score, \
    confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import os
import time

from Python_code.classifiers.preprocessing import nn_preprocess as prep


CM_LABELS = ['Negative', 'Neutral', 'Positive']


def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(CM_LABELS))
    plt.xticks(tick_marks, CM_LABELS, rotation=45)
    plt.yticks(tick_marks, CM_LABELS)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


print('loading data....')
start_time = time.time()
images, labels = prep.get_data(40)
images = images.astype('float32')
train_x, test_x, train_y, test_y = train_test_split(
    images, labels, train_size=.7, random_state=20160319)
print('Total data load time:')
print('---------------------')
print(time.time() - start_time)

# Consider trying different values for output_layers
print('\nstarting nn....')
tf = OverfeatTransformer(output_layers=[-3], batch_size=None)
clf = LogisticRegression()
pipe = make_pipeline(tf, clf)
start_time = time.time()
pipe.fit(train_x, train_y)
print('Total transform time:')
print('---------------------')
print(time.time() - start_time)

print('\nstarting predictions....')
start_time = time.time()
pred_y = pipe.predict(test_x)
print('total prediction time')
print('---------------------')
print(time.time() - start_time)

print()

print(classification_report(test_y, pred_y))
print()

print("Accuracy score")
print("==============")
print(accuracy_score(test_y, pred_y))
print()

print('Confusion Matrix')
print('================')
cm = confusion_matrix(test_y, pred_y)
print(cm)

plt.figure()
plot_confusion_matrix(cm)

os.system('say "your program has finished')

plt.show()

