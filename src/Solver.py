import time
import MatrixController as m

# goal state
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

visited = []
start_state = []
timeLimit = 1200

# dictionary to store the parent of each matrixState
parent = {}
# dictionary to store matrix move and lvl
mat_info = {}

# enumerate direction
direction = ["Atas", "Bawah", "Kiri", "Kanan"]

# Function Kurang(i)
def kurang_func(matrix):
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
def f_func(matrix):
    return mat_info[m.mat_to_str(matrix)][1]

# our heuristic function, the number of misplaced tiles
def g_func(matrix):
    g = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != goal_state[i][j] and matrix[i][j] != 16:
                g += 1
    return g

# create matrix_step from the goal state to the start state
def connect_parent(newMatrix, matrix_step):
    global parent
    str_mat = m.mat_to_str(newMatrix)
    matrix_step.append((newMatrix, mat_info[str_mat][0]))
    tempPar = parent[str_mat]
    while tempPar != start_state:
        if (tempPar, mat_info[m.mat_to_str(newMatrix)][0]) not in matrix_step:
            matrix_step.append((tempPar, mat_info[m.mat_to_str(tempPar)][0]))
            tempPar = parent[m.mat_to_str(tempPar)]
    matrix_step.append(start_state)
    matrix_step.reverse()

# solver
def solve(matrix, matrix_step):
    # matrix stores the current matrixState
    # matrix_step stores the steps of solving the matrix
    # queue stores the list of matrixState that are not yet visited, is a PrioQueue to make sure we visited the matrixState with the lowest gFunc
    # parent stores the parent of each matrixState

    global start_state
    global parent

    mat_info[m.mat_to_str(matrix)] = ("Init", 0)
    level = 0
    # queue for node to process
    live_queue = []

    # a timer, to prevent a very long execution time
    start = time.time()
    # if start state is already a goal state, return the matrix_step
    if matrix == goal_state:
        matrix_step.append(matrix)
        return
    
    # set start_state
    start_state = matrix
    # append first matrix state to live_queue
    live_queue.append(matrix)
    count = 0
    while live_queue and time.time() - start < timeLimit:
        matrix = live_queue.pop(0)
        # check if matrix already visited
        if matrix in visited:
            continue
        visited.append(matrix)

        if matrix != start_state:
            level = mat_info[m.mat_to_str(matrix)][1]
        level += 1
        # iterate all 4 possible direction
        for move in enumerate(direction):
            newMatrix = m.move_16(matrix, move[1])
            if (newMatrix in visited):
                continue
            # print("Jumlah simpul dibangkitkan: " + str(count))
            # create a key for the newMatrix, to be used as a key in the parent dictionary
            matstr = m.mat_to_str(newMatrix)
            mat_info[matstr] = (move[1],  level)
            parent[matstr] = matrix

            # count++
            count += 1

            # check if newMatrix is the goal state
            if newMatrix == goal_state:
                connect_parent(newMatrix, matrix_step)
                print("Jumlah simpul dibangkitkan: " + str(count))
                return
            
            # else, queue the newMatrix
            live_queue.append(newMatrix)
            if len(live_queue) > 1:
                # cost check
                pos = live_queue.index(newMatrix)
                while (pos > 0 and f_func(live_queue[pos-1]) + g_func(live_queue[pos-1]) > level + g_func(live_queue[pos])):
                    live_queue[pos-1], live_queue[pos] = live_queue[pos], live_queue[pos-1]
                    pos -= 1


    # if time limit exceded
    if live_queue:
        connect_parent(matrix, matrix_step)
        print("Jumlah simpul dibangkitkan: " + str(count))