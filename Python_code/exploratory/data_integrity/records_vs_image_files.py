"""
Check for orphaned records in database or orphaned image files
"""

from Python_code import sql_connect as mysql
import os


connection = mysql.connect()
with connection.cursor() as cursor:
    sql = 'SELECT tweet_id FROM Original_tweets'
    cursor.execute(sql)
    orig_tweets = [x['tweet_id'] for x in cursor.fetchall()]
    sql = 'SELECT tweet_id FROM Duplicate_images'
    cursor.execute(sql)
    dupe_tweets = [x['tweet_id'] for x in cursor.fetchall()]
connection.close()

image_list = os.listdir('/Volumes/NeuralNet/images')
dupe_images = os.listdir('/Volumes/NeuralNet/dupe_images')

bad_db1 = 0
bad_db2 = 0
bad_img1 = 0
bad_img2 = 0

# for tweet in orig_tweets:
#     if str(tweet) + '.jpg' not in image_list:
#         bad_db1 += 1
# print(bad_db1, bad_db1/len(orig_tweets))
#
# for tweet in dupe_tweets:
#     if str(tweet) + '.jpg' not in dupe_images:
#         bad_db2 += 1
# print(bad_db2, bad_db2/len(dupe_tweets))

for img in image_list:
    if img.endswith('.jpg') and int(img[:-4]) not in orig_tweets:
        bad_img1 += 1
        # os.remove('/Volumes/NeuralNet/images/' + img)
print(bad_img1, bad_img1/len(image_list))

for img in dupe_images:
    if img.endswith('.jpg') and int(img[:-4]) not in dupe_tweets:
        bad_img2 += 1
        # os.remove('/Volumes/NeuralNet/dupe_images/' + img)
print(bad_img2, bad_img2/len(dupe_images))

print(bad_db1, bad_db2, bad_img1, bad_img2)
