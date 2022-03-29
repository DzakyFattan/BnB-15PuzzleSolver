import os
from unittest import case

# read matrix from .txt file from specified input
def readMatrix(filename):
    matrix = []
    # get parent folder path
    fileDir = os.path.join( os.getcwd(), 'test', filename)
    print(fileDir)
    try:
        with open(fileDir, 'r') as f:
            for line in f:
                tempList = list(line.strip().split())
                matrix.append([int(x) for x in tempList])
        return matrix
    except FileNotFoundError:
        print("File tidak ditemukan")
        return None

# print matrix properly
def printMatrix(matrix):
    if (matrix != None):
        print("---------------------")
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                strToPrint = str(matrix[i][j]) + " " if matrix[i][j] < 10 else str(matrix[i][j])
                if strToPrint == "16": strToPrint = "  "
                print("| " + strToPrint, end=" ")
                if j == len(matrix[i])-1:
                    print("|")
            print("---------------------")
    else:
        print("Matrix kosong")

# find 16 position in matrix, return -1, -1 if not found
def find16(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] == 16):
                return i, j
    return -1, -1

def copyMatrix(matrix):
    tempMatrix = []
    for i in range(len(matrix)):
        tempMatrix.append([])
        for j in range(len(matrix[i])):
            tempMatrix[i].append(matrix[i][j])
    return tempMatrix

# move 16 to specified position
def move16(matrix, direction):
    i, j = find16(matrix)
    tempMatrix = copyMatrix(matrix)
    if direction == 0:
        if i > 0:
            tempMatrix[i][j], tempMatrix[i-1][j] = matrix[i-1][j], matrix[i][j]
    elif direction == 2:
        if i < len(matrix)-1:
            tempMatrix[i][j], tempMatrix[i+1][j] = matrix[i+1][j], matrix[i][j]
    elif direction == 3:
        if j > 0:
            tempMatrix[i][j], tempMatrix[i][j-1] = matrix[i][j-1], matrix[i][j]
    elif direction == 1:
        if j < len(matrix[i])-1:
            tempMatrix[i][j], tempMatrix[i][j+1] = matrix[i][j+1], matrix[i][j]
    return tempMatrix