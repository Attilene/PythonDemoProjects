from multiprocessing import Process, Pool
import os


def read(path: str):
    res = []
    f = open(path, "r", encoding='utf-8')
    while True:
        line = f.readline()
        if not line:
            break
        res.append(list(map(lambda x: float(x), line.split())))
    return res


def check_matrix(matrix1: list, matrix2: list) -> bool:
    L = len(matrix1[0])
    for row in matrix1:
        if len(row) != L:
            return False
    if L != len(matrix2):
        return False
    return True


def calc_element(index: tuple, A: list, B: list, path: str):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    write_element(path, res)


def write_element(path: str, element):
    with open(path, "w") as file:
        file.write(str(element))
        file.close()


def write_length(path: str, matrix1: list, matrix2: list) -> tuple:
    l1 = len(matrix1[0])
    l2 = len(matrix2)
    with open(path, "a") as file:
        file.write(str(l1) + ' ' + str(l2) + '\n')
        file.close()
    return l1, l2


def write_to_result_matrix(path_length: str, path_res: str):
    with open(path_length, 'r') as file_length:
        l1, l2 = map(lambda x: int(x), file_length.readline().split())
        file_length.close()
    with open(path_res, "w") as file_res:
        for i in range(l1):
            for j in range(l2):
                while not os.path.isfile(str(i) + '_' + str(j)):
                    pass
                with open(str(i) + '_' + str(j), 'r') as f:
                    file_res.write(f.readline() + ' ')
                    f.close()
            file_res.write('\n')
        file_res.close()


def start():
    A = read("first_matrix.txt")
    B = read("second_matrix.txt")
    POOL_THREADS = 4
    if check_matrix(A, B):
        l1, l2 = write_length("length.txt", A, B)
        pool = Pool(POOL_THREADS)
        proc_list = []
        for i in range(l1):
            for j in range(l2):
                proc_list.append(
                    pool.apply_async(
                        calc_element, ((i, j), A, B, str(i) + '_' + str(j))))
        write_to_result_matrix("length.txt", "result_matrix.txt")
    else:
        print("Некорректный формат начальных матриц!")


if __name__ == "__main__":
    start()