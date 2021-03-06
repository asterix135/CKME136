"""
Preprocess images for theano algos
http://blog.yhat.com/posts/image-classification-in-Python.html
"""
from PIL import Image
import numpy as np
from sklearn.decomposition import RandomizedPCA
import matplotlib.pyplot as plt
import pandas as pd
from Python_code import sql_connect as mysql
import platform


SIZE = (400, 400)
TESTING = False
if platform.platform()[:5] == 'Linux':
    IMAGE_DIR = '/home/ec2-user/images/'
else:
    IMAGE_DIR = '/Volumes/NeuralNet/images/'


def img_to_3d_matrix(filename, size):
    """
    Loads image, resizes if necessary, and turns into a 4D Numpy array
    :param filename: including path
    :return: 1D Numpy array of RGB data
    """
    img = Image.open(filename).convert('RGB')
    if img.size != size:
        img = img.resize(size, Image.ANTIALIAS)
    img = np.array(img.getdata()).reshape(size[0], size[1], 3)
    return img


def visualize_data(data, labels):
    pca = RandomizedPCA(n_components=2)
    reshaped = pca.fit_transform(data)
    df = pd.DataFrame({'x': reshaped[:,0], 'y': reshaped[:, 1],
                       'label': np.where(labels == 1, 'Positive',
                                         np.where(labels == 0, 'Neutral',
                                                  'Negative'))})
    colors = ['yellow', 'red', 'blue']
    for label, color in zip(df['label'].unique(), colors):
        mask = df['label'] == label
        plt.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)
    plt.legend()
    plt.title('PCA Decomposition of Image Data')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.show()
    # plt.savefig('PCA_plot.png')


def get_crowdflower(class_count=1000,
                    image_path='/Volumes/NeuralNet/crowdflower_images/',
                    size=(231,231)):
    data = []
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = '(SELECT image_id, sentiment FROM Crowdflower ' \
              'WHERE unclear_sentiment = 0 AND SENTIMENT = 1 ' \
              'LIMIT ' + str(class_count) + ') ' \
              'UNION ALL ' \
              '(SELECT image_id, sentiment FROM Crowdflower ' \
              'WHERE unclear_sentiment = 0 AND SENTIMENT = -1 ' \
              'LIMIT ' + str(class_count) + ') '
        cursor.execute(sql)
        results = pd.DataFrame(cursor.fetchall())
    connection.close()

    for image in results['image_id']:
        image = image_path + str(image) + '.jpg'
        img = img_to_3d_matrix(image, size)
        data.append(img)
    data = np.stack(data)
    return data, np.array(results['sentiment'])


def get_data(class_count=1000, image_path=IMAGE_DIR,
             rand=True, size=(231, 231)):
    """
    put data into Numpy array
    put category data into list
    requires Database pull
    returns equal number of examples per class
    :param class_count: number of examples of each class to keep
    :param image_path: location of image files
    :param rand: Boolean whether to take random selection or just first 1st n
    """
    # 1. retreive list of images to process
    data = []
    connection = mysql.connect()
    with connection.cursor() as cursor:
        if rand:
            sql = 'SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
                  'WHERE unclear_sentiment = 0 AND tweet_sentiment = '

            # Neutral sentiment
            cursor.execute(sql + '0')
            sub_results = pd.DataFrame(cursor.fetchall())
            pct_keep = class_count / len(sub_results)
            np.random.seed(3112016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = sub_results[keep]

            # Positive sentiment
            cursor.execute(sql + '1')
            sub_results = pd.DataFrame(cursor.fetchall())
            pct_keep = class_count / len(sub_results)
            np.random.seed(11032016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = results.append(sub_results[keep])

            # Negative sentiment
            cursor.execute(sql + '-1')
            sub_results = pd.DataFrame(cursor.fetchall())
            pct_keep = class_count / len(sub_results)
            np.random.seed(1132016)
            keep = np.random.uniform(0, 1, len(sub_results)) <= pct_keep
            results = results.append(sub_results[keep])

        else:
            sql = '(SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
                  'WHERE unclear_sentiment = 0 AND tweet_sentiment = 0 ' \
                  'LIMIT ' + str(class_count) + ') ' \
                  'UNION ALL ' \
                  '(SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
                  'WHERE unclear_sentiment = 0 AND tweet_sentiment = 1 ' \
                  'LIMIT ' + str(class_count) + ') ' \
                  'UNION ALL ' \
                  '(SELECT tweet_id, tweet_sentiment FROM Original_tweets ' \
                  'WHERE unclear_sentiment = 0 AND tweet_sentiment = -1 ' \
                  'LIMIT ' + str(class_count) + ')'
            cursor.execute(sql)
            results = pd.DataFrame(cursor.fetchall())
    connection.close()


    for image in results['tweet_id']:
        image = image_path + str(image) + '.jpg'
        img = img_to_3d_matrix(image, size)
        data.append(img)
    data = np.stack(data)
    return data, np.array(results['tweet_sentiment'])


def test():
    """
    Small sample data set for testing
    :return: numpy array of pixel data, numpy array of sentiment values
    """
    data = []
    sentiments = np.array([-1] * 10 + [1] * 10 + [0] * 10)
    image_list = [691363804903559168, 691363809072648192, 691363947493007360,
                  691363989423575040, 691364035585912832, 691364060726579201,
                  691364178184048640, 691364241085829120, 691364333364875264,
                  691364580853977088,
                  691363813279531008, 691363838449573889, 691363842635464706,
                  691364014614519808, 691364060751745024, 691364169786990592,
                  691364186593595397, 691364236908445696, 691364316600274944,
                  691364392093364224,
                  691363767133851648, 691363779729182720, 691363779737681921,
                  691363809076711424, 691363813292122113, 691363825845682176,
                  691363851019927553, 691363851028320256, 691363863615270912,
                  691363867788759040]
    for image in image_list:
        image = IMAGE_DIR + str(image) + '.jpg'
        img = img_to_3d_matrix(image, (231, 231))
        data.append(img)
    data = np.array(data)

    return data, sentiments


def main(visualize=True):
    if TESTING:
        data, labels = test()
    else:
        data, labels = get_data(100)
        # data, labels = get_crowdflower()
        print(len(data))
        print(len(labels))
        print(data)
        print(labels)
    if visualize:
        visualize_data(data, labels)


if __name__ == '__main__':
    main(False)
