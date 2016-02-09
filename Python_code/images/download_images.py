"""
Download images to hard drive for easier processing
"""

import PIL
from PIL import Image
from io import BytesIO
import requests
from Python_code import sql_connect as mysql
import sys

PATH = '/Volumes/NeuralNet/Images/'
# PATH = ''
TESTING = True


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


def fetch_image(url, tweet_id, path):
    """
    Collects image from URL, resizes to 400x400 and saves to local drive
    :param url:
    :param tweet_id:
    :param path:
    :return:
    """
    try:
        response = requests.get(url)
        if response.status_code == 404:
            remove_bad_image(tweet_id)
        else:
            img = Image.open(BytesIO(response.content))
            img = img.resize((400, 400), PIL.Image.ANTIALIAS)
            filename = path + str(tweet_id) + '.jpg'
            img.save(filename)
    except Exception as err:
        print('Error on tweet id: ' + str(tweet_id) + '. Execution halted.')
        sys.exit(err)


def load_tweet_list():
    # open database connection
    connection = mysql.connect()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, image_url FROM Original_tweets"
        if TESTING:
            sql += ' LIMIT 100'
        cursor.execute(sql)
        tweet_list = cursor.fetchall()
    connection.close()
    return tweet_list


def fetch_all_images(path):
    tweet_list = load_tweet_list()
    for tweet in tweet_list:
        fetch_image(tweet['image_url'], tweet['tweet_id'], path)

        # TODO: Something about free size on disk maybe
        # see: http://stackoverflow.com/questions/787776/find-free-disk-space-in-python-on-os-x


if __name__ == '__main__':
    path = PATH
    fetch_all_images(path)
