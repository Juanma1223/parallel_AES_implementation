import numpy as np
import aesTools

f = open("test.txt", "r")

# 128 bits password
password = "1234567891234567"

# Convert password to list
newList = []
newList[:0] = password
password = newList

plainText = f.read()

chars = []
i = 0

for char in plainText:
    # Get 16 characters and start block encryption
    if(i <= 16):
        chars.append(char)
        i = i + 1
    else:
        aesTools.aesEncrypt(chars, password)
        chars = []
        i = 0
