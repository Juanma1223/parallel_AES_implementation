# Substitution box
# Adds confusion to the information

import numpy as np


# This table is the result of taking the inverse multiplicative IN THE GALOIS FIELD (x/(x**8+x**4+x**3+x+1)) for numbers
# between 0 and 256 in hexadecimal, then, a transformation matrix is applied to add even more confussion

# https://en.wikipedia.org/wiki/Rijndael_S-box

# To avoid all of the previously mentioned calculus, we load the matrix directly into memory
substitutionMatrix = np.array([
    ["63", "7c", "77", "7b", "f2", "6b", "6f", "c5",
     "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
    ["ca", "82", "c9", "7d", "fa", "59",	"47", "f0",
     "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
    ["ca",	"82", "c9", "7d", "fa", "59", "47", "f0",
     "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
    ["04", "c7", "23", "c3", "18", "96", "05", "9a",
     "07", "12", "80", "e2", "eb", "27", "b2", "75"],
    ["09",	"83",	"2c",	"1a",	"1b",	"6e",	"5a",	"a0",
     "52", "3b",	"d6",	"b3",	"29",	"e3",	"2f",	"84"],
    ["53",	"d1",	"00",	"ed",	"20",	"fc",	"b1",	"5b",
     "6a",	"cb",	"be",	"39",	"4a",	"4c",	"58",	"cf"],
    ["d0",	"ef",	"aa",	"fb",	"43",	"4d",	"33",	"85",
     "45",	"f9",	"02",	"7f",	"50",	"3c",	"9f",	"a8"],
    ["51",	"a3",	"40",	"8f",	"92",	"9d",	"38",	"f5",
     "bc",	"b6",	"da",	"21",	"10",	"ff",	"f3",	"d2"],
    ["cd",	"0c",	"13",	"ec",	"5f",	"97",	"44",	"17",	"c4",
     "a7",	"7e",	"3d",	"64",	"5d",	"19",	"73"],
    ["60",	"81",	"4f",	"dc", "22",	"2a",	"90",	"88",
     "46",	"ee",	"b8",	"14",	"de",	"5e",	"0b",	"db"],
    ["e0",	"32",	"3a",	"0a",	"49",	"06",	"24",	"5c",
     "c2",	"d3",	"ac",	"62",	"91",	"95",	"e4",	"79"],
    ["e7",	"c8",	"37",	"6d",	"8d",	"d5",	"4e",	"a9",
     "6c",	"56",	"f4",	"ea",	"65",	"7a",	"ae",	"08"],
    ["ba",	"78",	"25",	"2e",	"1c",	"a6",	"b4",	"c6",
     "e8",	"dd",	"74",	"1f",	"4b",	"bd",	"8b",	"8a"],
    ["70",	"3e",	"b5",	"66",	"48",	"03",	"f6",	"0e",
     "61",	"35",	"57",	"b9",	"86",	"c1",	"1d",	"9e"],
    ["e1",	"f8",	"98",	"11",	"69",	"d9",	"8e",	"94",
     "9b",	"1e",	"87",	"e9",	"ce",	"55",	"28",	"df"],
    ["8c",	"a1",	"89",	"0d",	"bf",	"e6",	"42",	"68",
     "41",	"99",	"2d",	"0f",	"b0", "54",	"bb",	"16"]
])


# Apply susbtitution using the Rjindael S-Box to add more confussion to the ciphertext
def sBox(num):
    num = int(num)
    binary = bin(num)
    # Add padding to binary number so we can extract nibbles
    padding = 10-len(binary)
    binary = binary[0:2]+''.join(["0" for i in range(0, padding)])+binary[2:]
    # Most significant nibble decimal conversion
    firstNibble = int("0b"+binary[2:6], base=2)
    # Less significant nibble decimal conversion
    lastNibble = int("0b"+binary[6:10], base=2)
    substitute = substitutionMatrix[firstNibble][lastNibble]
    # Convert from hex to decimal
    return int("0x"+substitute, base=16)


# Replace every number of a matrix for it's equivalent substitute
def subBytes(matrix):
    for i in range(0, 4):
        for j in range(0, 4):
            matrix[i][j] = sBox(matrix[i][j])
    return matrix