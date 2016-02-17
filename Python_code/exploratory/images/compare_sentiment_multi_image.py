"""
Tests to see how sentiment ratings compare on images that appear
numerous times
"""

import os
from Python_code import sql_connect as mysql
from PIL import Image
import math
import pandas as pd

def get_repeats():
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT DISTINCT primary_tweet, ' \
              'FROM Duplicate_images'
        cursor.execute(sql)
        repeat_df = pd.DataFrame(cursor.fetchall())
    connection.close()
    return repeat_df


def compare_sentiments(repeat_df):

    for i in range(len(repeat_df)):
        pass