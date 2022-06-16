

/**
 * Tree Node,
 * allow chained objects in a tree-like pattern.
 * 
 * Each node can have one parent and multiple childrens
 * ordered in a hierarchy starting from a single node called root.
 */


// ---------------------------------------------------------


/**
 * The index of a Node with no parent.
 * 
 * @since 1.0
 */
 export const NODE_NO_INDEX = -1;


// ---------------------------------------------------------


/**
 * This is an iterator used by the walk methods of the Node.
 * 
 * @since 1.0
 */
 export class NodeWalkIterator
{
	constructor(/** @type {array<Node>} */ path,/** @type {TreeNode} */ node)
	{
		/** @type {array<Node>} */
		this.path = path;
		/** @type {TreeNode} */
		this.node = node;
	}
}


// ---------------------------------------------------------


/**
 * The Node class object, it allow to connect and be connected with other nodes.
 * 
 * When a connection happen the child, who is being connected, get the reference of the parent, who started the connection, and the parent get a reference of the child.
 * 
 * Inside a connection group is possible for any object to get any other object by travelling with a path structure.
 * 
 * @since 1.0
 */
 export class TreeNode
{


	// ---------------------------------------------------------


	/**
	 * 
	 * @param {string} name - "Node"
	 */
	constructor(name = "Node")
	{
		/**
		 * The Node object wich the current Node is child of.
		 * 
		 * @type {TreeNode}
		 * @since 1.0
		 * */
		this.parent = null;


		/**
		 * The list of Node objects wich are childrens of the current Node.
		 * 
		 * @type {array<Node>}
		 * @since 1.0
		 * */
		this.childrens = [];


		/**
		 * The unique name of the current Node, it will automatically rename itself if the current Node become the child of a parent Node with already another child with the same name.
		 * 
		 * @type {string}
		 * @since 1.0
		 * */
		this.name = name;
	}


	// ---------------------------------------------------------


	/**
	 * Executed before the current Node remove all references to itself to any other Node is connected to it.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_free() {}


	/**
	 * Executed after the current Node has been manually renamed with `rename` or automatically to make his name unique.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_renamed() {}


	/**
	 * Executed after the parent of the current Node has changed or removed.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_changed_parent() {}


	/**
	 * Executed after a new node has been parented as a child.
	 * 
	 * @param {TreeNode} child The child just added.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_add_child(child) {}

	
	/**
	 * Executed after a node has been unparented from being a child.
	 * 
	 * @param {TreeNode} child The child just removed.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_removed_child(child) {}


	// ---------------------------------------------------------


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
	free()
	{
		for (let child of [...this.childrens])
		{
			child.free();
		}

		this._free();

		if (this.parent != null) {
			this.parent.remove_child(this);
		}
	}


	/**
	 * Will change the name of the current node and execute the `_renamed` virtual after.
	 * 
	 * If the name is already used by another child it will start a counter to find an new unique name.
	 * 
	 * @param {string} name The new desired name.
	 * 
	 * @since 1.0
	 */
	rename(name)
	{

		if (this.parent != null)
		{
			let fix_name = name;
			let count = 0;

			while(true)
			{
				let found = false;

				for (let child of this.parent.childrens)
				{
					if ((child != this) && (fix_name == child.name))
					{
						found = true;
						break;
					}
				}

				if (found == true) {
					++count;
					fix_name = `${name}${count}`;
				} else {
					name = fix_name;
					break;
				}
			}
		}

		this.name = name;
		this._renamed();
	}


	/**
	 * Will unparent itself from the parent Node.
	 * 
	 * If no parent exist it will throw an exception.
	 * 
	 * @since 1.0
	 */
	remove()
	{

		if (this.parent == null) {
			throw "The current Node is not parented whit a Node.";
		}

		this.parent.remove_child(this);
	}


	/**
	 * Will move his index position inside the childrens vector from the parent Node.
	 * 
	 * If no parent exist it will throw an exception.
	 * 
	 * @param {int} index the desired index position.
	 * 
	 * @since 1.0
	 */
	move(index)
	{

		if (this.parent == null) {
			throw "The current Node is not parented whit a Node.";
		}

		this.parent.move_child(this, index);
	}


	/**
	 * Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.
	 * 
	 * If the input Node is already parented with another Node or is invalid an exception will throw.
	 * 
	 * @param {TreeNode} node The new node to parent.
	 * @param {int} index	Optional index of his position.
	 * 
	 * @since 1.0
	 */
	add_child(node, index = -1)
	{
		
		if ((node instanceof TreeNode) == false) {
			throw `Tried to add type '${typeof node}' to a Node class.`;
		}

		if (node.parent != null) {
			throw "Tried to add as a child a Node wich is already parented to another Node.";
		}

		let c_size = this.childrens.length;

		if (index >= 0) {
			if (index > c_size) {
				index = c_size;
			}
		} else {
			if (-index > c_size) {
				index = 0;
			} else {
				index = c_size + index + 1;
			}
		}

		this.childrens.splice(index, 0, node);
		node.parent = this;
		node.rename(node.name);
		node._changed_parent();
		this._add_child(node);
	}


