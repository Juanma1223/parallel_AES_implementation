import numpy as np

with open("test.txt", 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line)