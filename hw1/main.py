from fib import fib
import ast
import networkx as nx
import inspect


def get_num():
    x = 0
    while True:
        x += 1
        yield x


gen_num = get_num()
g = nx.Graph()
node_attr = {}


def get_name(node):
    return node.__class__.__name__


def visit_node(gv, node, name, color='white', shape='ellipse'):
    counter = next(gen_num)
    node_attr[counter] = {'style': 'filled', 'fillcolor': color, 'label': name, 'shape': shape}
    g.add_node(counter)
    lst = gv.generic_visit(node)
    g.add_edges_from(map(lambda x: (counter, x), lst))
    return counter


class GraphVisitor(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        return visit_node(self, node, "Function '{}'".format(node.name), color='lemonchiffon', shape='rectangle')

    def visit_arguments(self, node):
        return visit_node(self, node, get_name(node), color='lightblue1', shape='rectangle')

    def visit_For(self, node):
        return visit_node(self, node, get_name(node) + ' cycle', color='lightcyan1', shape='rectangle')

    def visit_Return(self, node):
        return visit_node(self, node, get_name(node), color='slategray1', shape='rectangle')

    def visit_Name(self, node):
        return visit_node(self, node, "Variable '{}'".format(node.id), color='pink')

    def visit_BinOp(self, node: ast.BinOp):
        return visit_node(self, node, get_name(node), color='peachpuff1', shape='rectangle')

    def visit_Add(self, node):
        return visit_node(self, node, get_name(node), color='peachpuff1')

    def visit_Assign(self, node):
        return visit_node(self, node, get_name(node), color='papayawhip', shape='rectangle')

    def visit_arg(self, node):
        return visit_node(self, node, "Variable '{}'".format(node.arg), color='pink')

    def visit_List(self, node):
        return visit_node(self, node, get_name(node), color='lightyellow1', shape='rectangle')

    def visit_Constant(self, node):
        return visit_node(self, node, "{} '{}'".format(get_name(node), node.value), color='lightsteelblue1')

    def visit_Expr(self, node: ast.Expr):
        return visit_node(self, node, get_name(node), color='grey90', shape='rectangle')

    def visit_Call(self, node: ast.Call):
        return visit_node(self, node, get_name(node), color='lightgoldenrod1', shape='rectangle')

    def visit_Sub(self, node: ast.Sub):
        return visit_node(self, node, get_name(node), color='peachpuff1')

    def visit_Attribute(self, node: ast.Attribute):
        return visit_node(self, node, "{}: '{}'".format(get_name(node), node.attr), color='powderblue', shape='rectangle')

    def visit_Subscript(self, node: ast.Subscript):
        return visit_node(self, node, get_name(node), color='grey90', shape='rectangle')

    def generic_visit(self, node):
        lst = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        c = self.visit(item)
                        if not isinstance(c, list):
                            lst.append(c)
            elif isinstance(value, ast.AST):
                c = self.visit(value)
                if not isinstance(c, list):
                    lst.append(c)
        return lst


def main():
    source = inspect.getsource(fib)
    tree = ast.parse(source)
    visitor = GraphVisitor()
    visitor.visit(tree)
    g2 = nx.dfs_tree(g)
    g3 = nx.drawing.nx_agraph.to_agraph(g2)
    for node in g3.nodes():
        for key, value in node_attr[int(node)].items():
            node.attr[key] = value
    pos = g3.layout('dot')
    g3.draw('artifacts/AST.png', format='png')


if __name__ == "__main__":
    main()