	/**
	 * Will remove the input Node from being the parent of the current Node and will remove it from the childrens list.
	 * 
	 * If the input Node is not parented with the current Node or is invalid an exception will throw.
	 * 
	 * @param {TreeNode} child The child to remove.
	 * 
	 * @since 1.0
	 */
	remove_child(node)
	{
		if ((node instanceof TreeNode) == false) {
			throw `Tried to remove type '${typeof node}' to a Node class.`;
		}

		if (node.parent != this) {
			throw "Tried to remove a node wich isn't parented with the current Node.";
		}

		node.parent = null;
		this.childrens = this.childrens.filter(element => element != node);
		node._changed_parent();
		this._removed_child(node);
	}


	/**
	 * Will move the index position of the input Node inside the current Node.
	 * 
	 * If the input Node is not parented with the current Node or is invalid an exception will throw.
	 * 
	 * @param {TreeNode} node The node to move.
	 * @param {int} index The new index position.
	 * 
	 * @since 1.0
	 */
	move_child(node, index)
	{
		if (node.parent != this) {
			throw "Tried to move a node wich isn't parented with the current Node.";
		}

		this.childrens = this.childrens.filter(element => element != node);
		this.childrens.splice(index, 0, node);
	}

	
	// ---------------------------------------------------------


	/**
	 * Get the index position inside the parent list of the current Node.
	 * 
	 * @returns {int}
	 * @since 1.0
	 */
	get_index()
	{
		return (this.parent == null) ? NODE_NO_INDEX : this.parent.childrens.findIndex(element => element == this);
	}


	/**
	 * Will get the top-level Node wich is parented with all the Nodes of the current tree.
	 * 
	 * @returns {TreeNode}
	 * @since 1.0
	 */
	get_root()
	{
		let node = this;

		while(node.parent != null) {
			node = node.parent;
		}

		return node;
	}


	/**
	 * Get the reference of all Nodes between the root Node and the current Node.
	 * 
	 * @returns {array<Node>}
	 * @since 1.0
	 */
	get_path()
	{
		let path = [];
		let node = this;

		while(node.parent != null)
		{
			node = node.parent;
			path.splice(0, 0, node);
		}

		return path;
	}


	/**
	 * Will give the total amount of childrens parented with the current Node.
	 * 
	 * @returns {int} The size of childrens list.
	 * @since 1.0
	 */
	get_child_count()
	{
		return this.childrens.length;
	}


	/**
	 * Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).
	 * 
	 * @param  {...[int, string]} path The path from the current Node to the target Node, you can find childrens by their index position or unique name.
	 * 
	 * @returns {Node|null}
	 * @since 1.0
	 */
	get_child(...path)
	{
		let current = this;
		let node = null;

		for (let p of path)
		{
			if (typeof p == "number") {
				let c_size = current.childrens.length;

				if (p >= 0) {
					if (p > (c_size -1)) {
						return null;
					} else {
						current = current.childrens[p];
					}
				} else {
					if (-p > c_size) {
						return null;
					} else {
						current = current.childrens[c_size + p];
					}
				}

				node = current;
			
			} else if (typeof p == "string") {
				let found = false;

				for (let child of current.childrens)
				{
					if (child.name == p)
					{
						found = true;
						current = child;
						node = child;
						break;
					}
				}

				if (found != true) {
					return null;
				}
			} else {
				throw `Invalid type '${typeof p}' used in path.`;
			}
		}

		return node;
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will first get all the childrens before the sub-childrens.
	 * 
	 * @param {bool} inverse Will invert the iteration from top-down to bottom-up.
	 * 
	 * @returns {array<NodeWalkIterator>}
	 * @since 1.0
	 */
	walk_base(inverse = false)
	{
		let walk = [];
		let walk_childrens = (inverse == false) ? this.childrens : this.childrens.reverse();

		// [x]: Store the array (reversed or not) in a temporary array.
		// Because the array is used twince and compute the reversed version twince is dumb.
		// Better reverse it, store it and then use that shit twince.

		for (let child of walk_childrens)
		{
			let step = new NodeWalkIterator([this], child);
			walk.push(step);
		}

		for (let child of walk_childrens)
		{
			for (let iter of child.walk_base(inverse))
			{
				walk.path.splice(index, 0, this);
				walk.push(iter);
			}
		}

		return walk;
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will get childrens and sub-childrens sequencially.
	 * 
	 * @param inverse Will invert the iteration from top-down to bottom-up.
	 * 
	 * @returns {array<NodeWalkIterator>}
	 * @since 1.0
	 */
	walk_tree(inverse = false)
	{
		let walk = [];

		for (let child of ((inverse == false) ? this.childrens : this.childrens.reverse()))
		{
			let step = new NodeWalkIterator([this], child);
			walk.push(step);

			for (let iter of child.walk_tree(inverse))
			{
				iter.path.splice(0, 0, this);
				walk.push(iter);
			}
		}

		return walk;
	}


	/**
	 * Convert the current Node into a string.
	 * 
	 * @returns {string}
	 * @since 1.0
	 */
	repr()
	{
		return `<${this.constructor.name}:'${this.name}'>`;
	}


	/**
	 * Convert the current Node structure into a fancy string.
	 * 
	 * @returns {string}
	 * @since 1.0
	 */
	repr_tree()
	{
		let string = `${this.repr()}${((this.childrens.length > 0) ? "/" : "")}`;

		for (let iter of this.walk_tree())
		{
			string += `\n${"\t".repeat(iter.path.length)}${iter.node.repr()}${(iter.node.childrens.length > 0) ? "/" : ""}`;
		}

		return string;
	}

	
};


// ---------------------------------------------------------

