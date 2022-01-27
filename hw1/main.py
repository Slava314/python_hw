from fib import fib
import ast
import networkx as nx
import matplotlib.pyplot as plt
import inspect


def get_num():
	x = 0
	while True:
		x += 1
		yield x


gen_num = get_num()
g = nx.Graph()
node_names = {}


def get_name(node):
	return node.__class__.__name__


def visit_node(gv, node, name):
	counter = next(gen_num)
	node_names[counter] = name
	g.add_node(counter)
	lst = gv.generic_visit(node)
	g.add_edges_from(map(lambda x: (counter, x), lst))
	return counter


class GraphVisitor(ast.NodeVisitor):

	def visit_Module(self, node: ast.Module):
		return visit_node(self, node, 'module')

	def visit_FunctionDef(self, node: ast.FunctionDef):
		return visit_node(self, node, "function '{}'".format(node.name))

	def visit_arguments(self, node: ast.arguments):
		return visit_node(self, node, get_name(node))

	def visit_For(self, node: ast.For):
		return visit_node(self, node, 'for cycle')

	def visit_Return(self, node):
		return visit_node(self, node, 'return')

	def visit_Name(self, node: ast.Name):
		return visit_node(self, node, "variable '{}'".format(node.id))

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
	#print(node_names)
	g1 = nx.relabel_nodes(g, node_names)
	g2 = nx.dfs_tree(g1)
	print(ast.dump(tree, indent=4))
	print(ast.dump(tree))
	#subax1 = plt.subplot(121)
	nx.draw(g2, with_labels=True)
	#plt.show()
	plt.savefig("artifacts/AST.png")


if __name__ == "__main__":
	main()
