"""
Get sizes of images from urls
http://stackoverflow.com/questions/1507084/how-to-check-dimensions-of-all-images-in-a-directory-using-python
http://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
"""

# import urllib.request as urllib
from PIL import Image
from io import BytesIO
import requests
from Python_code import sql_connect as mysql
import pandas as pd
import matplotlib.pyplot as plt


TESTING = True


def get_size(tweet, fail_list):
    # image = Image.open(filepath)
    try:
        response = requests.get(tweet['image_url'])
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        pixels = width * height
        return {'width': width, 'height': height, 'pixels': pixels}
    except:
        fail_list.append(tweet['tweet_id'])
        return False


def load_tweet_list():
    # open database connection
    connection = mysql.connect()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, image_url " \
              "FROM Original_tweets"
        if TESTING:
            sql = sql + ' LIMIT 50'
        cursor.execute(sql)
        tweet_list = cursor.fetchall()
    connection.close()
    return tweet_list


def remove_bad_images(fail_list):
    """
    Loops through fail list and removes from MySQL database
    :param fail_list: list of tweet_id's for invalid images
    """
    connection = mysql.connect()
    for tweet_id in fail_list:
        with connection.cursor() as cursor:
            sql = 'DELETE FROM Original_tweets WHERE tweet_id = %s'
            cursor.execute(sql, tweet_id)
    connection.commit()
    connection.close()


def test_calculate_image_stats():
    fail_list = []
    tweet_list = load_tweet_list()
    image_stats = pd.DataFrame(columns=('width', 'height', 'pixels'))
    tweet_idx = 0
    converged = False
    while not converged:
        image_size = get_size(tweet_list[tweet_idx], fail_list)
        if image_size:
            image_stats = image_stats.append(image_size, ignore_index=True)




def calculate_image_stats():
    fail_list = []
    tweet_list = load_tweet_list()
    image_stats = pd.DataFrame(columns=('width', 'height'))
    for tweet_idx in range(len(tweet_list)):
        image_size = get_size(tweet_list[tweet_idx], fail_list)
        if image_size:
            image_stats = image_stats.append(image_size, ignore_index=True)
        if len(fail_list) > 50:
            remove_bad_images(fail_list)
            print(str(tweet_list[tweet_idx]))
            fail_list = []
    print(len(image_stats))
    print(len(fail_list))
    print(image_stats.mode(axis=0))
    print()
    print(image_stats.mean())
    print()
    print(image_stats.median())
    print()
    print(image_stats.max())
    print()
    print(image_stats.min())


if __name__ == '__main__':
    calculate_image_stats()
