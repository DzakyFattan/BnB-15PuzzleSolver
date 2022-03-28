import MatrixController as m

# goal state
goalState = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
counter = 0
tempDict = {}


def KURANGFunc(matrix):
    kurang = 0
    emptyPos = -1
    print("Urutan penulisan fungsi KURANG(i) mengikuti urutan baris dan kolom")
    for i in range(len(matrix)**2):
        if (matrix[i//len(matrix)][i % len(matrix)] == 16):
            emptyPos = i
        tempKurang = 0
        for j in range(i+1, len(matrix)**2):
            if (matrix[j//len(matrix)][j % len(matrix)] < matrix[i//len(matrix)][i % len(matrix)]):
                tempKurang += 1
        if matrix[i//len(matrix)][i % len(matrix)] != 16:
            print("KURANG(" + str(matrix[i//len(matrix)]
                  [i % len(matrix)]) + ") = " + str(tempKurang))
        kurang += tempKurang
    return kurang if emptyPos % 2 == 1 else kurang+1


def gFunc(matrix):
    g = 0
    for i in range(len(matrix)**2):
        if (matrix[i//len(matrix)][i % len(matrix)] != i + 1):
            g += 1
    return g


def getKey(matrixAsVal):
    for key, value in tempDict.items():
        if matrixAsVal == value:
            return key
    


def solve(matrix, matrixStep, queue, parent):
    if (matrix not in matrixStep):
        matrixStep.append(matrix)
    for i in range(4):
        newMatrix = m.move16(matrix, i)
        queue.append(newMatrix)
        if len(queue) > 1:
            pos = queue.index(newMatrix)
            while (pos > 0 and gFunc(queue[pos-1]) > gFunc(queue[pos])):
                queue[pos-1], queue[pos] = queue[pos], queue[pos-1]
                pos -= 1
        global counter
        tempDict[counter] = newMatrix
        parent[counter] = matrix
        counter += 1
        if newMatrix == goalState:
            matrixStep.append(newMatrix)
            if parent[getKey(newMatrix)] not in matrixStep:
                matrixStep.append(parent[getKey(newMatrix)])
            return
    if len(queue) != 0:
        nextMatrix = queue.pop(0)
        print("Matriks selanjutnya:")
        m.printMatrix(nextMatrix)
        solve(nextMatrix, matrixStep, queue, parent)