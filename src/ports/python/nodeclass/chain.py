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
	

	def __init__(self, name: str = "Node") -> None:
		self._parent: ChainNode = None
		self._child: ChainNode = None
		self._name: str = name


	def __repr__(self) -> "str":
		return self.repr()
	

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
			raise Exception("Tried to add 'None' as a child.")

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

		- Since: 1.0
		"""

		if (self._parent != None):
			raise Exception("The current Node is not connected to a child.")
		
		child = self._child

		self._child = None
		child._parent = None
		self._child_changed()
		child._parent_changed()
	

	# -------------------------------------------------


	def get_index(self) -> "int":
		"""
		Get the index position inside the chain from the start to the current position.

		Returns:
			Integer of the current position, it will start from 0.
		
		- Since: 1.0
		"""

		index: int = 0
		current: ChainNode = self

		while(current._parent != None):
			index += 1
			current = current._parent
		
		return index


	def get_start(self) -> "ChainNode":
		"""
		The the first Node of the whole chain structure.

		Returns:
			The current Node or the first node of the chain.
		
		- Since: 1.0
		"""

		node: ChainNode = self

		while(node._parent != None):
			node = node._parent
		
		return node
	

	def get_end(self) -> "ChainNode":
		"""
		The the last Node of the whole chain structure.

		Returns:
			The current Node or the last node of the chain.
		
		- Since: 1.0
		"""

		node: ChainNode = self

		while(node._child != None):
			node = node._child
		
		return node

	
	def get_chain(self, index: "int") -> Union["ChainNode", None]:
		"""
		Get a node by skipping index amount going backwards or forwards from the current Node.

		Returns:
			The found node after the amount of steps or None if the index position does not exist and is outside the chain.

		- Since: 1.0
		"""

		node: ChainNode = self

		if (index >= 0):

			for n in range(index):

				if (node._child != None):
					node = node._child
				else:
					return None
		else:
			index = -index

			for n in range(index):

				if (node._parent != None):
					node = node._parent
				else:
					return None

		return node
	

	def get_path(self, to_end: "bool" = False) -> tuple["ChainNode"]:
		"""
		Will get all the nodes between the current Node and the fist Node, or from the current Node to the last Node.

		Params:
			`to_end` (bool): If enabled will get the path to the last Node.
		
		- Since: 1.0
		"""

		path: tuple[ChainNode] = ()
		current: ChainNode = None

		if (to_end == False):
			current = self._parent
			
			while(current != None):
				path = (*path, current)
				current = current._parent
		
		else:
			current = self._child
			
			while(current != None):
				path = (*path, current)
				current = current._child

		return path


	def repr(self) -> "str":
		"""
		Convert the current node into a string.

		Returns:
			The string with a rappresentation of the current Node.
		
		- Since: 1.0
		"""

		return "<{node_class}:{node_index}>".format(node_class = type(self).__name__, node_index = self.get_index())


# -------------------------------------------------

