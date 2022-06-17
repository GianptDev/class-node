"""
Tree Node,
allow chained objects in a tree-like pattern.

Each node can have one parent and multiple childrens
ordered in a hierarchy starting from a single node called root.

- since: 1.0
"""


# -------------------------------------------------


from typing import Union


# -------------------------------------------------


NODE_NO_INDEX: "int" = -1
"""
The index of a Node with no parent.

- Since: 1.0
"""


# -------------------------------------------------



class NodeWalkIterator():
	"""
	This is an iterator used by the walk methods of the Node.

	- Since: 1.0
	"""

	def __init__(self, path: list["TreeNode"], node: "TreeNode") -> None:

		self.path: list[TreeNode]  = path
		"""
		The path from the caller to reach node.
		"""

		self.node: TreeNode = node
		"""
		The current node target of this iteration.
		"""


# -------------------------------------------------


class TreeNode():
	"""
	The Node class object, it allow to connect and be connected with other nodes.

	When a connection happen the child, who is being connected, get the reference of the parent, who started the connection, and the parent get a reference of the child.

	Inside a connection group is possible for any object to get any other object by travelling with a path or index structure.

	- Since: 1.0
	"""


	# -------------------------------------------------


	def __init__(self, name: "str" = "Node") -> None:
		self._parent: TreeNode = None
		self._childrens: list[TreeNode]  = []
		self._name: str = name


	def __repr__(self) -> "str":
		return self.repr()
	

	def __iter__(self) -> "TreeNode":

		for child in self._childrens:
			yield child
	

	def __len__(self) -> "int":
		return len(self._childrens)


	# -------------------------------------------------


	@property
	def parent(self) -> "TreeNode":
		"""
		The Node object wich the current Node is child of.

		- The property is stored as `_parent`, if you edit it directly it may cause desync between Nodes.
		"""

		return self._parent


	@property
	def childrens(self) -> list["TreeNode"]:
		"""
		The list of Node objects wich are childrens of the current Node.

		The property is stored as `_childrens`, if you edit it directly it may cause desync between Nodes.

		- Since: 1.0
		"""

		return self._childrens


	@property
	def name(self) -> "str":
		"""
		The unique name of the current Node, it will automatically rename itself if the current Node become the child of a parent Node with already another child with the same name.

		The property is stored as `_name`, if you edit it directly it may cause desync between Nodes.

		- Since: 1.0
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
	

	def _renamed(self) -> None:
		"""
		Executed after the current Node has been manually renamed with `rename` or automatically to make his name unique.

		- Virtual
		- Since: 1.0
		"""
		pass


	def _changed_parent(self) -> None:
		"""
		Executed after the parent of the current Node has changed or removed.

		- Virtual
		- Since: 1.0
		"""
		
		pass


	def _add_child(self, child: "TreeNode") -> None:
		"""
		Executed after a new node has been parented as a child.

		Params:
			`child` Node: The child just added.

		- Virtual
		- Since: 1.0
		"""

		pass


	def _removed_child(self, child: "TreeNode") -> None:
		"""
		Executed after a node has been unparented from being a child.

		Params:
			`child` Node: The child just removed.

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
		
		for c in tuple(self._childrens):
			c.free()

		self._free()

		if (self._parent != None):
			self._parent.remove_child(self)
	

	def rename(self, name: "str") -> None:
		"""
		Will change the name of the current node and execute the `_renamed` virtual after.

		If the name is already used by another child it will start a counter to find an new unique name.

		Params:
			`name` str: The new desired name.
		
		- Since: 1.0
		"""

		if (self._parent != None):
			fix_name: str = name
			count: int = 0

			while(True):
				found: bool = False

				for child in self._parent._childrens:

					if ((child != self) and (fix_name == child._name)):
						found = True
						break
				
				if (found == True):
					count += 1
					fix_name = f"{name}{count}"
				else:
					name = fix_name
					break
		
		self._name = name
		self._renamed()


	def remove(self) -> None:
		"""
		Will unparent itself from the parent Node.
		
		If no parent exist it will throw an exception.
		- Since: 1.0
		"""

		if (self._parent == None):
			raise Exception("The current Node is not parented whit a Node.")
		
		self._parent.remove_child(self)
	

	def move(self, index: "int") -> None:
		"""
		Will move his index position inside the childrens vector from the parent Node.

		If no parent exist it will throw an exception.

		Params:
			`index` int: the desired index position.
		
		- Since: 1.0
		"""

		if (self._parent == None):
			raise Exception("The current Node is not parented whit a Node.")
		
		self._parent.move_child(self, index)


	def add_child(self, node: "TreeNode", index: "int" = -1) -> None:
		"""
		Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.

		If the input Node is already parented with another Node or is invalid an exception will throw.

		Params:
			`node` Node: The new node to parent.
			`index` int: Optional index of his position, by default is appended to end.
		
		- Since: 1.0
		"""

		if (isinstance(node, TreeNode) == False):
			raise Exception("Tried to add class type '{type}' instead of '{node}' base class.".format(
				type = type(node).__name__,
				node = type(self).__name__
			))
		
		if (node == self):
			raise Exception("You can't parent a Node with itself.")
		
		if (node._parent != None):
			raise Exception("Tried to add as a child a Node already parented with a Node.")

		c_size: int = len(self._childrens)
		
		if (index >= 0):
			if (index > c_size):
				index = c_size
		else:
			if (-index > c_size):
				index = 0
			else:
				index = c_size + index + 1
		
		self._childrens.insert(index, node)
		node._parent = self
		node.rename(node._name)	# Make sure to update name.
		node._changed_parent()
		self._add_child(node)


	def remove_child(self, child: "TreeNode") -> None:
		"""
		Will remove the input Node from being the parent of the current Node and will remove it from the childrens list.

		If the input Node is not parented with the current Node or is invalid an exception will throw. 

		Params:
			`node` Node: The child to remove.
		
		- Since: 1.0
		"""
		
		if (isinstance(child, TreeNode) == False):
			raise Exception("Tried to remove class type '{type}' instead of '{node}' base class.".format(
				type = type(child).__name__,
				node = type(self).__name__
			))
		
		if (child._parent != self):
			raise Exception("Tried to remove a Node wich isn't connected to the current Node.")
		
		child._parent = None
		del self._childrens[self._childrens.index(child)]
		child._changed_parent()
		self._removed_child(child)


	def move_child(self, child: "TreeNode", index: "int") -> None:
		"""
		Will move the index position of the input Node inside the current Node.

		If the input Node is not parented with the current Node or is invalid an exception will throw. 

		Params:
			`node` Node: The child to move.
			`index` int: The new index position.
		
		- Since: 1.0
		"""

		if (isinstance(child, TreeNode) == False):
			raise Exception("Tried to move class type '{type}' instead of '{node}' base class.".format(
				type = type(child).__name__,
				node = type(self).__name__
			))

		if (child._parent != self):
			raise Exception("Tried to move a Node wich isn't connected to the current Node.")
		
		del self._childrens[self._childrens.index(child)]
		self._childrens.insert(index, child)


	# -------------------------------------------------


	def get_index(self) -> "int":
		"""
		Get the index position inside the parent list of the current Node.
		
		Returns:
			The index position of the curret Node or `NODE_NO_INDEX` if no parent exist.
		
		- Since: 1.0
		"""
		
		return NODE_NO_INDEX if (self._parent == None) else self._parent._childrens.index(self)


	def get_root(self) -> "TreeNode":
		"""
		Will get the top-level Node wich is parented with all the Nodes of the current tree.

		- Since: 1.0
		"""

		node: TreeNode = self

		while(node._parent != None):
			node = node._parent
		
		return node


	def get_path(self) -> "tuple":
		"""
		Get the reference of all Nodes between the root Node and the current Node.

		- Since: 1.0
		"""

		path: tuple = ()
		node: TreeNode = self

		while(node.parent != None):
			node = node.parent
			path = (node, *path)
		
		return path


	def get_child_count(self) -> "int":
		"""
		Will give the total amount of childrens parented with the current Node.
		
		Returns:
			The size of childrens list.
		
		- since: 1.0
		"""
		
		return len(self._childrens)


	def get_child(self, *path: Union["int", "str"]) -> Union["TreeNode", None]:
		"""
		Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).

		The path allow multiple types to get nodes:
		- int: The index position inside the list, positive numbers will get the item from the begin to the end and negative numbers will get the item from the end to the begin.
		- str: The unique name of the node.

		Params:
			`path` (int|string)

		Returns:
			The found Node or `None` if not found.
		
		- Since: 1.0
		"""

		current: TreeNode = self
		node: TreeNode = None

		for p in path:
			
			if (isinstance(p, int) == True):
				c_size: int = len(current._childrens)
				
				if (p >= 0):
					if (p > (c_size - 1)):
						return None
					else:
						current = current._childrens[p]
				
				else:
					if (-p > c_size):
						return None
					else:
						current = current._childrens[c_size + p]
				
				node = current
			
			elif (isinstance(p, str) == True):
				found: bool = False

				for c in current._childrens:

					if (c._name == p):
						found = True
						current = c
						node = c
						break
				
				if (found == False):
					return None
			
			else:
				raise Exception("Invalid type '{type}' used in path.".format(
					type = type(p).__name__
				))

		return node


	def walk_base(self, inverse: "bool" = False) -> list[NodeWalkIterator]:
		"""
		Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.

		It will first get all the childrens before the sub-childrens.

		Params:
			`inverse` (bool): Will invert the iteration from top-down to bottom-up.
		
		Returns:
			List of all iterators.
		
		- Since: 1.0
		"""

		child_list: list[TreeNode]  = self._childrens if (inverse == False) else self._childrens[::-1]
		walk: list[NodeWalkIterator] = []

		for child in child_list:
			step: NodeWalkIterator = NodeWalkIterator([self], child)
			walk.append(step)

		for child in child_list:

			for iter in child.walk_base(inverse = inverse):
				iter.path.append(self)
				walk.append(iter)

		return walk
	

	def walk_tree(self, inverse: "bool" = False) -> list[NodeWalkIterator]:
		"""
		Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.

		It will get childrens and sub-childrens sequencially.

		Params:
			`inverse` (bool): Will invert the iteration from top-down to bottom-up.
		
		Returns:
			List of all iterators.
		
		- Since: 1.0
		"""
		
		child_list: list[TreeNode]  = self._childrens if (inverse == False) else self._childrens[::-1]
		walk: list[NodeWalkIterator] = []

		for child in child_list:
			step: NodeWalkIterator = NodeWalkIterator([self], child)
			walk.append(step)
			
			for iter in child.walk_tree(inverse = inverse):
				iter.path.append(self)
				walk.append(iter)

		return walk
	

	def repr(self) -> "str":
		"""
		Convert the current Node into a string.

		Returns:
			The string with a rappresentation of the current Node.
		
		- Since: 1.0
		"""

		return "<{node_class}:'{node_name}'>".format(node_class = type(self).__name__,node_name = self._name)


	def repr_tree(self) -> "str":
		"""
		Convert the current Node structure into a fancy string.

		Returns:
			The string with a rappresentation of the tree.
		
		- Since: 1.0
		"""

		string: str = ("%s/" if (len(self._childrens) > 0) else "%s") % self.repr()
		
		for iter in self.walk_tree():
			string = ("%s\n%s%s/" if (len(iter.node._childrens) > 0) else "%s\n%s%s") % (
				string,
				("\t" * len(iter.path)),
				iter.node.repr()
			)

		return string
	

	def repr_path(self, arrow: "str" = " => ") -> "str":
		"""
		Convert the path of the current Node into a fancy string, you can put a string between each name.

		Params:
			`arrow` (str): A custom string added in between of each node rappresented.

		Returns:
			The string with a rappresentation of the path, current node is excluded.
		
		- since: 1.0
		"""

		string: str = ""

		# string = arrow.join(p.repr() for p in self.get_path()) #USE LATER

		for p in self.get_path():

			if (string != ""):
				string += arrow

			string += p.repr()
		
		return string


# -------------------------------------------------

