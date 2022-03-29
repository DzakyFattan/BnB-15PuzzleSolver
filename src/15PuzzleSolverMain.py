import time
import sys
import MatrixController as m
import Solver as s

# variables for BnB
matrixStep = []
liveQueue = []
f = 1
parent = {}

def printTitle():
    print("""
 _ ____          ___               _        __       _                
/ | ___|        / _ \_   _ _______| | ___  / _\ ___ | |_   _____ _ __ 
| |___ \ _____ / /_)/ | | |_  /_  / |/ _ \ \ \ / _ \| \ \ / / _ \ '__|
| |___) |_____/ ___/| |_| |/ / / /| |  __/ _\ \ (_) | |\ V /  __/ |   
|_|____/      \/     \__,_/___/___|_|\___| \__/\___/|_| \_/ \___|_|   
                                                                      
""")
    print("\nDibuat oleh: Dzaky Fattan Rizqullah - 13520003\n")


# The Main Program
sys.setrecursionlimit((10**3)*2)
printTitle()
ipt = input("\nInput nama file, pastikan sudah terletak dalam folder test (contoh: input.txt): ")
matrix = m.readMatrix(ipt)
if (matrix != None):
    print("Matriks yang dibaca:")
    m.printMatrix(matrix)
    kurang = s.KURANGFunc(matrix)
    if kurang % 2 == 1:
        print("Status tujuan tidak dapat dicapai")
    else:
        start = time.time_ns()
        print("Status tujuan dapat dicapai")
        s.startState = matrix
        s.solve(matrix, matrixStep, liveQueue, parent)
        end = time.time_ns()
        if (matrixStep != []):
            print("\nPosisi awal:")
            m.printMatrix(matrixStep.pop(0))
            for i in range(len(matrixStep)):
                print("\nLangkah ke-" + str(i+1) + ":")
                m.printMatrix(matrixStep[i])

        print("Waktu eksekusi: " + str((end-start)/1000000) + " ms")
        # prompt before exiting
        input("Press enter to exit\n")