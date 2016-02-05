"""
Get sizes of images from urls
http://stackoverflow.com/questions/1507084/how-to-check-dimensions-of-all-images-in-a-directory-using-python
http://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
"""

import urllib.request as urllib
from PIL import Image
from io import BytesIO
import requests
from Python_code import sql_connect as sql


href = 'http://pbs.twimg.com/media/CZg3tZyUcAACpMg.jpg'



def get_size(url):
    # image = Image.open(filepath)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    print(width, height)


get_size(href)
