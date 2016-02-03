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
import pandas as pd
from Python_code import sql_vals
from Python_code.text_sentiment.vader import vader
from Python_code.text_sentiment import split_hashtag as sh



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
        sql = "SELECT tweet_id, username, text, processed_tweet " \
              "FROM Original_tweets"
        cursor.execute(sql)
        original_tweets = cursor.fetchall()
    connection.close()
    all_tweets = pd.DataFrame(original_tweets)
    return all_tweets


def calculate_vader(tweet_list):
    """
    Calculate sentimenet using VADER code
    :param tweet_list:
    :return:
    """
    pass


def calculate_afinn(tweet):
    """
    calculate sentiment using AFINN lexicon
    :param tweet:
    :return:
    """
    pass


def calculate_hu_lui(tweet_list):
    pass


def calculate_sentic(tweet_list):
    pass


def figure_tweet_stats(result_matrix):
    pass


def update_database(result_matrix):
    """
    Updates database to indicate tweet sentiment and whether certainty
    tweet_sentiment: -1 = negative, 0 = neutral, 1 = positive
    unclear_sentiment: 0 = clear, 1 = unclear
    :param result_matrix:
    :return:
    """
    pass


def calculate_sentiments():
    """
    Loops through various
    :param tweet_list:
    :return:
    """
    # 1. get tweet data into a dataframe
    tweet_df = pull_all_original_tweets()
    # 2. Calculate vader sentiment
    # tweet_df['vader'] = tweet_df.appy(lambda x: calculate_vader)
    tweet_df['vader'] = tweet_df['text'].apply(calculate_vader)


if __name__ == '__main__':
    # foo = pull_all_original_tweets()
    # print(type(foo.at[0,'text']))
    calculate_sentiments()