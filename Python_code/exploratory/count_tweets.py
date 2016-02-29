"""
counts number of lines in all downloaded tweet files and prints count
"""

import os
import platform

if platform.platform()[:5] == 'Linux':
    IMAGE_DIR = '/home/ec2-user/images/'
else:
    IMAGE_DIR = '/Volumes/NeuralNet/images/'
os.chdir(IMAGE_DIR)

total_lines = 0
for file in os.listdir():
    if file.endswith('.txt'):
        num_lines = sum(1 for line in open(file))
        total_lines += num_lines

print(total_lines)