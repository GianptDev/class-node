"""
Relation Node,
allow chained objects in a relative pattern.

Each Node can have multiple parents and childrens
the order is relative because there is no start or end node.

- since: 1.0
"""


# -------------------------------------------------


from typing import Union


# -------------------------------------------------


class RelationNode():


	# -------------------------------------------------


	def __init__(self) -> None:
		self._parents: list[RelationNode] = []
		self._childrens: list[RelationNode] = []
		self._index: int = -1
		self._name: str = ""
	

	def get_parent(self, *path: Union["int", "str"]) -> "RelationNode" | None:
		pass
	
	def get_child(self, *path: Union["int", "str"]) -> "RelationNode" | None:
		pass


# -------------------------------------------------

