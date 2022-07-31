from pydoc import plain
import numpy as np
import aesTools
import os
import shutil

f = open("test.txt", "r")

# 128 bits password
password = "1234567891234567"

# Convert password to list
newList = []
newList[:0] = password
password = newList

plainText = f.read()
# Remove line jumps
plainText = plainText.split("\n")
plainText = ' '.join(plainText)
print(plainText)


chars = []
i = 0

fileIndex = 0

# Remove previous encryption
shutil.rmtree('encrypted')
# Create new directory
os.mkdir('encrypted')

# Encrypt
for char in plainText:
    # Get 16 characters and start block encryption
    if(i <= 16):
        chars.append(char)
        i = i + 1
    else:
        encrypted = aesTools.aesEncrypt(chars, password)
        # Write encrypted content to file
        newFile = open("./encrypted/"+str(fileIndex)+".txt", "x")
        newFile.write(encrypted)
        fileIndex += 1
        chars = []
        i = 0


# Decrypt

# Remove previous encryption
shutil.rmtree('decrypted')
# Create new directory
os.mkdir('decrypted')

# Open encrypted files directory
directory = 'encrypted'
fileIndex = 0
for file in os.listdir(directory):
    encrypted = open(directory+"/"+file)
    text = encrypted.read()
    decrypted = aesTools.aesDecrypt(text, password)
    print(decrypted)
    # Write decrypted content to file
    newFile = open("./decrypted/"+str(fileIndex)+".txt", "x")
    fileIndex += 1
    newFile.write(decrypted)
