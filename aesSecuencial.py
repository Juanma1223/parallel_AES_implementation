import numpy as np
import aesTools
import sBox

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
        encrypted = aesTools.aesEncrypt(chars, password)
        print("encrypted",encrypted)
        decrypted = aesTools.aesDecrypt(encrypted)
        print("decrypted",decrypted)
        chars = []
        i = 0

