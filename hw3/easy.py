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


class Matrix:
    def __init__(self, lst):
        self.val = lst
        self.n = len(self.val)
        if self.n == 0:
            raise MatrixError('Matrix with zero lines')
        self.m = len(self.val[0])
        for line in self.val:
            if len(line) != self.m:
                raise MatrixError('Matrix with different line sizes')

    def __add__(self, other):
        try:
            if self.n != other.n or self.m != other.m:
                raise ArithmeticMatrixError(self.n, self.m, other.n, other.m, 'Incorrect matrices sizes')
            res = [[0 for _ in range(self.n)] for _ in range(self.m)]
            for i in range(self.n):
                for j in range(self.m):
                    res[i][j] = self.val[i][j] + other.val[i][j]
            return Matrix(res)
        except ArithmeticMatrixError as e:
            print(e)
            return None

    def __mul__(self, other):
        try:
            if self.n != other.n or self.m != other.m:
                raise ArithmeticMatrixError(self.n, self.m, other.n, other.m, 'Incorrect matrices sizes')
            res = [[0 for _ in range(self.m)] for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.m):
                    res[i][j] = self.val[i][j] * other.val[i][j]
            return Matrix(res)
        except ArithmeticMatrixError as e:
            print(e)
            return None

    def __matmul__(self, other):
        try:
            if self.m != other.n:
                raise ArithmeticMatrixError(self.n, self.m, other.n, other.m, 'Incorrect matrices sizes')
            res = [[0 for _ in range(self.n)] for _ in range(other.m)]
            for i in range(self.n):
                for j in range(other.m):
                    for k in range(other.n):
                        res[i][j] += self.val[i][k] * other.val[k][j]
            return Matrix(res)
        except ArithmeticMatrixError as e:
            print(e)
            return None

    def __str__(self):
        s = '['
        for lst in self.val:
            s += str(lst).replace(',', '') + '\n '
        return s[:-2] + ']'


np.random.seed(0)
a = Matrix(np.random.randint(0, 10, (10, 10)))
b = Matrix(np.random.randint(0, 10, (10, 10)))

with open("./artifacts/easy/matrix+.txt", 'w') as f:
    f.write(str(a + b))

with open("./artifacts/easy/matrix*.txt", 'w') as f:
    f.write(str(a * b))

with open("./artifacts/easy/matrix@.txt", 'w') as f:
    f.write(str(a @ b))
