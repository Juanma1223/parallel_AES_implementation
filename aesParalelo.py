from multiprocessing import Pool, Process
import aesSecuencial
import os
import shutil
import math

f = open("test.txt", "r")

nProcess = 6

# 128 bits password
password = "1234567891234567"

plainText = f.read()
# Remove line jumps
plainText = plainText.split("\n")
plainText = ' '.join(plainText)

# Remove previous encryption
shutil.rmtree('encrypted')
# Create new directory
os.mkdir('encrypted')
shutil.rmtree('decrypted')
# Create new directory
os.mkdir('decrypted')

# Domain partition
charsPerProcess = math.ceil(len(plainText)/nProcess)

# Store plain text for each process
processPlainText = []

i = 0
currPlainText = ""
for char in plainText:
    if(i < charsPerProcess):
        currPlainText = currPlainText + char
        i += 1
    else:
        i = 0
        processPlainText.append(currPlainText)
        currPlainText = ""

# Execute encryption over subdomain on each process
if __name__ == '__main__':
    with Pool(nProcess) as p:
        result = p.map(aesSecuencial.encrypt,processPlainText)


# Execute decryption in several files per process
files = os.listdir("encrypted")
nFilesPerProcess = math.ceil(len(files)/nProcess)
filesPerProcess = []
for i in range(0,nProcess):
    filesPerProcess.append(files[i*nFilesPerProcess:i*nFilesPerProcess+nFilesPerProcess])
if __name__ == '__main__':
    with Pool(nProcess) as p:
        result = p.map(aesSecuencial.decrypt,filesPerProcess)
