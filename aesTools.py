import numpy as np
import copy
import sBox

# Composed logical gate for bitwise xor


def xor(a, b):
    return (a & (~ b)) | ((~ a) & b)


def aesEncrypt(chars, password):
    # Convert plain text to 4x4 matrix
    stateMatrix = buildStateMatrix(chars)
    passwordMatrix = buildStateMatrix(password)
    for i in range(0, 9):
        # Perform bitwise xor between state matrix and password
        stateMatrix = stateMatrixXor(stateMatrix, passwordMatrix)
        # Perform byte substitution using substitution box
        stateMatrix = sBox.subBytes(stateMatrix)
        # Apply diffusion
        stateMatrix = shiftRows(stateMatrix)
        stateMatrix = mixColumns(stateMatrix)
        # Get new key
        passwordMatrix = keyExpansion(passwordMatrix)
    return stateMatrix


# Map plain text to a 4x4 matrix for encryption
def buildStateMatrix(chars):
    # Define state matrix with shape 4x4
    # 1 char = 8 bits = 1 byte
    stateMatrix = np.zeros((4, 4))
    for i in range(0, 4):
        for j in range(0, 4):
            # Check if less than 16 chars have been sent
            if((i*4)+j >= len(chars)):
                return stateMatrix
            # Convert 2 dimensional index i and j to 1 dimensional array index and
            # convert char to it's ascii code equivalent
            charAscii = ord(chars[(i*4)+j])
            stateMatrix[j][i] = charAscii
    return stateMatrix

# Apply bitwise xor between the password and the state matrix


def stateMatrixXor(stateMatrix, password):
    for i in range(0, 4):
        for j in range(0, 4):
            passChar = int(password[j][i])
            currNumber = int(stateMatrix[j][i])
            # Perform bitwise xor between password and stateMatrix for each character
            stateMatrix[j][i] = xor(passChar, currNumber)
    return stateMatrix


# Generate new expansion key for every step
def keyExpansion(key):
    prevKey = copy.deepcopy(key)
    aux = key[3][3]
    key[3][3] = key[0][3]
    key[0][3] = aux
    # Apply substitution box
    for i in range(0, 4):
        key[i][3] = sBox.sBox(key[i][3])
    # Xor between previous key's first column and new generated column
    for i in range(0, 4):
        key[i][0] = xor(int(key[i][0]), int(key[i][3]))
    # Xor every other column with the corresponding one
    for i in range(1, 4):
        for j in range(0, 4):
            key[j][i] = xor(int(key[j][i-1]), int(prevKey[j][i]))
    return key


# Shifts rows to the left to create diffusion
def shiftRows(stateMatrix):
    for i in range(0, 4):
        # Rotate as many times as needed
        for j in range(0, i):
            aux = np.append(stateMatrix[i][1:4], stateMatrix[i][0])
            stateMatrix[i] = aux
    print(stateMatrix)
    return stateMatrix


# Inverse function, rotates to the right
def invShiftRows(stateMatrix):
    print(stateMatrix)
    for i in range(0, 4):
        # Rotate as many times as needed
        for j in range(0, i):
            aux = np.append(stateMatrix[i][3],stateMatrix[i][0:3])
            stateMatrix[i] = aux
    print(stateMatrix)
    return stateMatrix

# WIP
def mixColumns(stateMatrix):
    return stateMatrix


