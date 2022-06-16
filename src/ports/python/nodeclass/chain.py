"""
Chain Node,
allow chained objects in a linear pattern.

Each node has a single parent and a single child
ordered from a starting node to a final node.

- since: 1.0
"""

# -------------------------------------------------


class ChainNode():


	# -------------------------------------------------
	

	def __init__(self) -> None:
		self._parent: ChainNode = None
		self._child: ChainNode = None
		self._name: str = ""


	def add_node(self, node: "ChainNode") -> None:
		pass

	def remove_parent(self) -> None:
		pass

	def remove_child(self) -> None:
		pass
	
	
	def get_node(self, index: "int") -> "ChainNode":
		pass


# -------------------------------------------------

