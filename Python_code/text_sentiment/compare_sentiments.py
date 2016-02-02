"""
Compare various methods to ascribe sentiment to tweets
With aim to figuring out how much they disagree and figuring out what to
do with disagreement
1) read in all tweets (currently list of dictionaries - dunno if best)
2) Double loop:
    Sentiment methods
        Tweets
            Calculate sentiment
3) For each tweet calculate degree agreement
4) Calculate which method has highest correlation with other methods
5) Dump ambiguous tweets
6) Assign sentiment value based on???
"""

import pymysql.cursors
import numpy as np
from Python_code import sql_vals
from Python_code.text_sentiment.vader import vader



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
    :return original_tweets: list of dictionaries
    """
    # open database connection
    connection = mysql_connection()

    # pull record id, username and image url from all downloaded tweets
    with connection.cursor() as cursor:
        sql = "SELECT tweet_id, username, text FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()
    return original_tweets


def calculate_sentiments(tweet_list):
    """
    Loops through various
    :param tweet_list:
    :return:
    """
