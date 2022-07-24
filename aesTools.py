import numpy as np

# Composed logical gate for xor
def xor(a, b):
    return (a & (~ b)) | ((~ a) & b)


def aesEncrypt(chars,password):
    stateMatrix = buildStateMatrix(chars)
    #print(stateMatrix)
    print("")
    stateMatrix = stateMatrixXor(stateMatrix,password)
    print(stateMatrix)


def buildStateMatrix(chars):
    # Define state matrix with shape 4x4
    # 1 char = 8 bits = 1 byte
    stateMatrix = np.zeros((4,4))
    for i in range(0,4):
        for j in range(0,4):
            # Check if less than 16 chars have been sent
            if((i*4)+j >= len(chars)):
                return stateMatrix
            # Convert 2 dimensional index i and j to 1 dimensional array index and
            # convert char to it's ascii code equivalent
            charAscii = ord(chars[(i*4)+j])
            stateMatrix[j][i] = charAscii
    return stateMatrix


def stateMatrixXor(stateMatrix,password):
    for i in range(0,4):
        for j in range(0,4):
            passChar = ord(password[(i*4)+j])
            currNumber = int(stateMatrix[j][i])
            # Perform bitwise xor between password and stateMatrix for each character
            stateMatrix[j][i] = xor(passChar,currNumber)
    return stateMatrix


    