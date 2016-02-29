from PIL import Image
import os
import platform

if platform.platform()[:5] == 'Linux':
    IMAGE_DIR = '/home/ec2-user/images/'
else:
    IMAGE_DIR = '/Volumes/NeuralNet/images/'

for file in os.listdir(IMAGE_DIR):
    if file.endswith('jpg'):
        try:
            img = Image.open(IMAGE_DIR + file)
        except Exception as err:
            print("Error on image: " + str(file))
            print(err)
            os.remove(IMAGE_DIR + file)