"""
Preprocess images for machine learning algos
http://blog.yhat.com/posts/image-classification-in-Python.html
"""
from PIL import Image
import numpy as np
from sklearn.decomposition import RandomizedPCA
import matplotlib.pyplot as plt
import pandas as pd


SIZE = (400, 400)
TESTING = True
IMAGE_DIR = '/Volumes/NeuralNet/images/'


def img_to_flat_matrix(filename):
    """
    Loads image, resizes if necessary, and turns into a 1D Numpy array
    :param filename: including path
    :return: 1D Numpy array of RGB data
    """
    img = Image.open(filename)
    if img.size != SIZE:
        img = img.resize(SIZE, Image.ANTIALIAS)
    img = np.array(img.getdata())
    img_size = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, img_size)
    return img_wide[0]


def visualize_data(data, labels):
    pca = RandomizedPCA(n_components=2)
    reshaped = pca.fit_transform(data)
    df = pd.DataFrame({'x': reshaped[:,0], 'y': reshaped[:,1],
                       'label': np.where(labels==1, 'Positive', 'Negative')})
    colors = ['yellow', 'blue']
    for label, color in zip(df['label'].unique(), colors):
        mask = df['label'] == label
        plt.scatter(df[mask]['x'], df[mask]['y'], c=color, label = label)
    plt.legend()
    plt.title('PCA Decomposition of Image Data')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.show()
    # plt.savefig('PCA_plot.png')




def get_data():
    """
    put data into Numpy array
    put category data into list
    requires Database pull
    :return:
    """
    pass


def test():
    data = []
    sentiments = np.array([-1] * 10 + [1] * 10)
    image_list = [691363804903559168, 691363809072648192, 691363947493007360,
                  691363989423575040, 691364035585912832, 691364060726579201,
                  691364178184048640, 691364241085829120, 691364333364875264,
                  691364580853977088,
                  691363813279531008, 691363838449573889, 691363842635464706,
                  691364014614519808, 691364060751745024, 691364169786990592,
                  691364186593595397, 691364236908445696, 691364316600274944,
                  691364392093364224]
    for image in image_list:
        image = IMAGE_DIR + str(image) + '.jpg'
        img = img_to_flat_matrix(image)
        data.append(img)
    data = np.array(data)
    return data, sentiments


def main():
    if TESTING:
        data, labels = test()
    else:
        return
    visualize_data(data, labels)


if __name__ == '__main__':
    main()
