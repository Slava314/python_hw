import numpy as np


class ArithmeticMatrixError(Exception):
    def __init__(self, left_n, left_m, right_n, right_m, description):
        self.left_n = left_n
        self.left_m = left_m
        self.right_n = right_n
        self.right_m = right_m
        self.val = description + ': {} * {} and {} * {}'.format(left_n, left_m, right_n, right_m)

    def __str__(self):
        return str(self.val)


class MatrixError(Exception):
    def __init__(self, description):
        self.val = description

    def __str__(self):
        return str(self.val)


class HashMix:
    def sum_squares_hash(self):
        """
            calculates the hash of matrix as sum of squares
        """
        return int(sum(sum(x * x for x in line) for line in self.val))


class Matrix(HashMix):
    _matmul_cache = {}

    def __init__(self, lst):
        self.val = lst
        self.n = len(self.val)
        if self.n == 0:
            raise MatrixError('Matrix with zero lines')
        self.m = len(self.val[0])
        for line in self.val:
            if len(line) != self.m:
                raise MatrixError('Matrix with different line sizes')

    def __matmul__(self, other):
        try:
            if self.m != other.n:
                raise ArithmeticMatrixError(self.n, self.m, other.n, other.m, 'Incorrect matrices sizes')
            matrix_hash = (hash(self), hash(other))
            if matrix_hash not in self._matmul_cache:
                res = [[0 for _ in range(self.n)] for _ in range(other.m)]
                for i in range(self.n):
                    for j in range(other.m):
                        for k in range(other.n):
                            res[i][j] += self.val[i][k] * other.val[k][j]
                self._matmul_cache[matrix_hash] = res
            return Matrix(self._matmul_cache[matrix_hash])
        except ArithmeticMatrixError as e:
            print(e)
            return None

    def __hash__(self):
        return self.sum_squares_hash()

    def __str__(self):
        s = '['
        for lst in self.val:
            s += str(lst).replace(',', '') + '\n '
        return s[:-2] + ']'

    def write_to_file(self, file_path):
        with open(file_path, "w") as f:
            f.write(str(self))


a = Matrix([[3, 4], [6, 8]])
b = Matrix([[1, 1], [1, 1]])
c = Matrix([[5, 0], [10, 0]])
d = Matrix([[1, 1], [1, 1]])

a.write_to_file("./artifacts/hard/A.txt")
b.write_to_file("./artifacts/hard/B.txt")
c.write_to_file("./artifacts/hard/C.txt")
d.write_to_file("./artifacts/hard/D.txt")

ab = a @ b
c._matmul_cache = {}
cd = c @ d

ab.write_to_file("./artifacts/hard/AB.txt")
cd.write_to_file("./artifacts/hard/CD.txt")

with open("./artifacts/hard/hash.txt", "w") as file:
    file.write('AB hash: ')
    file.write(str(hash(ab)) + '\n')
    file.write('CD hash: ')
    file.write(str(hash(cd)) + '\n')