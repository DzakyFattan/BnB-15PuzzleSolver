import time
import MatrixController as m

# goal state
goalState = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
# counter to create a key for each matrixState
counter = 0
tempDict = {}
visited = []
startState = []
timeLimit = 1200

# Function Kurang(i)
def KURANGFunc(matrix):
    kurang = 0
    emptyPos = -1
    print("Urutan penulisan fungsi KURANG(i) mengikuti urutan baris dan kolom")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 16:
                emptyPos = i + j
            tempKurang = 0
            for k in range(i * len(matrix) + j + 1, len(matrix)**2):
                if matrix[k//len(matrix)][k % len(matrix)] < matrix[i][j]:
                    tempKurang += 1
            if (matrix[i][j] != 16):
                print("KURANG(" + str(matrix[i][j]) + ") = " + str(tempKurang))
            kurang += tempKurang
    return kurang if emptyPos % 2 == 0 else kurang+1

# our heuristic function, the number of misplaced tiles
def gFunc(matrix):
    g = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != goalState[i][j] and matrix[i][j] != 16:
                g += 1
    return g

# get the key of the matrixState
def getKey(matrixAsVal):
    for key, value in tempDict.items():
        if matrixAsVal == value:
            return key

# create matrixStep from the goal state to the start state
def connectParent(newMatrix, matrixStep, parent):
    matrixStep.append(newMatrix)
    tempPar = parent[getKey(newMatrix)]
    while tempPar != startState:
        if tempPar not in matrixStep:
            matrixStep.append(tempPar)
            tempPar = parent[getKey(tempPar)]
    matrixStep.append(startState)
    matrixStep.reverse()

# solver
def solve(matrix, matrixStep, queue, parent):
    # matrix stores the current matrixState
    # matrixStep stores the steps of solving the matrix
    # queue stores the list of matrixState that are not yet visited, is a PrioQueue to make sure we visited the matrixState with the lowest gFunc
    # parent stores the parent of each matrixState

    # a timer, to prevent a very long execution time
    start = time.time()

    # append first matrix state to queue
    queue.append(matrix)
    count = 0
    while queue and time.time() - start < timeLimit:
        matrix = queue.pop(0)

        # check if matrix already visited, this part can be improved
        if matrix in visited:
            continue
        visited.append(matrix)

        # if start state is already a goal state, return the matrixStep
        if matrix == goalState:
            matrixStep.append(matrix)
            return

        # iterate all 4 possible direction
        for i in range(4):
            newMatrix = m.move16(matrix, i)

            # queue the newMatrix, could also be improved
            queue.append(newMatrix)

            if len(queue) > 1:

                # gFunc check
                pos = queue.index(newMatrix)
                while (pos > 0 and gFunc(queue[pos-1]) > gFunc(queue[pos])):
                    queue[pos-1], queue[pos] = queue[pos], queue[pos-1]
                    pos -= 1
            
            # create a key for the newMatrix, to be used as a key in the parent dictionary
            global counter
            tempDict[counter] = newMatrix
            parent[counter] = matrix
            counter += 1

            # finally, check if newMatrix is the goal state
            if newMatrix == goalState:
                connectParent(newMatrix, matrixStep, parent)
                return

    # if time limit exceded
    if queue:
        connectParent(matrix, matrixStep, parent)