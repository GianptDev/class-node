

# -------------------------------------------------


from nodeclass.tree import *
from nodeclass.chain import *


# -------------------------------------------------


def main() -> None:

	n = ChainNode("start")

	n.get_end().add_child(ChainNode())
	n.get_end().add_child(ChainNode())
	n.get_end().add_child(ChainNode("middle"))
	n.get_end().add_child(ChainNode())
	n.get_end().add_child(ChainNode())
	n.get_end().add_child(ChainNode("end"))
	print(n.repr_chain())

	return

	# Make a new node
	n = TreeNode(name = "root")

	for a in range(4):
		n.add_child(TreeNode())
	
	for a in range(4):
		n.get_child(0).add_child(TreeNode())
	
	for a in range(2):
		n.get_child(1).add_child(TreeNode())

	print(n.repr_tree())
	print(n.get_child(0,0).repr_path())

	#n.get_child(0, 0).swap_node(n)
	#print(n.repr_tree())


# -------------------------------------------------


if (__name__ == "__main__"):
	main()


# -------------------------------------------------

