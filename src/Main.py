from time import time_ns
import MatrixController as m
import Solver as s

# list of steps
matrix_step = []

def print_title():
    print("""
 _ ____          ___               _        __       _                
/ | ___|        / _ \_   _ _______| | ___  / _\ ___ | |_   _____ _ __ 
| |___ \ _____ / /_)/ | | |_  /_  / |/ _ \ \ \ / _ \| \ \ / / _ \ '__|
| |___) |_____/ ___/| |_| |/ / / /| |  __/ _\ \ (_) | |\ V /  __/ |   
|_|____/      \/     \__,_/___/___|_|\___| \__/\___/|_| \_/ \___|_|   
                                                                      
""")
    print("Dibuat oleh: Dzaky Fattan Rizqullah - 13520003")

def calc_time(start, end):
    duration = (end - start)
    if duration > 1000000000:
        duration = duration / 1000000000
        print("\nWaktu eksekusi:", duration, "detik")
    elif duration > 1000000:
        duration = duration / 1000000
        print("\nWaktu eksekusi:", duration, "ms")
    else:
        print("\nWaktu eksekusi:", duration, "ns")

# The Main Program
def main():
    print_title()
    ipt = input("\nInput nama file, pastikan sudah terletak dalam folder test (contoh: input.txt): ")
    matrix = m.read_matrix(ipt)
    if (matrix != None):
        print("Puzzle yang dibaca:")
        m.print_matrix(matrix)
        kurang = s.kurang_func(matrix)
        print("Nilai Kurang(i) + X:", kurang)
        if kurang % 2 == 1:
            print("\nStatus tujuan tidak dapat dicapai")
        else:
            start = time_ns()
            print("\nStatus tujuan dapat dicapai, mencari solusi...")
            s.startState = matrix
            s.solve(matrix, matrix_step)
            end = time_ns()
            if (matrix_step != []):
                print("\nPosisi awal:")
                m.print_matrix(matrix_step.pop(0))
                for i in range(len(matrix_step)):
                    print("\nLangkah ke-" + str(i+1) + ": " + str(matrix_step[i][1]))
                    m.print_matrix(matrix_step[i][0])
            print("\nUrutan langkah: ", end="")
            for i in range(len(matrix_step)):
                str_to_print = str(matrix_step[i][1]) + ", " if i != len(matrix_step) - 1 else str(matrix_step[i][1])
                print(str_to_print, end="")
            calc_time(start, end)
    else:
        print("Error saat membaca matriks persoalan.")
    # prompt before exiting
    input("Press enter to exit\n")

if __name__ == "__main__":
    main()