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


def get_size(tweet):
    # image = Image.open(filepath)
    try:
        response = requests.get(tweet['image_url'])
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        pixels = width * height
        return {'width': width, 'height': height, 'pixels': pixels}
    except:
        remove_bad_image(tweet['tweet_id'])
        return False


def load_tweet_list():
    # open database connection
    connection = mysql.connect()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, image_url " \
              "FROM Original_tweets"
        if TESTING:
            sql = sql + ' LIMIT 100'
        cursor.execute(sql)
        tweet_list = cursor.fetchall()
    connection.close()
    return tweet_list


def remove_bad_image(tweet_id):
    """
    Removes record from MySQL database
    :param tweet_id: id for tweet to remove
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'DELETE FROM Original_tweets WHERE tweet_id = %s'
        cursor.execute(sql, tweet_id)
    connection.commit()
    connection.close()


def calculate_image_stats():
    tweet_list = load_tweet_list()
    image_stats = pd.DataFrame(columns=('width', 'height', 'pixels'))
    tweet_idx = 0
    old_mean = 10e10
    converge_threshhold = 0.001
    converged = False
    start_idx = 0
    while not converged:
        for i in range(start_idx + 50):
            image_size = get_size(tweet_list[tweet_idx])
            if image_size:
                image_stats = image_stats.append(image_size, ignore_index=True)
        new_mean = image_stats.mean()['pixels']
        if abs(new_mean - old_mean)/old_mean < converge_threshhold:
            converged = True
        else:
            start_idx += 50
            if start_idx + 50 < len(image_stats):
                converged = True
    return image_stats.mean()


def old_calculate_image_stats():
    fail_list = []
    tweet_list = load_tweet_list()
    image_stats = pd.DataFrame(columns=('width', 'height'))
    for tweet_idx in range(len(tweet_list)):
        image_size = get_size(tweet_list[tweet_idx], fail_list)
        if image_size:
            image_stats = image_stats.append(image_size, ignore_index=True)
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
