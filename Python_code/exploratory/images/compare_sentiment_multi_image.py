"""
Tests to see how sentiment ratings compare on images that appear
numerous times
"""

import os
from Python_code import sql_connect as mysql
from PIL import Image
import math
import pandas as pd

def get_unique_repeats():
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT DISTINCT primary_tweet, ' \
              'FROM Duplicate_images'
        cursor.execute(sql)
        repeat_df = pd.DataFrame(cursor.fetchall())
    connection.close()
    return repeat_df


def get_all_same(tweet_id):
    connection = mysql.connect()
    with connection.cursor as cursor:
        sql = 'SELECT unclear_sentiment, tweet_sentiment ' \
              'FROM Duplicate_images ' \
              'WHERE primary_tweet = %s'
        cursor.execute(sql, tweet_id)
        dupes = pd.DataFrame(cursor.fetchall())

        sql = 'SELECT unclear_sentiment, tweet_sentiment ' \
              'FROM Original_tweets ' \
              'WHERE tweet_id = %s'
        cursor.execute(sql, tweet_id)
        dupes.extend(cursor.fetchall())

    connection.close()
    return dupes



def compare_sentiments():
    repeat_list = get_unique_repeats()
    for i in range(len(repeat_list)):
        curr_set = get_all_same(int(repeat_list))
        curr_set['']
