from time import time
import MatrixController as m
import heapq as hq

# goal state
goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

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
    for i in range(len(matrix)**2):
        if matrix[i//len(matrix)][i % len(matrix)] != goal_state[i//len(matrix)][i % len(matrix)]:
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

    timeconst = 1000000
    visited = set()
    
    mat_info[m.mat_to_str(matrix)] = ("Init", 0)
    level = 0
    # queue for node to process
    live_queue = []
    hq.heapify(live_queue)
    # a timer, to prevent a very long execution time
    start = time()
    # if start state is already a goal state, return the matrix_step
    if matrix == goal_state:
        matrix_step.append(matrix)
        return
    
    # set start_state
    start_state = matrix
    # push first matrix state to live_queue
    hq.heappush(live_queue, (f_func(matrix) + g_func(matrix), matrix))
    count = 0
    while live_queue and time() - start < timeLimit:
        matrix = live_queue.pop(0)
        matrix = matrix[1]
        # check if matrix already visited
        matstr = m.mat_to_str(matrix)
        if matstr in visited:
            continue
        visited.add(matstr)

        if matrix != start_state:
            level = mat_info[m.mat_to_str(matrix)][1]
        level += 1

        # iterate all 4 possible direction (build node)
        for move in enumerate(direction):
            newMatrix = m.move_16(matrix, move[1])
            matstr = m.mat_to_str(newMatrix)
            # skips if it's already visited, prevent from going backwards
            if (matstr in visited):
                continue

            # print("Jumlah simpul dibangkitkan: " + str(count))
            # create dic of matrix info and the parent            
            mat_info[matstr] = (move[1],  level)          
            parent[matstr] = matrix

            # count++
            count += 1
            # if (count % 1000 == 0):
            #     print("Jumlah simpul dibangkitkan: " + str(count))
            #     print("live_queue length: " + str(len(live_queue)))
            
            # check if newMatrix is the goal state
            if newMatrix == goal_state:
                connect_parent(newMatrix, matrix_step)
                print("Jumlah simpul dibangkitkan: " + str(count))
                return
            
            # else, queue the newMatrix
            hq.heappush(live_queue, (level + g_func(newMatrix), newMatrix))

    # if time limit exceded
    if live_queue:
        connect_parent(matrix, matrix_step)
        print("Jumlah simpul dibangkitkan: " + str(count))