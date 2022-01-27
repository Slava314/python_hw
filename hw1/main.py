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
node_names = {}


def visit_node(gv, node, name):
	counter = next(gen_num)
	node_names[counter] = str(counter) + ': ' + name
	g.add_node(counter)
	lst = gv.generic_visit(node)
	g.add_edges_from(map(lambda x: (counter, x), lst))
	return counter


class GraphVisitor(ast.NodeVisitor):

	def visit_FunctionDef(self, node):
		return visit_node(self, node, "function '{}'".format(node.name))

	def visit_arguments(self, node):
		return visit_node(self, node, 'arguments')

	def visit_For(self, node):
		return visit_node(self, node, 'for cycle')

	def visit_Return(self, node):
		return visit_node(self, node, 'return')

	def visit_Name(self, node):
		return visit_node(self, node, "variable '{}'".format(node.id))

	def visit_BinOp(self, node: ast.BinOp):
		return visit_node(self, node, 'bin op')

	def visit_Add(self, node):
		return visit_node(self, node, 'add')

	def visit_Assign(self, node):
		return visit_node(self, node, 'assign')

	def visit_arg(self, node):
		return visit_node(self, node, "variable '{}'".format(node.arg))

	def visit_List(self, node):
		return visit_node(self, node, 'list')

	def visit_Constant(self, node):
		return visit_node(self, node, "constant '{}'".format(node.value))

	def visit_Expr(self, node: ast.Expr):
		return visit_node(self, node, 'expr')

	def visit_Call(self, node: ast.Call):
		return visit_node(self, node, 'call')

	def visit_Sub(self, node: ast.Sub):
		return visit_node(self, node, 'sub')

	def visit_Attribute(self, node: ast.Attribute):
		return visit_node(self, node, 'attribute')

	def visit_Subscript(self, node: ast.Subscript):
		return visit_node(self, node, 'subscript')

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
	g1 = nx.relabel_nodes(g, node_names)
	g2 = nx.dfs_tree(g1)
	g3 = nx.drawing.nx_agraph.to_agraph(g2)
	pos = g3.layout('dot')
	g3.draw('artifacts/AST.png', format='png')
	#nx.draw(g2, with_labels=True)
	#plt.savefig("artifacts/AST.png")
	print(ast.dump(tree, indent=4))
	print(ast.dump(tree))


if __name__ == "__main__":
	main()
