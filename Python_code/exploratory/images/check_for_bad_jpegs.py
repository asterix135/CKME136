from PIL import Image
import os

for file in os.listdir('/Volumes/NeuralNet/images/'):
    if file.endswith('jpg'):
        try:
            img = Image.open('/Volumes/NeuralNet/images/' + file)
        except Exception as err:
            print("Error on image: " + str(file))
            print(err)
            os.remove('/Volumes/NeuralNet/images/' + file)