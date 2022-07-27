import math
import numpy as np
import copy
import sBox

def aesEncrypt(chars, password):
    # Convert plain text to 4x4 matrix
    stateMatrix = buildStateMatrix(chars)
    passwordMatrix = buildStateMatrix(password)
    print(stateMatrix)
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
            stateMatrix[j][i] = passChar ^ currNumber
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
        key[i][0] = int(key[i][0]) ^ int(key[i][3])
    # Xor every other column with the corresponding one
    for i in range(1, 4):
        for j in range(0, 4):
            key[j][i] = int(key[j][i-1]) ^ int(prevKey[j][i])
    return key


# Shifts rows to the left to create diffusion
def shiftRows(stateMatrix):
    for i in range(0, 4):
        # Rotate as many times as needed
        for j in range(0, i):
            aux = np.append(stateMatrix[i][1:4], stateMatrix[i][0])
            stateMatrix[i] = aux
    return stateMatrix


# Inverse function, rotates to the right
def invShiftRows(stateMatrix):
    for i in range(0, 4):
        # Rotate as many times as needed
        for j in range(0, i):
            aux = np.append(stateMatrix[i][3],stateMatrix[i][0:3])
            stateMatrix[i] = aux
    return stateMatrix

# Apply transformation matrix to add confusion column wise
def mixColumns(stateMatrix):

    for i in range(0,4):
        stateMatrix[:,i] = galoisMultiply(stateMatrix[:,i])
    return stateMatrix

def invMixColumns(stateMatrix):
    for i in range(0,4):
        stateMatrix[:,i] = invGaloisMultiply(stateMatrix[:,i])
    return stateMatrix

# Apply multiplication on the galois field to a single column
def galoisMultiply(col):
    newCol = np.array([0,0,0,0])
    newCol[0] = math.floor(sBox.gMulBy2(col[0])) ^ math.floor(sBox.gMulBy3(col[1])) ^ math.floor(col[2]) ^ math.floor(col[3])
    newCol[1] = math.floor(col[0]) ^ math.floor(sBox.gMulBy2(col[1])) ^ math.floor(sBox.gMulBy3(col[2])) ^ math.floor(math.floor(col[3]))
    newCol[2] = math.floor(col[0]) ^ math.floor(col[1]) ^ math.floor(sBox.gMulBy2(col[2])) ^ math.floor(sBox.gMulBy3(col[3]))
    newCol[3] = math.floor(sBox.gMulBy3(col[0])) ^ math.floor(col[1]) ^ math.floor(col[2]) ^ math.floor(sBox.gMulBy2(col[3]))
    return newCol

def invGaloisMultiply(col):
    newCol = np.array([0,0,0,0])
    newCol[0] = math.floor(sBox.gMulBy14(col[0])) ^ math.floor(sBox.gMulBy11(col[1])) ^ math.floor(sBox.gMulBy13(col[2])) ^ math.floor(sBox.gMulBy9(col[3]))
    newCol[1] = math.floor(sBox.gMulBy9(col[0])) ^ math.floor(sBox.gMulBy14(col[1])) ^ math.floor(sBox.gMulBy11(col[2])) ^ math.floor(sBox.gMulBy13(col[3]))
    newCol[2] = math.floor(sBox.gMulBy13(col[0])) ^ math.floor(sBox.gMulBy9(col[1])) ^ math.floor(sBox.gMulBy14(col[2])) ^ math.floor(sBox.gMulBy11(col[3]))
    newCol[3] = math.floor(sBox.gMulBy11(col[0])) ^ math.floor(sBox.gMulBy13(col[1])) ^ math.floor(sBox.gMulBy9(col[2])) ^ math.floor(sBox.gMulBy14(col[3]))
    return newCol