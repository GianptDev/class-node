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
	"""
	The Node class object, it allow to connect and be connected with other nodes.

	When a connection happen the child, who is being connected, get the reference of the parent, who started the connection, and the parent get a reference of the child.

	Inside a connection group is possible for any object to get any other object by travelling with a path or index structure.

	- Since: 1.0
	"""


	# -------------------------------------------------
	

	def __init__(self, name: str = "Node") -> None:
		self._parent: ChainNode = None
		self._child: ChainNode = None
		self._name: str = name


	def __repr__(self) -> "str":
		return self.repr()
	

	def __iter__(self) -> "ChainNode":

		for child in self.get_path(to_end = True):
			yield child


	# -------------------------------------------------


	@property
	def parent(self) -> "ChainNode":
		"""
		The previus node wich the current node has been connected to.

		- since: 1.0
		"""

		return self._parent
	

	@property
	def child(self) -> "ChainNode":
		"""
		The next node with has been connected to the current node.

		- since: 1.0
		"""

		return self._child
	

	@property
	def name(self) -> "str":
		"""
		Unique string name identifier of the current node.

		- since: 1.0
		"""

		return self._name
	

	@name.setter
	def name(self, name: "str") -> None:
		self.rename(name)


	# -------------------------------------------------


	def _free(self) -> None:
		"""
		Executed before the current Node remove all references to itself to any other Node is connected to it.

		- Virtual
		- Since: 1.0
		"""

		pass


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


	def free(self) -> None:
		"""
		Will help you to remove all references of the current Node from any connection.

		Here the order of what will happen when executed:
		1. Will first execute the same method to all childrens, make sure to remove them before executing this method if you wish to keep them.
		2. Will execute the `_free` virtual.
		3. Will disconnect from the parent.
		
		After that you can destroy the object with no problem.
		- Since: 1.0
		"""
		
		for c in self.get_path(to_end = True):
			c.free()

		self._free()

		if (self._parent != None):
			self._parent.remove_child()


	def rename(self, name: "str") -> None:
		new_name: str = name
		count: int = 0

		while(True):
			found: bool = False

			for n in self.get_start().get_path(to_end = True):

				if ((n != self) and (n._name == new_name)):
					found = True
					break
			
			if (found == True):
				count += 1
				new_name = f"{name}{count}"
			else:
				name = new_name
				break


		self._name = name


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
		node.rename(node._name)	# Make sure to update name.
		node._parent_changed()
		self._child_changed()


	def remove_parent(self) -> None:
		"""
		Disconnect the current Node from his parent.

		- Since: 1.0
		"""
		
		if (self._parent == None):
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

		if (self._child == None):
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

	
	def get_chain(self, index: Union["int", "str"]) -> Union["ChainNode", None]:
		"""
		Get a node relative from the current node.

		If index is a positive number the function return a node forward from the current node.
		
		If index is a negative number the function return a node forward from the current node.

		If index is a string the function return the only node he can find in the whole chain with that name.

		- Since: 1.0
		"""

		node: ChainNode = self

		if (isinstance(index, int) == True):

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
		
		elif (isinstance(index, str) == True):

			for n in self.get_start().get_path(to_end = True):

				if (n._name == index):
					node = n
					break

		else:
			raise Exception("Invalid type '{type}' used in index.".format(
				type = type(index).__name__
			))

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
		
		- since: 1.0
		"""

		return "<{node_class}:{node_index}:'{node_name}'>".format(
			node_class = type(self).__name__,
			node_index = self.get_index(),
			node_name = self._name
		)
	

	def repr_chain(self) -> "str":
		"""
		Convert the current chain structure into a fancy string.

		Returns:
			The string with a rappresentation of the chain.

		- since: 1.0
		"""

		string = self.repr()

		for n in self.get_path(to_end = True):
			string = "%s\n\t%s" % (
				string,
				n.repr()
			)
		
		return string


# -------------------------------------------------

