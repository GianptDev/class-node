

// ---------------------------------------------------------


export class ChainNode
{


	// ---------------------------------------------------------


	/**
	 * 
	 * @param {string} name - "Node"
	 */
	constructor(name = "Node")
	{
		/**
		 * The previus node wich the current node has been connected to.
		 * 
		 * @type {ChainNode}
		 * @since 1.0
		 */
		this.parent = null;

		/**
		 * The next node with has been connected to the current node.
		 * 
		 * @type {ChainNode}
		 * @since 1.0
		 */
		this.child = null;
		

		/**
		 * Unique string name identifier of the current node.
		 * 
		 * @type {string}
		 * @since 1.0
		 */
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
	 * Executed after the parent of the current Node has changed or removed.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	_parent_changed() {}


	/**
	 * Executed after the child of the current Node has changed or removed.
	 * 
	 * @since: 1.0
	 * @virtual
	 */
	_child_changed() {}


	// ---------------------------------------------------------


	/**
	 * @since 1.0
	 */
	free()
	{
		for (let child of this.get_path(true))
		{
			child.free();
		}

		this._free();

		if (this.parent != null) {
			this.parent.remove_child();
		}
	}


	/**
	 * 
	 * @param {string} name 
	 * @since 1.0
	 */
	rename(name)
	{
		let new_name = name;
		let count = 0;

		while(true)
		{
			let found = false;

			for (let n of this.get_start().get_path(true))
			{
				if ((n != this) && (n.name == new_name)) {
					found = true;
					break;
				}
			}

			if (found == true) {
				++count;
				new_name = `${name}${count}`;
			} else {
				name = new_name;
				break;
			}
		}

		this.name = name;
	}


	/**
	 * Connect node as a child of the current Node.
	 * 
	 * If a child already exist, an exception is raised.
	 * 
	 * @param {ChainNode} node 
	 */
	add_child(node)
	{
		if ((node instanceof ChainNode) == false) {
			throw `Tried to add type '${typeof node}' as a child.`;
		}

		if (this.child != null) {
			throw "Another child is already connected to this Node.";
		}

		node.parent = this;
		this.child = node;
		node.rename(node.name);
		node._parent_changed();
		this._child_changed();
	}


	/**
	 * @since 1.0
	 */
	remove_parent()
	{
		if (this.parent == null) {
			throw "The current Node is not connected to a parent.";
		}

		let parent = this.parent;

		this.parent = null;
		parent.child = null;
		this._parent_changed();
		parent._child_changed();
	}


	/**
	 * Disconnect the current Node from his child.
	 * 
	 * @since 1.0
	 */
	remove_child()
	{
		if (this.child == null) {
			throw "The current Node is not connected to a child.";
		}

		let child = this.child;

		this.child = null;
		child.parent = null;
		this._child_changed();
		child._parent_changed();
	}


	// ---------------------------------------------------------


	/**
	 * Get the index position inside the chain from the start to the current position.
	 * 
	 * @returns {int}
	 * @since 1.0
	 */
	get_index()
	{
		let index = 0;
		let current = this;

		while(current.parent != null) {
			++index;
			current = current.parent;
		}

		return index;
	}


	/**
	 * The the first Node of the whole chain structure.
	 * 
	 * @returns {ChainNode}
	 * @since 1.0
	 */
	get_start()
	{
		let node = this;

		while(node.parent != null) {
			node = node.parent;
		}

		return node;
	}


	/**
	 * The the last Node of the whole chain structure.
	 * 
	 * @returns {ChainNode}
	 * @since 1.0
	 */
	get_end()
	{
		let node = this;

		while(node.child != null) {
			node = node.child;
		}

		return node;
	}


	/**
	 * Get a node by skipping index amount going backwards or forwards from the current Node.
	 * 
	 * @param {int|string} index 
	 * @returns {ChainNode|null}
	 */
	get_chain(index)
	{
		let node = this;

		if (typeof index == "number")
		{
			if (index >= 0)
			{
				for (let n = 0; n < index; ++n)
				{
					if (node.child != null) {
						node = node.child;
					} else {
						return null;
					}
				}
			} else {
				index = -index;

				for (let n = 0; n < index; ++n)
				{
					if (node.parent != null) {
						node = node.parent;
					} else {
						return null;
					}
				}
			}
		}
		else if (typeof index == "string")
		{
			for (let n of this.get_start().get_path(true))
			{
				if (n.name == index) {
					node = n;
					break;
				}
			}
		}
		else {
			throw `Invalid type '${typeof p}' used in index.`;
		}

		return node;
	}


	/**
	 * Will get all the nodes between the current Node and the fist Node, or from the current Node to the last Node.
	 * 
	 * @param {bool} to_end - false
	 * @returns {array<ChainNode>}
	 */
	get_path(to_end = false)
	{
		let path = [];
		let current = null;

		if (to_end == false)
		{
			current = this.parent;

			while(current != null) {
				path.splice(index, 0, current);
				current = current.parent;
			}
		} else {
			current = this.child;

			while(current != null) {
				path.splice(path.length, 0, current);
				current = current.child;
			}
		}

		return path;
	}


	/**
	 * Convert the current node into a string.
	 * 
	 * @returns {string}
	 */
	repr()
	{
		return `<${this.constructor.name}:${this.get_index()}:'${this.name}'>`;
	}


	/**
	 * Convert the current chain structure into a fancy string.
	 * 
	 * @returns {string}
	 */
	repr_chain()
	{
		let string = this.repr();

		for (let n of this.get_path(true))
		{
			string += `\n\t${n.repr()}`;
		}

		return string;
	}


}


// ---------------------------------------------------------

