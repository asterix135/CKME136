"""
counts number of lines in all downloaded tweet files and prints count
"""

import os

os.chdir('/Volumes/NeuralNet/processed_data/')

total_lines = 0
for file in os.listdir():
    if file.endswith('.txt'):
        num_lines = sum(1 for line in open(file))
        total_lines += num_lines

print(total_lines)