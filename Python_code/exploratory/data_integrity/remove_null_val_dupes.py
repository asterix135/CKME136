"""
Clean up database by removing records in duplicate_images with a null value
for unclear_sentiment

Also delete image files
"""

import os
from Python_code import sql_connect as mysql

connection = mysql.connect()
with connection.cursor() as cursor:
    sql = 'SELECT tweet_id FROM Duplicate_images ' \
          'WHERE unclear_sentiment IS NULL'
    cursor.execute(sql)
    null_records = [x['tweet_id'] for x in cursor.fetchall()]

dupe_path = '/Volumes/NeuralNet/dupe_images/'

for tweet in null_records:
    os.remove(dupe_path + str(tweet) + '.jpg')
with connection.cursor() as cursor:
    sql = 'DELETE FROM Duplicate_images WHERE unclear_sentiment IS NULL'
    cursor.execute(sql)

connection.commit()
connection.close()
