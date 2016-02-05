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


TESTING = True

def is_valid_image(url):
    """
    Returns boolean as to whether image url is still valid
    :param url: string
    :return: boolean
    """
    try:
        urllib.urlopen(url)
        valid_url = True
    except:
        valid_url = False
    return valid_url


def get_size(tweet, fail_list):
    # image = Image.open(filepath)
    try:
        response = requests.get(tweet['image_url'])
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        print(width, height)
    except:
        fail_list.append(tweet['tweet_id'])


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
        url_list = cursor.fetchall()
    connection.close()
    return url_list


def calculate_image_stats():
    fail_list = []
    tweet_list = load_tweet_list()



if __name__ == '__main__':
    pass
