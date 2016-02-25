"""
Clean up missing images
"""

from Python_code import sql_connect as mysql
from Python_code.images import find_duplicates as dupes
from PIL import Image
import os

FILE_PATH = '/Volumes/NeuralNet/crowdflower_images/'
missing_image = Image.open(FILE_PATH + '694552455.jpg')
missing_hash = dupes.calculate_image_hash(missing_image)

print(missing_hash)

file_list = os.listdir(FILE_PATH)


def delete_from_mysql(img_id):
    connection = mysql.connect()
    with connection.cursor() as cursor:
        sql = 'DELETE FROM Crowdflower WHERE image_id = %s'
        cursor.execute(sql, img_id)
    connection.commit()
    connection.close()

for file in file_list:
    if file.endswith('.jpg'):
        img = Image.open(FILE_PATH + file)
        img_hash = dupes.calculate_image_hash(img)
        if img_hash == missing_hash:
            img_id = int(file[:-4])
            os.remove(FILE_PATH + file)
            delete_from_mysql(img_id)
