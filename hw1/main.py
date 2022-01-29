from fib import fib
import ast
import networkx as nx
import inspect


def get_name(node):
    return node.__class__.__name__


class GraphVisitor(ast.NodeVisitor):

    def __init__(self):
        self.counter = 0
        self.g = nx.Graph()
        self.node_attr = {}

    def visit_FunctionDef(self, node):
        return self.visit_node(node, "Function '{}'".format(node.name), color='lemonchiffon', shape='rectangle')

    def visit_arguments(self, node):
        return self.visit_node(node, get_name(node), color='lightblue1', shape='rectangle')

    def visit_For(self, node):
        return self.visit_node(node, get_name(node) + ' cycle', color='lightcyan1', shape='rectangle')

    def visit_Return(self, node):
        return self.visit_node(node, get_name(node), color='slategray1', shape='rectangle')

    def visit_Name(self, node):
        return self.visit_node(node, "Variable '{}'".format(node.id), color='pink')

    def visit_BinOp(self, node):
        return self.visit_node(node, get_name(node), color='peachpuff1', shape='rectangle')

    def visit_Add(self, node):
        return self.visit_node(node, get_name(node), color='peachpuff1')

    def visit_Assign(self, node):
        return self.visit_node(node, get_name(node), color='papayawhip', shape='rectangle')

    def visit_arg(self, node):
        return self.visit_node(node, "Variable '{}'".format(node.arg), color='pink')

    def visit_List(self, node):
        return self.visit_node(node, get_name(node), color='lightyellow1', shape='rectangle')

    def visit_Constant(self, node):
        return self.visit_node(node, "{} '{}'".format(get_name(node), node.value), color='lightsteelblue1')

    def visit_Expr(self, node):
        return self.visit_node(node, get_name(node), color='grey90', shape='rectangle')

    def visit_Call(self, node):
        return self.visit_node(node, get_name(node), color='lightgoldenrod1', shape='rectangle')

    def visit_Sub(self, node):
        return self.visit_node(node, get_name(node), color='peachpuff1')

    def visit_Attribute(self, node):
        return self.visit_node(node, "{}: '{}'".format(get_name(node), node.attr), color='powderblue',
                               shape='rectangle')

    def visit_Subscript(self, node):
        return self.visit_node(node, get_name(node), color='grey90', shape='rectangle')

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

    def visit_node(self, node, name, color='white', shape='ellipse'):
        self.counter += 1
        counter = self.counter
        self.node_attr[counter] = {'style': 'filled', 'fillcolor': color, 'label': name, 'shape': shape}
        self.g.add_node(counter)
        lst = self.generic_visit(node)
        self.g.add_edges_from(map(lambda x: (counter, x), lst))
        return counter


def main():
    source = inspect.getsource(fib)
    tree = ast.parse(source)
    visitor = GraphVisitor()
    visitor.visit(tree)
    vis_g = nx.drawing.nx_agraph.to_agraph(nx.dfs_tree(visitor.g))
    for node in vis_g.nodes():
        for key, value in visitor.node_attr[int(node)].items():
            node.attr[key] = value
    pos = vis_g.layout('dot')
    vis_g.draw('artifacts/AST.png', format='png')


if __name__ == "__main__":
    main()
