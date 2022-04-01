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

# queue for node to process
liveQueue = []
# dictionary to store the parent of each matrixState
parent = {}

# enumerate direction
direction = ["Atas", "Bawah", "Kiri", "Kanan"]

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

# fFunc to find length from root parent to current matrix
def fFunc(matrix):
    level = 0
    while matrix != startState:
        matrix = parent[getKey(matrix)]
        level += 1
    return level

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
    a = 0
    for key, value in tempDict.items():
        a += 1
        if matrixAsVal == value[0]:
            return key

# create matrixStep from the goal state to the start state
def connectParent(newMatrix, matrixStep):
    global parent
    tempKey = getKey(newMatrix)
    matrixStep.append((newMatrix, tempDict[tempKey][1]))
    tempPar = parent[tempKey]
    while tempPar != startState:
        if tempPar not in matrixStep:
            matrixStep.append((tempPar, tempDict[getKey(tempPar)][1]))
            tempPar = parent[getKey(tempPar)]
    matrixStep.append(startState)
    matrixStep.reverse()

# solver
def solve(matrix, matrixStep):
    # matrix stores the current matrixState
    # matrixStep stores the steps of solving the matrix
    # queue stores the list of matrixState that are not yet visited, is a PrioQueue to make sure we visited the matrixState with the lowest gFunc
    # parent stores the parent of each matrixState

    # a timer, to prevent a very long execution time
    start = time.time()
    # if start state is already a goal state, return the matrixStep
    if matrix == goalState:
        matrixStep.append(matrix)
        return
    
    # append first matrix state to liveQueue
    global liveQueue
    global parent
    liveQueue.append(matrix)
    count = 0
    while liveQueue and time.time() - start < timeLimit:
        matrix = liveQueue.pop(0)
        # check if matrix already visited
        if matrix in visited:
            continue
        visited.append(matrix)

        # iterate all 4 possible direction
        for move in enumerate(direction):
            newMatrix = m.move16(matrix, move[1])
            if (newMatrix in visited):
                continue
            
            # create a key for the newMatrix, to be used as a key in the parent dictionary
            global counter
            tempDict[counter] = (newMatrix, move[1])
            parent[counter] = matrix
            counter += 1

            # count++
            count += 1

            # check if newMatrix is the goal state
            if newMatrix == goalState:
                connectParent(newMatrix, matrixStep)
                print("Jumlah simpul dibangkitkan: " + str(count))
                return
            
            # else, queue the newMatrix
            liveQueue.append(newMatrix)
            if len(liveQueue) > 1:
                # cost check
                pos = liveQueue.index(newMatrix)
                while (pos > 0 and fFunc(liveQueue[pos-1]) + gFunc(liveQueue[pos-1]) > fFunc(liveQueue[pos]) + gFunc(liveQueue[pos])):
                    liveQueue[pos-1], liveQueue[pos] = liveQueue[pos], liveQueue[pos-1]
                    pos -= 1


    # if time limit exceded
    if liveQueue:
        connectParent(matrix, matrixStep)
        print("Jumlah simpul dibangkitkan: " + str(count))