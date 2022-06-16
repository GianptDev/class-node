"""
Chain Node,
allow chained objects in a linear pattern.

Each node has a single parent and a single child
ordered from a starting node to a final node.

- since: 1.0
"""

# -------------------------------------------------


from typing import Union


# -------------------------------------------------


class ChainNode():


	# -------------------------------------------------
	

	def __init__(self) -> None:
		self._parent: ChainNode = None
		self._child: ChainNode = None


	# -------------------------------------------------


	@property
	def parent(self) -> "ChainNode":
		return self._parent
	

	@property
	def child(self) -> "ChainNode":
		return self._child


	# -------------------------------------------------


	def _parent_changed(self) -> None:
		"""
		Executed after the parent of the current Node has changed or removed.

		- Virtual
		- Since: 1.0
		"""

		pass
	

	def _child_changed(self) -> None:
		"""
		Executed after the child of the current Node has changed or removed.

		- Virtual
		- Since: 1.0
		"""

		pass


	# -------------------------------------------------


	def add_child(self, node: "ChainNode") -> None:
		"""
		Connect node as a child of the current Node.

		If a child already exist, an exception is raised.

		- Since: 1.0
		"""

		if (node == None):
			raise Exception("Tried to add None as a child.")

		if (self._child != None):
			raise Exception("Another child is already connected to this Node.")
		
		node._parent = self
		self._child = node
		node._parent_changed()
		self._child_changed()


	def remove_parent(self) -> None:
		"""
		Disconnect the current Node from his parent.

		- Since: 1.0
		"""
		
		if (self._parent != None):
			raise Exception("The current Node is not connected to a parent.")
		
		parent = self._parent

		self._parent = None
		parent._child = None
		self._parent_changed()
		parent._child_changed()


	def remove_child(self) -> None:
		"""
		Disconnect the current Node from his child.
		"""

		if (self._parent != None):
			raise Exception("The current Node is not connected to a child.")
		
		child = self._child

		self._child = None
		child._parent = None
		self._child_changed()
		child._parent_changed()
	

	# -------------------------------------------------


	def get_start(self) -> "ChainNode":
		"""
		The the first Node of the whole chain structure.
		"""

		node: ChainNode = self

		while(node._parent != None):
			node = node._parent
		
		return node
	

	def get_end(self) -> "ChainNode":
		"""
		The the last Node of the whole chain structure.
		"""

		node: ChainNode = self

		while(node._child != None):
			node = node._child
		
		return node

	
	def get_next(self, skip: "int" = 0) -> Union["ChainNode", None]:
		"""
		Get a child Node from the current Node or from another child.
		"""

		pass
	

	def get_previus(self, skip: "int" = 0) -> Union["ChainNode", None]:
		"""
		Get a parent Node from the current Node or from another parent.
		"""
		
		pass
	

	def get_path(self, inverse: "bool" = False) -> list["ChainNode"]:
		"""
		Will get all the nodes between the current Node and the fist Node, or from the current Node to the last Node.

		Params:
			`inverse` (bool): If enabled will get the path to the last Node.
		"""

		pass


# -------------------------------------------------

