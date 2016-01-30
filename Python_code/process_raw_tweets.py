"""
Routines to subset to english tweets that contain original image links
"""
import json
import pymysql.cursors
import Python_code.sql_vals as sql_vals
import os
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

TWEET_FILE_PATH = '/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Data/'
# TWEET_FILE_PATH = '/Users/chris/Documents/code/misc/CKME136 copy/Data/'
# TWEET_FILE_PATH = '/Volumes/NeuralNet/Data/'


def subset_tweets(tweet_file):
    """
    Extracts info from json file of twitter data, and subsets
    based on english language and presence of image url
    :param tweet_file: json file
    :return tweets: list of tweets as dictionary
    """
    tweets = []
    for line in tweet_file:
        try:
            curr_tweet = json.loads(line)
            if decide_to_include_tweet(curr_tweet):
                tweets.append(curr_tweet)
        except:
            pass
    return tweets


def decide_to_include_tweet(tweet):
    """
    helper function setting criteria as to whether to include a tweet in
    list to be processed
    :param tweet: dictionary
    :return: boolean
    """
    if 'lang' in tweet and tweet['lang'] == 'en':
        if 'text' in tweet and 'extended_entities' in tweet:
            return True
    return False


def image_is_original(tweet):
    """
    Return boolean as to whether an image is retweeted
    :param tweet: dictionary
    :return: boolean
    """
    # return 'source_user_id_str' in tweet['extended_entities']['media'][0]
    return not tweet['text'][:2] == 'RT'


def convert_twitter_date_to_datetime(twitter_created_at):
    """
    Converts twitter 'created_at' data to UTC-5 datetime format
    :param twitter_created_at:
    :return:
    """
    timestamp = mktime_tz(parsedate_tz(twitter_created_at))
    return str(datetime.fromtimestamp(timestamp))


def insert_record(connection, tweet):
    try:
        with connection.cursor() as cursor:
            # Create new record
            id = tweet['id']
            tweet_txt = tweet['text']
            tweet_url = tweet['extended_entities']['media'][0]['media_url']
            timestamp = convert_twitter_date_to_datetime(tweet['created_at'])
            username = tweet['user']['screen_name']
            sql = "INSERT INTO Original_tweets (tweet_id, username, text, image_url, created_ts) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (id, username, tweet_txt, tweet_url, timestamp))
    except:
        pass


def send_to_database(tweet_file):
    # tweet_file = open(TWEET_FILE_PATH + TWEET_FILE)
    tweet_list = subset_tweets(tweet_file)
    # tweet_file.close()

    # Open database connection
    connection = pymysql.connect(host=sql_vals.host,
                                 password=sql_vals.password,
                                 port=sql_vals.port,
                                 user=sql_vals.user,
                                 db=sql_vals.db,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8mb4')


    # save relevant data on tweets with original images
    insert_count = 0
    for tweet in tweet_list:
        if image_is_original(tweet):
            insert_record(connection, tweet)
            insert_count += 1
    connection.commit()
    print(str(insert_count) + ' records inserted\n')

    connection.close()


def process_all_tweet_files(path):
    for file in os.listdir(path):
        if file.endswith('.txt'):
            tweet_file = open(path + file)
            send_to_database(tweet_file)
            tweet_file.close()


if __name__ == '__main__':
    process_all_tweet_files(TWEET_FILE_PATH)
