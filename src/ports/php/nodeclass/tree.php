<?php


	/**
	 * Tree Node,
	 * allow chained objects in a tree-like pattern.
	 * 
	 * Each node can have one parent and multiple childrens
	 * ordered in a hierarchy starting from a single node called root.
	 */


	# -------------------------------------------------


	namespace nodeclass;
	use Exception;
	

	# -------------------------------------------------


	/**
	 * The index of a Node with no parent.
	 * 
	 * @since 1.0
	 */
	const NODE_NO_INDEX = -1;


	# -------------------------------------------------


	/**
	 * This is an iterator used by the walk methods of the Node.
	 * 
	 * @since 1.0
	 */
	class NodeWalkIterator
	{
		public array $path;
		public TreeNode $node;

		public function __construct(array $path, TreeNode $node)
		{
			$this->path = $path;
			$this->node = $node;
		}
	}


	# -------------------------------------------------


	/**
	 * This is the base class of a Node, it contain all the base logic for parenting and building a tree objects structure.
	 * 
	 * These structures start with an initial Node called `root` and extend into a list of `childrens` and `parents` with more `childrens` parented with it.
	 * 
	 * @since 1.0
	 */
	class TreeNode
	{


		# -------------------------------------------------


		/**
		 * The Node object wich the current Node is child of.
		 * 
		 * @since 1.0
		 */
		private ?TreeNode $parent;


		/**
		 * The list of Node objects wich are childrens of the current Node.
		 * 
		 * @since 1.0
		 */
		private array $childrens;


		/**
		 * The unique name of the current Node, it will automatically rename itself if the current Node become the child of a parent Node with already another child with the same name.
		 * 
		 * @since 1.0
		 */
		private String $name;


		# -------------------------------------------------


		public function __construct(String $name = "Node")
		{
			$this->childrens = [];
			$this->parent = null;
			$this->name = $name;
		}


		public function __toString() : string
		{
			return $this->repr();
		}


		# -------------------------------------------------


		/**
		 * Executed before the current Node remove all references to itself to any other Node is connected to it.
		 * 
		 * @virtual
		 * @since 1.0
		 */
		private function _free() : void {}


		/**
		 * Executed after the current Node has been manually renamed with `rename` or automatically to make his name unique.
		 *  
		 * @virtual
		 * @since 1.0
		 */
		private function _renamed() : void {}


		/**
		 * Executed after the parent of the current Node has changed or removed.
		 * 
		 * @virtual
		 * @since 1.0
		 */
		private function _changed_parent() : void {}


		/**
		 * Executed after a new node has been parented as a child.
		 * 
		 * @virtual
		 * @since 1.0
		 */
		private function _add_child(TreeNode $node) : void {}


		/**
		 * Executed after a node has been unparented from being a child.
		 * 
		 * @virtual
		 * @since 1.0
		 */
		private function _removed_child(TreeNode $node) : void {}


		# -------------------------------------------------


		/**
		 * Will help you to remove all references of the current Node from any connection.
		 * 
		 * Here the order of what will happen when executed:
		 * 1. Will first execute the same method to all childrens, make sure to remove them before executing this method if you wish to keep them.
		 * 2. Will execute the `_free` virtual.
		 * 3. Will disconnect from the parent.
		 * 
		 * After that you can destroy the object with no problem.
		 * 
		 * @since 1.0
		 */
		public final function free() : void
		{
			foreach($this->childrens as $child)
			{
				$child->free();
			}

			$this->_free();

			if(is_null($this->parent) == false) {
				$this->parent->remove_child($this);
			}
		}


		/**
		 * Will change the name of the current node and execute the `_renamed` virtual after.
		 * 
		 * If the name is already used by another child it will start a counter to find an new unique name.
		 * 
		 * @since 1.0
		 */
		public final function rename(String $name) : void
		{

			if (is_null($this->parent) == false)
			{
				$fix_name = $name;
				$count = 0;

				while(true)
				{
					$found = false;

					foreach ($this->parent->childrens as $child)
					{
						if (($child !== $this) && (strcmp($fix_name, $child->name) == 0))
						{
							$found = true;
							break;
						}
					}

					if ($found == true) {
						++$count;
						$fix_name = "$name$count";
					} else {
						$name = $fix_name;
						break;
					}
				}
			}
			
			$this->name = $name;
			$this->_renamed();
		}


		/**
		 * Will unparent itself from the parent Node.
		 * 
		 * If no parent exist it will throw an exception.
		 * 
		 * @since 1.0
		 */
		public final function remove() : void
		{
			if (is_null($this->parent) == true) {
				throw new Exception("The current Node is not parented whit a Node.");
			}

			$this->parent->remove_child($this);
		}


		/**
		 * Will move his index position inside the childrens vector from the parent Node.
		 * 
		 * If no parent exist it will throw an exception.
		 * 
		 * @since 1.0
		 */
		public final function move(Int $index) : void
		{
			if (is_null($this->parent) == true) {
				throw new Exception("The current Node is not parented whit a Node.");
			}

			$this->parent->move_child($this, $index);
		}

		
		/**
		 * Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.
		 * 
		 * If the input Node is already parented with another Node or is invalid an exception will throw.
		 * 
		 * @since 1.0
		 */
		public final function add_child(TreeNode $node, Int $index = -1) : void
		{

			if (is_null($node->parent) == false) {
				throw new Exception("Tried to parent a Node wich is already parented with another Node.");
			}

			$c_size = sizeof($this->childrens);

			if ($index >= 0) {
				if ($index > $c_size) {
					$index = $c_size;
				}
			} else {
				if (-$index > $c_size) {
					$index = 0;
				} else {
					$index = $c_size + $index + 1;
				}
			}

			array_splice($this->childrens, $index, 0, [$node]);
			$node->parent = $this;
			$node->rename($node->name);
			$this->_add_child($node);
			$node->_changed_parent();
		}


		/**
		 * Will remove the input Node from being the parent of the current Node and will remove it from the childrens list.
		 * 
		 * If the input Node is not parented with the current Node or is invalid an exception will throw. 
		 * 
		 * @since 1.0
		 */
		public final function remove_child(TreeNode $node) : void
		{

			if ($node->parent != $this) {
				throw new Exception("Tried to move a Node wich isn't connected to the current Node.");
			}

			$node->parent = null;
			array_splice($this->childrens, array_search($node, $this->childrens), 1);
			$this->_removed_child($node);
			$node->_changed_parent();	# [x]: Vscode show an error here but the code actually work, no idea.
										# Error says method not declared but add_child call it with no problem.
		}


		/**
		 * Will move the index position of the input Node inside the current Node.
		 * 
		 * If the input Node is not parented with the current Node or is invalid an exception will throw. 
		 * 
		 * @since 1.0
		 */
		public final function move_child(TreeNode $node, Int $index) : void
		{

			if ($node->parent != $this) {
				throw new Exception("Tried to move a Node wich isn't connected to the current Node.");
			}

			array_splice($this->childrens, $index, 0,	# Insert the Node from the return.
				array_splice($this->childrens,
					array_search($node, $this->childrens),	# Find the Node.
				1)	# Remove and return the Node.
			);
		}


		# -------------------------------------------------


		/**
		 * @return parent The parent of the current Node.
		 * @since 1.0
		 */
		public final function get_parent() : TreeNode
		{
			return $this->parent;
		}


		/**
		 * @return childrens The childrens of the current Node.
		 * @since 1.0
		 */
		public final function get_childrens() : array
		{
			return $this->childrens;
		}


		/**
		 * @return name The name of the current Node.
		 * @since 1.0
		 */
		public final function get_name() : String
		{
			return $this->name;
		}


		/**
		 * Get the index position inside the parent list of the current Node.
		 * 
		 * If the Node is not parented the constant `NODE_NO_INDEX` is returned.
		 * 
		 * @return int The index position in the childrens array.
		 * @return NODE_NO_INDEX If the current Node is not connected with a parent.
		 * @since 1.0
		 */
		public final function get_index() : int
		{
			return (is_null($this->parent) == true) ? NODE_NO_INDEX : array_search($this, $this->childrens);
		}


		/**
		 * Will get the top-level Node wich is parented with all the Nodes of the current tree.
		 * 
		 * @since 1.0
		 */
		public final function get_root() : TreeNode
		{
			$node = $this;

			while(is_null($node->parent) == false)
			{
				$node = $node->parent;
			}

			return $node;
		}


		/**
		 * Get the reference of all Nodes between the root Node and the current Node.
		 * 
		 * @since 1.0
		 */
		public final function get_path() : array
		{
			$path = [];
			$node = $this;

			while(is_null($node->parent) == false)
			{
				$node = $node->parent;
				array_splice($path, 0, 0, [$node]);
			}

			return $path;
		}


		/**
		 * Will give the total amount of childrens parented with the current Node.
		 * 
		 * @return int The size of childrens list.
		 * @since 1.0
		 */
		public final function get_child_count() : int
		{
			return sizeof($this->childrens);
		}


		/**
		 * Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).
		 * 
		 * @param ...path int|string The path from the current Node to the target Node, you can find childrens by their index position or unique name.
		 * 
		 * @return node The found Node or `null` if not found.
		 * @since 1.0
		 */
		public final function get_child(...$path) : ?TreeNode
		{
			$current = $this;
			$node = null;

			foreach($path as $p)
			{
				if (is_int($p) == true)
				{
					$c_size = sizeof($current->childrens);

					if ($p >= 0) {
						if ($p > ($c_size - 1)) {
							return null;
						} else {
							$current = $current->childrens[$p];
						}
					} else {
						if (-$p > $c_size) {
							return null;
						} else {
							$current = $current->childrens[$c_size + $p];
						}
					}

					$node = $current;
				}
				elseif (is_string($p) == true)
				{
					$found = false;

					foreach($current->childrens as $c)
					{
						if ($c->name == $p)
						{
							$found = true;
							$current = $c;
							$node = $c;
							break;
						}
					}

					if ($found == false) {
						return null;
					}
				}
				else
				{
					throw new Exception(sprintf("Invalid type '%s' used in path.", gettype($p)));
				}
			}

			return $node;
		}


		/**
		 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
		 * 
		 * It will first get all the childrens before the sub-childrens.
		 * 
		 * @param inverse bool Will invert the iteration from top-down to bottom-up.
		 * 
		 * @return walk List of all iterators.
		 * @since 1.0
		 */
		public final function walk_base(bool $inverse = false) : array
		{
			$walk = [];
			$walk_childrens = ($inverse == true) ? array_reverse($this->childrens) : $this->childrens;

			// [x]: Store the array (reversed or not) in a temporary array.
			// Because the array is used twince and compute the reversed version twince is dumb.
			// Better reverse it, store it and then use that shit twince.

			foreach($walk_childrens as $child)
			{
				$step = new NodeWalkIterator([$this], $child);
				array_push($walk, $step);
			}

			foreach($walk_childrens as $child)
			{
				foreach($child->walk_tree($inverse) as $iter)
				{
					array_splice($iter->path, 0, 0, [$this]);
					array_push($walk, $iter);
				}
			}

			return $walk;
		}


		/**
		 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
		 * 
		 * It will get childrens and sub-childrens sequencially.
		 * 
		 * @param inverse bool Will invert the iteration from top-down to bottom-up.
		 * 
		 * @return walk List of all iterators.
		 * @since 1.0
		 */
		public final function walk_tree(bool $inverse = false) : array
		{
			$walk = [];

			foreach(($inverse == true) ? array_reverse($this->childrens) : $this->childrens as $child)
			{
				$step = new NodeWalkIterator([$this], $child);
				array_push($walk, $step);

				foreach($child->walk_tree($inverse) as $iter)
				{
					array_splice($iter->path, 0, 0, [$this]);
					array_push($walk, $iter);
				}
			}

			return $walk;
		}


		/**
		 * Convert the current Node into a string.
		 * 
		 * @return string The string with a rappresentation of the current Node.
		 * @since 1.0
		 */
		public final function repr() : string
		{
			return sprintf("<%s:'%s'>", get_class($this), $this->name);
		}


		/**
		 * Convert the current Node structure into a fancy string.
		 * 
		 * @return string The string with a rappresentation of the tree.
		 * @since 1.0
		 */
		public final function repr_tree() : string
		{
			$string = sprintf((sizeof($this->childrens) > 0) ? "%s/" : "%s", $this->repr());

			foreach($this->walk_tree() as $iter)
			{
				$string = $string.sprintf(
					(sizeof($iter->node->childrens) > 0) ? "\n%s%s/" : "\n%s%s",
					str_repeat("\t", sizeof($iter->path)), $iter->node->repr()
				);
			}

			return $string;
		}


		/**
		 * Convert the path of the current Node into a fancy string, you can put a string between each name.
		 * 
		 * @param arrow string A string but between each representation.
		 * 
		 * @return string The string with a rappresentation of the path, current node is excluded.
		 * @since 1.0
		 */
		public final function repr_path(string $arrow = " => ") : string
		{
			$string = "";

			foreach($this->get_path() as $p)
			{
				if (strcmp($string, "") != 0) {
					$string = sprintf("%s%s", $string, $arrow);
				}

				$string = sprintf("%s%s", $string, $p->repr());
			}

			return $string;
		}


	}


?>