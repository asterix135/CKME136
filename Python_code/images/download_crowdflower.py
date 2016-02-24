"""
Puts crowdflower data in MySQL and downloads transformed images
"""

import os
from Python_code import sql_connect as mysql
import pandas as pd
from PIL import Image
from io import BytesIO
import requests


FILE_PATH = '/Volumes/NeuralNet/crowdflower_images/'

def download_image(url, image_id):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((400, 400), Image.ANTIALIAS)
    filename = FILE_PATH + str(image_id) + '.jpg'
    img.save(filename)


def add_to_db(image_id, sentiment, unclear_sentiment, image_url):
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'INSERT INTO '


curr_dir = os.getcwd()
os.chdir(curr_dir[:-18] + 'Data/test_data')

cf_images = pd.read_csv('Sentiment-Polarity-DFE.csv')



for row in range(5):
    image_id = int(cf_images.at[row,'_unit_id'])
    sentiment = 1 if 'ositive' in \
                     cf_images.at[row, 'which_of_these_sentiment_scores_does_the_above_image_fit_into_best'] \
        else -1
    unclear_sentiment = 0 if \
        cf_images.at[row, 'which_of_these_sentiment_scores_does_the_above_image_fit_into_best:confidence'] > .66 \
        else 1
    image_url = cf_images.at[row, 'imageurl']
    # download_image(image_url, image_id)
    print(image_id, sentiment, unclear_sentiment, image_url)
