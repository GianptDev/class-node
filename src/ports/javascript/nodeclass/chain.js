

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


	free()
	{
		for (let child of [...this.childrens])
		{
			child.free();
		}

		this._free();

		if (this.parent != null) {
			this.parent.remove_child();
		}
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
		let node = self;

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
		let node = self;

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
				path.splice(index, 0, current);
				current = current.child;
			}
		}

		return path;
	}


}


// ---------------------------------------------------------

