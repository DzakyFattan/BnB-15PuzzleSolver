import MatrixController as m

# goal state
goalState = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
counter = 0
tempDict = {}
visited = []
startState = []

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
    
def connectParent(newMatrix, matrixStep, parent):
    matrixStep.append(newMatrix)
    tempPar = parent[getKey(newMatrix)]
    while tempPar != startState:
        if tempPar not in matrixStep:
            matrixStep.append(tempPar)
            tempPar = parent[getKey(tempPar)]
    matrixStep.append(startState)
    matrixStep.reverse()


def solve(matrix, matrixStep, queue, parent):
    if matrix in visited:
        return
        # for i in visited:
        #     m.printMatrix(i)
    # print("-> Solve dipanggil, matriks di-append ke queue visited")
    visited.append(matrix)
    if matrix == goalState:
        matrixStep.append(matrix)
        return
    
    for i in range(4):
        newMatrix = m.move16(matrix, i)
        # m.printMatrix(newMatrix)
        # print("gFunc newMatrix:", gFunc(newMatrix))
        queue.append(newMatrix)

        if len(queue) > 1:
            try:
                pos = queue.index(newMatrix)
                while (pos > 0 and gFunc(queue[pos-1]) > gFunc(queue[pos])):
                    queue[pos-1], queue[pos] = queue[pos], queue[pos-1]
                    pos -= 1
            except RecursionError:
                print("Recursion Error, Hasil tidak dapat ditemukan")
                connectParent(matrix, matrixStep, parent)
                return
        
        global counter
        tempDict[counter] = newMatrix
        parent[counter] = matrix
        counter += 1
        if newMatrix == goalState:
            connectParent(newMatrix, matrixStep, parent)
            return

    if len(queue) != 0:
        # print("liveQueue atm:")
        # for i in queue:
        #     m.printMatrix(i)
        nextMatrix = queue.pop(0)
        # print("gFunc nextMatrix:", gFunc(nextMatrix))
        while (nextMatrix in visited):
            nextMatrix = queue.pop(0)
            # print("liveQueue length remove:",len(queue))
            if len(queue) == 0:
                return
        # print("Matriks selanjutnya:")
        # m.printMatrix(nextMatrix)
        # print("=====================================")
        solve(nextMatrix, matrixStep, queue, parent)