import os

for file in os.listdir('/Volumes/NeuralNet/dupe_images/'):
    os.rename('/Volumes/NeuralNet/dupe_images/' + file, '/Volumes/NeuralNet/images/' + file)