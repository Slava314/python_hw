import numpy as np


class FileMix:
    def write_to_file(self, file_path):
        with open(file_path, "w") as f:
            f.write(str(self))


class StrMix:
    def __str__(self):
        return 'matrix: {} * {}\n'.format(self.n, self.m) + str(self.val)


class GetSetMix:
    def get_val(self):
        return self.val

    def get_n(self):
        return self.n

    def get_m(self):
        return self.m

    def set_val(self, value):
        self.val = value
        self.n = len(value)
        self.m = len(value[0])


class Matrix:
    def __init__(self, lst):
        self.val = lst
        self.n = len(self.val)
        self.m = len(self.val[0])


class MatrixMix(Matrix, np.lib.mixins.NDArrayOperatorsMixin, FileMix, StrMix, GetSetMix):
    _HANDLED_TYPES = (Matrix,)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.val if isinstance(x, Matrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.val if isinstance(x, Matrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


np.random.seed(0)
a = MatrixMix(np.random.randint(0, 10, (10, 10)))
b = MatrixMix(np.random.randint(0, 10, (10, 10)))
(a + b).write_to_file("./artifacts/medium/matrix+.txt")
(a * b).write_to_file("./artifacts/medium/matrix*.txt")
(a @ b).write_to_file("./artifacts/medium/matrix@.txt")
