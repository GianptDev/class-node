

# -------------------------------------------------


from nodeclass.tree import TreeNode as Node


# -------------------------------------------------


def main() -> None:

	# Make a new node
	n = Node(name = "root")

	for a in range(4):
		n.add_child(Node())
	
	for a in range(4):
		n.get_child(0).add_child(Node())
	
	for a in range(2):
		n.get_child(1).add_child(Node())

	print(n.repr_tree())
	print(n.get_child(0,0).repr_path())

	#n.get_child(0, 0).swap_node(n)
	#print(n.repr_tree())


# -------------------------------------------------


if (__name__ == "__main__"):
	main()


# -------------------------------------------------

