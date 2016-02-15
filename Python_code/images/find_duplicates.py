"""
Find duplicates among downloaded images
Remove duplicates and update sentiment scores based on aggregate text

Calculates a perceptual hashcode (based on difference hashing) for each
image

Compares hashes using Hamming distance

counts as duplicate if distance < lam_val
"""

## Matching images in files:
# [693431907158245380, 693431894554329089]
# [693432267838988290, 693432498555084800, 693433001867354112, 693433106703863809]


import os
from Python_code.text_sentiment import compare_sentiments as sent
from Python_code import sql_connect as mysql
from PIL import Image
import math


IMAGE_PATH = '/Volumes/NeuralNet/images/'
# IMAGE_PATH = '/Volumes/NeuralNet/test_images/'


def concat_image_text(matching_id_list):
    connection = mysql.connect()
    # do something
    connection.close()


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
            pixel_right =image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # convert boolean list to hexadecimal string
    decimal_value = 0
    hex_string = []
    just_val = math.ceil(hash_size / 4)
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % hash_size)
        if (index % hash_size) == hash_size -1:
            hex_string.append(hex(decimal_value)[2:].rjust(just_val, '0'))
            decimal_value = 0
    return ''.join(hex_string)


def find_image_duplicates(jpg_file):
    # 1. load image
    # 2. loop through remaining files (all of them)
        # a. if match:
            # i. record id of matched image to list or something
    # 3. Concatenate text of all tweets with matching images
    # 4.
    pass


def process_dupes():
    axed_id_list = []
    for file in os.listdir(IMAGE_PATH):
        if file.endswith('.jpg'):
            tweet_id = int(file[:-4])
            dupe_list = find_image_duplicates(file)


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
    plt.show()
    print(hash_diff_counts)


if __name__ == '__main__':
    # process_dupes()
    test()