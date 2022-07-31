from pydoc import plain
import numpy as np
import aesTools
import os
import shutil

password = "1234567891234567"


def encrypt(plainText):
    global password
    print("current process", os.getpid())
    # Convert password to list
    newList = []
    newList[:0] = password
    password = newList

    chars = []
    i = 0

    fileIndex = 0

    # Encrypt
    for char in plainText:
        # Get 16 characters and start block encryption
        if(i <= 16):
            chars.append(char)
            i = i + 1
        else:
            encrypted = aesTools.aesEncrypt(chars, password)
            # Write encrypted content to unique name file
            newFile = open("./encrypted/"+str(os.getpid()) +
                           str(fileIndex)+".txt", "x")
            newFile.write(encrypted)
            fileIndex += 1
            chars = []
            i = 0


# Decrypt

def decrypt(files):
    global password
    for file in files:
        f = open("encrypted/"+file,"r")
        cyphertext = f.read()
        # Convert password to list
        newList = []
        newList[:0] = password
        password = newList
        decrypted = aesTools.aesDecrypt(cyphertext, password)
        # Write encrypted content to file
        newFile = open("decrypted/"+file, "x")
        newFile.write(decrypted)
        i = 0


# Remove previous encryption
shutil.rmtree('encrypted')
# Create new directory
os.mkdir('encrypted')
shutil.rmtree('decrypted')
# Create new directory
os.mkdir('decrypted')

f = open("test.txt", "r")
# 128 bits password
password = "1234567891234567"

plainText = f.read()
# Remove line jumps
plainText = plainText.split("\n")
plainText = ' '.join(plainText)

encrypt(plainText)
decrypt(os.listdir("encrypted"))