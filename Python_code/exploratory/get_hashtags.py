"""
Get hashtags & counts from corpus
"""

import pymysql.cursors
from Python_code import sql_vals
import pandas as pd
import operator


def mysql_connection():
    """
    helper function to connect to database
    :return: mysql connection
    """
    connection = pymysql.connect(host=sql_vals.host,
                                 password=sql_vals.password,
                                 port=sql_vals.port,
                                 user=sql_vals.user,
                                 db=sql_vals.db,
                                 cursorclass=pymysql.cursors.DictCursor,
                                 charset='utf8mb4')
    return connection


def pull_all_original_tweets():
    """
    Hardcoded SQL query to pull all originally selected tweets
    :return original_tweets: pandas dataframe of original tweets
    """
    # open database connection
    connection = mysql_connection()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT text FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()
    return original_tweets


def get_hashtags():
    """
    Get counts of hashtags in original corpus
    :param tweet_df: pandas datafreme
    :return:
    """
    tweet_df = pull_all_original_tweets()
    all_hashtags = {}
    for tweet in tweet_df:
        tokens = tweet['text'].split()
        for token in tokens:
            if token[0] == '#' and len(token) > 1:
                hashtag = token[1:].lower()
                try:
                    all_hashtags[hashtag] += 1
                except:
                    all_hashtags[hashtag] = 1
    return all_hashtags

if __name__ == '__main__':
    hashtags = get_hashtags()
    sorted_hashtags = sorted(hashtags.items(), key=operator.itemgetter(1), reverse = True)
    print(sorted_hashtags[0:100])
