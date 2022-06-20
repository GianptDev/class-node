

// ---------------------------------------------------------


package nodeclass.chain;

import java.util.ArrayList;

// ---------------------------------------------------------


public class ChainNode
{
	

	// ---------------------------------------------------------


	/**
	 * The previus node wich the current node has been connected to.
	 * 
	 * @since 1.0
	 */
	private ChainNode parent;


	/**
	 * The next node with has been connected to the current node.
	 * 
	 * @since 1.0
	 */
	private ChainNode child;
	

	/**
	 * Unique string name identifier of the current node.
	 * 
	 * @since 1.0
	 */
	private String name;


	// ---------------------------------------------------------


	public ChainNode()
	{
		this("Node");
	}


	public ChainNode(String name)
	{
		this.parent = null;
		this.child = null;
		this.name = name;
	}


	public String toString()
	{
		return this.repr();
	}


	// ---------------------------------------------------------


	private void _free() {}


	private void _parent_changed() {}


	private void _child_changed() {}


	// ---------------------------------------------------------


	public void rename(String name)
	{
		var new_name = name;
		int count = 0;

		while(true)
		{
			boolean found = false;

			for (var n : this.get_start().get_path(true))
			{
				if ((n != this) && (new_name.equals(n.name) == true))
				{
					found = true;
					break;
				}
			}

			if (found == true) {
				++count;
				new_name = String.format("%s%d", name, count);
			} else {
				name = new_name;
				break;
			}
		}

		this.name = name;
	}


	public void add_child(ChainNode node)
	{
		if (node == null) {
			throw new Error("Tried to add 'null' as a child.");
		}

		if (this.child != null) {
			throw new Error("Another child is already connected to this Node.");
		}

		node.parent = this;
		this.child = node;
		node.rename(node.name);	// Make sure to update name.
		node._parent_changed();
		this._child_changed();
	}
	

	public void remove_parent()
	{
		if (this.parent == null) {
			throw new Error("The current Node is not connected to a parent.");
		}

		var parent = this.parent;

		this.parent = null;
		parent.child = null;
		this._parent_changed();
		parent._child_changed();
	}


	public void remove_child()
	{
		if (this.child == null) {
			throw new Error("The current Node is not connected to a child.");
		}

		var child = this.child;

		this.child = null;
		child.parent = null;
		this._child_changed();
		child._parent_changed();
	}


	// ---------------------------------------------------------


	public ChainNode get_parent()
	{
		return this.parent;
	}


	public ChainNode get_child()
	{
		return this.child;
	}


	public String get_name()
	{
		return this.name;
	}


	public int get_index()
	{
		int index = 0;
		var current = this;

		while(current.parent != null) {
			++index;
			current = current.parent;
		}

		return index;
	}


	public ChainNode get_start()
	{
		var node = this;

		while(node.parent != null) {
			node = node.parent;
		}

		return node;
	}


	public ChainNode get_end()
	{
		var node = this;

		while(node.child != null) {
			node = node.child;
		}

		return node;
	}


	public ChainNode get_chain(int index)
	{
		var node = this;

		if (index >= 0)
		{
			for(int n = 0; n < index; ++n)
			{
				if (node.child != null) {
					node = node.child;
				} else {
					return null;
				}
			}
		}
		else
		{
			index = -index;

			for(int n = 0; n < index; ++n)
			{
				if (node.parent != null) {
					node = node.parent;
				} else {
					return null;
				}
			}
		}

		return node;
	}


	public ChainNode get_chain(String index)
	{
		// TODO: may return itself on non-existent name.
		var node = this;

		for (var n : this.get_start().get_path(true))
		{
			if (n.name.equals(index) == true) {
				node = n;
				break;
			}
		}

		return node;
	}


	public ArrayList<ChainNode> get_path(boolean to_end)
	{
		var path = new ArrayList<ChainNode>();
		ChainNode current = null;

		if (to_end == false)
		{
			current = this.parent;

			while(current != null) {
				path.add(current);
				current = current.parent;
			}
		}
		else
		{
			current = this.child;

			while(current != null) {
				path.add(current);
				current = current.child;
			}
			System.out.print(path + "\n");
		}

		return path;
	}


	public ArrayList<ChainNode> get_path()
	{
		return this.get_path(false);
	}


	public String repr()
	{
		return String.format("<%s:%d:'%s'>", this.getClass().getName(), this.get_index(), this.name);
	}


	public String repr_chain()
	{
		var string = this.repr();

		for (var n : this.get_path(true))
		{
			string = String.format("%s\n\t%s", string, n.repr());
		}

		return string;
	}


	// ---------------------------------------------------------


}


// ---------------------------------------------------------

