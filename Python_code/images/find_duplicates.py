"""
Find duplicates among downloaded images
Remove duplicates and update sentiment scores based on aggregate text

Calculates a perceptual hashcode (based on difference hashing) for each
image

Compares hashes using Hamming distance

counts as duplicate if distance <= MAX_DIFF
    (MAX_DIFF is set manually, based on observation of results)
"""

import os
from Python_code import sql_connect as mysql
from PIL import Image
import math
import pandas as pd
import time
import platform

if platform.platform()[:5] == 'Linux':
    IMAGE_PATH = '/home/ec2-user/images/'
    DUPE_IMAGE_PATH = '/home/ec2-user/dupe_images'
else:
    IMAGE_PATH = '/Volumes/NeuralNet/images/'
    DUPE_IMAGE_PATH = '/Volumes/NeuralNet/dupe_images/'
# IMAGE_PATH = '/Volumes/NeuralNet/test_images/'
MAX_DIFF = 3


def get_tweet_list():
    """
    Returns a dataframe containing tweet_ids and image hashcodes for all
    recods in Original_tweets table
    :return: pd.DataFrame object
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT tweet_id, image_hash FROM Original_tweets'
        cursor.execute(sql)
        results = pd.DataFrame(cursor.fetchall())
    connection.close()
    return results


def find_matching_hash(hashcode, search_tweet_id):
    """
    Queries database to see if exactly matching hashcode exists for image
    If match exists, returns tweet_id of match
    else returns None
    :param hashcode: hashcode of image being searched on
    :param search_tweet_id: tweet_id of image being searched on
    :return: None or matching tweet_id
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT tweet_id from Original_tweets ' \
              'WHERE image_hash = %s ' \
              'AND tweet_id != %s'
        cursor.execute(sql, (hashcode, search_tweet_id))
        match = cursor.fetchone()
        if match:
            match = match['tweet_id']
    connection.close()
    return match


def hamming_distance(str1, str2):
    """
    Calculates Hamming distance between 2 strings;
    Strings must be the same length
    :param str1: 1st string
    :param str2: 2nd string
    :return: Integer
    """
    if len(str1) != len(str2):
        raise ValueError('Undefined for sequences of unequal length')
    return sum(bool(ord(ch1) - ord(ch2)) for ch1, ch2 in zip(str1, str2))


def calculate_image_hash(image, hash_size=12):
    """
    Creates a Hexidecimal hash code based on greyscale pixel difference
    :param image: PIL.Image object
    :param hash_size: pixel size of resized image; default 12
    :return: hexidecimal hash code as string
    """
    # 1. Convert to greyscale and rescale
    image = image.convert('L').resize(
            (hash_size + 1, hash_size),
            Image.ANTIALIAS,
    )

    # 2. compare adjacent pixels
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # convert boolean list to hexadecimal string
    decimal_value = 0
    hex_string = []
    just_val = math.ceil(hash_size / 4)
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % hash_size)
        if (index % hash_size) == hash_size - 1:
            hex_string.append(hex(decimal_value)[2:].rjust(just_val, '0'))
            decimal_value = 0
    return ''.join(hex_string)


def add_hash_to_sql(tweet_id, hashcode):
    """
    Updates specific record in mySQL with image hashcode
    :param tweet_id: integer
    :param hashcode: string
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'UPDATE Original_tweets ' \
              'SET image_hash = %s ' \
              'WHERE tweet_id = %s'
        cursor.execute(sql, (hashcode, tweet_id))
    connection.commit()
    connection.close()


def process_duplicate_image(match_id, dupe_id, dupe_hash):
    """
    Updates MySQL database for tweets with a duplicated image as follows:
    1. Adds duplicate tweet info to Duplicate_images table linked to matched id
    2. Updates any entries in Duplicate_images that point to moved tweet
    3. Deletes duplicate tweet record from Original_tweets table
    4. Moves duplicate image to DUPE_IMAGE_PATH
    :param match_id: tweet_id of record to keep in Original_tweets
    :param dupe_id: tweet_id of record to move to Duplicate_images
    :param dupe_hash: hashcode for record being moved
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM Original_tweets ' \
              'WHERE tweet_id = %s'
        cursor.execute(sql, int(dupe_id))
        dupe = cursor.fetchone()

        sql = 'UPDATE Duplicate_images ' \
              'SET primary_tweet = %s ' \
              'WHERE primary_tweet = %s'
        cursor.execute(sql, (int(match_id), int(dupe_id)))

        try:
            sql = 'INSERT INTO Duplicate_images ( ' \
                  'tweet_id, primary_tweet, username, text, processed_text, ' \
                  'image_url, tweet_sentiment, created_ts, image_hash, ' \
                  'unclear_sentiment) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(sql, (int(dupe['tweet_id']), int(match_id),
                                 dupe['username'], dupe['text'],
                                 dupe['processed_text'], dupe['image_url'],
                                 int(dupe['tweet_sentiment']),
                                 dupe['created_ts'], dupe_hash,
                                 int(dupe['unclear_sentiment'])))
        except Exception as err:
            print(str(err) + ' on record ' + str(dupe_id))

        sql = 'DELETE FROM Original_tweets ' \
              'WHERE tweet_id = %s'
        cursor.execute(sql, int(dupe_id))
    connection.commit()
    connection.close()
    # Move dupe image file
    file_name = str(dupe_id) + '.jpg'
    try:
        os.rename(IMAGE_PATH + file_name, DUPE_IMAGE_PATH + file_name)
    except Exception as err:
        print('error on ' + file_name)
        print(err)

