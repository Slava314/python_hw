from ExampleGeneratorOfAST import generate_image
from ExampleGeneratorOfAST import fib

from functools import reduce


def make_tex_file(name_of_file, string):
    f = open('artifacts/' + name_of_file + '.tex', 'w')
    head = '\\documentclass[12pt]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[' \
           'english]{babel}\n\\usepackage{graphicx}\n\\graphicspath{ {./artifacts/} }\n\\begin{document}\n'
    end = '\end{document}\n'
    f.write(head + string + end)
    f.close()


def resize_lst(lst, n, element=''):
    return lst[:n] + [element for _ in range(n - len(lst))]


def easy_task(lst):
    list_str = '\\begin{tabular}{ |'
    n = max(map(len, lst))
    lst = list(map(lambda x: resize_lst(x, n), lst))
    list_str += 'c|' * n + '}\n\\hline\n'
    list_str += reduce(
        lambda l, r: l + '\\hline\n' + r,
        map(lambda line: reduce(lambda l, r: str(l) + ' & ' + str(r), line) + ' \\\\\n', lst)
    )
    list_str += '\\hline\n\\end{tabular}\n'
    # make_tex_file('easy_task', list_str)
    return list_str


def medium_task(picture_path, lst):
    list_str = easy_task(lst)
    generate_image.generate_image(fib.fib)
    list_str += '\n\\includegraphics[scale=0.25]{' + picture_path + '}\n'
    make_tex_file('medium_task', list_str)


def main():
    n = 7
    lst = [[str(x * y) for x in range(1, n)] for y in range(1, 2 * n)]
    lst.append(['help' + str(i) for i in range(10)])
    medium_task('AST.png', lst)


if __name__ == '__main__':
    main()
