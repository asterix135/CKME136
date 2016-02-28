"""
Download images to hard drive for easier processing
Standardizes size to 400 x 400; jpeg format
"""

import PIL
from PIL import Image
from io import BytesIO
import requests
from Python_code import sql_connect as mysql
import pandas as pd
import matplotlib.pyplot as plt
import os
import platform

if platform.platform[:5] == 'Linux':
    PATH = '/home/ec2-user/images/'
else:
    PATH = '/Volumes/NeuralNet/images/'
# PATH = ''
TESTING = False


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


def write_size(tweet_id, width, height):
    """
    Writes image size to MySQL
    :param tweet_id:
    :param width:
    :param height:
    :return:
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'INSERT INTO Image_sizes (tweet_id, width, height, pixels) ' \
              'VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (tweet_id, width, height, width * height))
        connection.commit()
        connection.close()


def fetch_image(url, tweet_id, path, stats_df):
    """
    Collects image from URL, resizes to 400x400 and saves to local drive
    :param url: image url
    :param tweet_id: integer - will become file name
    :param path: where file is to be saved
    :param stats_df: data frame with original size data
    :return stats_df: data frame with updated size data
    """
    try:
        response = requests.get(url)
        if response.status_code == 404 or response.status_code == 403:
            remove_bad_image(tweet_id)
        else:
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            img_stats = {'width': width, 'height': height,
                         'pixels': width * height}
            stats_df = stats_df.append(img_stats, ignore_index=True)
            write_size(tweet_id, width, height)
            img = img.resize((400, 400), PIL.Image.ANTIALIAS)
            filename = path + str(tweet_id) + '.jpg'
            img.save(filename)
    except Exception as err:
        print('Error on tweet id: ' + str(tweet_id))
        print(err)
    return stats_df


def load_tweet_list():
    """
    Loads all tweets from MySQL, returns as list of dictionaries
    :return tweet_list: list of dictionaries
    """
    # open database connection
    connection = mysql.connect()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, image_url FROM Original_tweets "
              # "WHERE tweet_id <= 693431781333278720 " \
              # "AND tweet_id > 692068905158770689"
              # To get early: tweet_id <= 693431781333278720
        if TESTING:
            sql += ' LIMIT 50'
        cursor.execute(sql)
        tweet_list = cursor.fetchall()
    connection.close()
    return tweet_list


def plot_histogram(df, col_name):
    fig, ax = plt.subplots()
    df.hist(col_name, ax=ax)
    fig.savefig(col_name + '_histogram.png')


def fetch_all_images(path):
    """
    Main executing function
    Loads all images from database, loads, resizes & frames
    Maintains df with sizes
    prints histograms of size data
    :param path:
    :return:
    """
    start_disk_space = (os.statvfs(path).f_bavail *
                        os.statvfs(path).f_frsize) / 1024
    tweet_list = load_tweet_list()
    image_stats = pd.DataFrame(columns=('width', 'height', 'pixels'))
    for tweet in tweet_list:
        image_stats = fetch_image(tweet['image_url'],
                                  tweet['tweet_id'], path, image_stats)
        if (len(image_stats) % 5000 == 0):
            disk_avail = (os.statvfs(path).f_bavail *
                          os.statvfs(path).f_frsize) / 1024
            avg_img_size = (start_disk_space - disk_avail) / len(image_stats)
            imgs_to_go = len(tweet_list) - len(image_stats)
            if disk_avail/imgs_to_go < avg_img_size:
                input('May run out of space:  Press Enter to continue')

    # Save size histograms
    plot_histogram(image_stats, 'height')
    plot_histogram(image_stats, 'width')

    # Print Stats
    print('\nAverage original:')
    print(image_stats.mean())
    print('\nStd Dev original:')
    print(image_stats.std())


if __name__ == '__main__':
    path = PATH
    fetch_all_images(path)