def process_image_hash(file_name):
    """
    Generates a hashcode for an image and checks for an exact match in MySQL
    If match - moves related tweet to Duplicate_images table
    Otherwise, adds updates record with hash value
    :param file_name: string of file named as tweet_id.jpg
    """
    tweet_id = int(file_name[:-4])
    img = Image.open(IMAGE_PATH + file_name)
    img_hash = calculate_image_hash(img)
    match = find_matching_hash(img_hash, tweet_id)
    if match:
        process_duplicate_image(match, tweet_id, img_hash)
    else:
        add_hash_to_sql(tweet_id, img_hash)


def remove_original_tweet(tweet_id):
    """
    Deletes record from Original_tweets table
    :param tweet_id:
    """
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'DELETE FROM Original_tweets WHERE tweet_id = %s'
        cursor.execute(sql, int(tweet_id))
    connection.commit()
    connection.close()


def main():

    start_time = time.time()
    counter = 0
    for file in os.listdir(IMAGE_PATH):
        counter += 1
        if counter % 1000 == 0:
            print(time.time() - start_time)
            print(counter)
        if file.endswith('.jpg'):
            try:
                process_image_hash(file)
            except Exception as err:
                print('Error on image: ' + str(file))
                print(err)
    print('hashing complete')

    # double loop to check for near misses
    # 1. get df with tweet_ids & hash values from mysql
    tweet_list = get_tweet_list()
    # 2. double loop
    start_time = time.time()
    for i in range(len(tweet_list) - 1):
        if i % 100 == 0:
            print('\n'+ str(time.time() - start_time) + ' interval time')
            print(i, len(tweet_list))
            start_time = time.time()
        if not tweet_list.at[i, 'image_hash']:
            remove_original_tweet(tweet_list.at[i, 'tweet_id'])
            continue
        for j in range(i + 1, len(tweet_list)):
            try:
                if not tweet_list.at[j, 'image_hash']:
                    remove_original_tweet(tweet_list.at[j, 'tweet_id'])
                    continue
                dist = hamming_distance(tweet_list.at[i, 'image_hash'],
                                        tweet_list.at[j, 'image_hash'])
                if dist <= MAX_DIFF:
                    process_duplicate_image(tweet_list.at[i, 'tweet_id'],
                                            tweet_list.at[j, 'tweet_id'],
                                        tweet_list.at[j, 'image_hash'])
            except Exception as err:
                print(err)
                print('on '+ str(tweet_list.at[i, 'tweet_id']) + ', ' +
                      str(tweet_list.at[j, 'tweet_id']))

def test():
    import matplotlib.pyplot as plt
    file_list = os.listdir(IMAGE_PATH)[:10000]
    hash_list = []
    hash_diff_counts = {}
    image_list = []
    for file in file_list:
        if file.endswith('.jpg'):
            try:
                img = Image.open(IMAGE_PATH + file)
                hash_list.append(calculate_image_hash(img))
                image_list.append(file)
            except Exception as err:
                print('Error on file: ' + str(file))
                print(err)
    print('Hashing complete: Starting comparison')
    for i in range(len(hash_list)-1):
        for j in range(i + 1, len(hash_list)):
            dist = hamming_distance(hash_list[i], hash_list[j])
            if dist in hash_diff_counts:
                hash_diff_counts[dist] += 1
            else:
                hash_diff_counts[dist] = 1
            if 0 < dist < 10:
                print(image_list[i], image_list[j], dist)
    plt.bar(hash_diff_counts.keys(), hash_diff_counts.values())
    plt.xlabel('Hamming distance between hashes')
    plt.ylabel('Count')
    plt.title('Distribution of Image Differences')
    plt.show()
    # plt.savefig('/Users/christophergraham/Documents/School/Ryerson_program/CKME136/Submissions/graphics_etc/hash_diffs.png')
    print(hash_diff_counts)


if __name__ == '__main__':
    main()
