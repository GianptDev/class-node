

/**
 * Tree Node,
 * allow chained objects in a tree-like pattern.
 * 
 * Each node can have one parent and multiple childrens
 * ordered in a hierarchy starting from a single node called root.
 */


// -------------------------------------------------


module nodeclass.tree;


import std.format : format;
import std.algorithm.searching : countUntil;
import std.algorithm.mutation : remove, swapAt;
import std.range : repeat, join;
import std.array : array;


// -------------------------------------------------


/** 
 * The index of a Node with no parent.
 * since: 1.0
 */
const int NODE_NO_INDEX = -1;


// -------------------------------------------------


/** 
 * This is an iterator used by the walk methods of the Node.
 * since: 1.0
 */
struct TreeNodeWalkIterator
{
	TreeNode[] path;
	TreeNode node;

	this(TreeNode[] path, TreeNode node)
	{
		this.path = path;
		this.node = node;
	}
}


// -------------------------------------------------


/** 
 * This is the base class of a Node, it contain all the base logic for parenting and building a tree objects structure.
 * 
 * These structures start with an initial Node called `root` and extend into a list of `childrens` and `parents` with more `childrens` parented with it.
 * since: 1.0
 */
class TreeNode
{


	// -------------------------------------------------


	/** 
	 * The Node object wich the current Node is child of.
	 * since: 1.0
	 */
	private TreeNode parent;

	/** 
	 * The list of Node objects wich are childrens of the current Node.
	 * since: 1.0
	 */
	private TreeNode[] childrens;


	/** 
	 * The name of the current Node, if is parented it must be unique among childrens.
	 * Auto-rename appen if another Node with the same name if found.
	 * since: 1.0
	 */
	private string name;


	// -------------------------------------------------


	this(string name = "Node")
	{
		this.name = name;
		this.parent = null;
		this.childrens = [];
	}


	override string toString() const @safe pure
	{
		return this.repr();
	}


	// -------------------------------------------------


	/** 
	 * Executed before the current Node remove all references to itself to any other Node is connected to it.
	 * 
	 * - Virtual
	 * since: 1.0
	 */
	private void _free() {}


	/** 
	 * Executed after the current Node has been manually renamed with `rename` or automatically to make his name unique.
	 * 
	 * - Virtual
	 * since: 1.0
	 */
	private void _renamed() {}


	/** 
	 * Executed after the parent of the current Node has changed or removed.
	 * 
	 * - Virtual
	 * since: 1.0
	 */
	private void _changed_parent() {}


	/** 
	 * Executed after a new node has been parented as a child.
	 * 
	 * Params: 
	 * 	child = The child just added.
	 *
	 * - Virtual
	 * since: 1.0
	 */
	private void _add_child(TreeNode child) {}


	/** 
	* Executed after a node has been unparented from being a child.
	* 
	* Params:
	* 	child = The child just removed.
	* - Virtual
	* since: 1.0
	*/
	private void _removed_child(TreeNode child) {}


	// -------------------------------------------------


	/** 
	* Will help you to remove all references of the current Node from any connection.
	* After that you can destroy the object with no problem.
	* 
	* Here the order of what will happen when executed:
	* 1. Will first execute the same method to all childrens, make sure to remove them before executing this method if you wish to keep them.
	* 2. Will execute the `_free` virtual.
	* 3. Will disconnect from the parent.
	* since: 1.0
	*/
	public final void free()
	{
		foreach (child; array(this.childrens))
		{
			child.free();
			//destroy(child);
		}

		this._free();

		if (this.parent !is null) {
			this.parent.remove_child(this);
		}
	}


	/**
	 * Will change the name of the current node and execute the `_renamed` virtual after.
	 * 
	 * If the name is already used by another child it will start a counter to find an new unique name.
	 * since: 1.0
	 */
	public final void rename(string name)
	{

		if (this.parent !is null)
		{
			auto fix_name = name;
			int count = 0;

			while(true)
			{
				bool found = false;

				foreach (child; this.parent.childrens)
				{
					if ((child != this) && (fix_name == child.name))
					{
						found = true;
						break;
					}
				}

				if (found == true)
				{
					++count;
					fix_name = format("%s%d", name, count);
				}
				else
				{
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
	* since: 1.0
	*/
	public final void remove()
	{

		if (this.parent is null) {
			throw new Exception("The current Node is not parented whit a Node.");
		}

		this.parent.remove_child(this);
	}


	/** 
	 * Will move his index position inside the childrens vector from the parent Node.
	 * 
	 * If no parent exist it will throw an exception.
	 * since: 1.0
	 */
	public final void move(int index)
	{

		if (this.parent is null) {
			throw new Exception("The current Node is not parented whit a Node.");
		}

		this.parent.move_child(this, index);
	}


	/** 
	 * Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.
	 * 
	 * If the input Node is already parented with another Node or is invalid an exception will throw.
	 * since: 1.0
	 */
	public final void add_child(TreeNode node, int index = -1)
	{
		if (node is null) {
			throw new Exception("Tried to add as a child class 'null'.");
		}

		if (node.parent !is null) {
			throw new Exception("Tried to add as a child a Node wich is not parented with the current Node.");
		}

		auto c_size = cast(int) this.childrens.length;

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

		this.childrens = this.childrens[0 .. index] ~ node ~ this.childrens[index .. $];
		node.parent = this;
		node.rename(node.name);
		node._changed_parent();
		this._add_child(node);
	}


	/** 
	 * Will remove the input Node from being the parent of the current Node and will remove it from the childrens list.
	 * 
	 * If the input Node is not parented with the current Node or is invalid an exception will throw. 
	 * since: 1.0
	 */
	public final void remove_child(TreeNode node)
	{

		if (node is null) {
			throw new Exception("Tried to remove as a child class 'null'.");
		}

		if (node.parent != this) {
			throw new Exception("Tried to remove as a child a Node wich is not parented with the current Node.");
		}

		node.parent = null;
		this.childrens = this.childrens.remove(this.childrens.countUntil(node));
		node._changed_parent();
		this._removed_child(node);
	}


	/** 
	 * Will move the index position of the input Node inside the current Node.
	 * 
	 * If the input Node is not parented with the current Node or is invalid an exception will throw. 
	 * since: 1.0
	 */
	public final void move_child(TreeNode node, int index)
	{

		if (node is null) {
			throw new Exception("Tried to move as a child class 'null'.");
		}

		if (node.parent != this) {
			throw new Exception("Tried to move as a child a Node wich is not parented with the current Node.");
		}

		this.childrens.swapAt(this.childrens.countUntil(node), index);
	}


	// -------------------------------------------------


	/** 
	 * Returns: The parent of the current Node.
	 * since: 1.0
	 */
	public final TreeNode get_parent()
	{
		return this.parent;
	}

	/** 
	 * Returns: The childrens of the current Node.
	 * since: 1.0
	 */
	public final TreeNode[] get_childrens()
	{
		return this.childrens;
	}


	/** 
	 * Returns: The name of the current Node.
	 * since: 1.0
	 */
	public final string get_name()
	{
		return this.name;
	}


	/** 
	* Get the index position inside the parent list of the current Node.
	* 
	* Returns: The index position of the curret Node or `NODE_NO_INDEX` if no parent exist. 
	* since: 1.0
	*/
	public final int get_index()
	{
		return (this.parent is null) ? NODE_NO_INDEX : this.parent.childrens.countUntil(this);
	}


	/** 
	 * Will get the top-level Node wich is parented with all the Nodes of the current tree.
	 * since: 1.0
	 */
	public final TreeNode get_root()
	{
		auto node = this;

		while(node.parent !is null) {
			node = node.parent;
		}

		return node;
	}


	/** 
	 * Get the reference of all Nodes between the root Node and the current Node.
	 * since: 1.0
	 */
	public final TreeNode[] get_path()
	{
		TreeNode[] path;
		auto node = this;

		while(node.parent !is null)
		{
			node = node.parent;
			path = path ~ node;
		}

		return path;
	}


	/** 
	 * Will give the total amount of childrens parented with the current Node.
	 * 
	 * Returns: The size of childrens list.
	 * since: 1.0
	 */
	int get_child_count()
	{
		return this.childrens.length;
	}


	/** 
	 * Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).
	 * 
	 * Params:
	 * 	path = The path from the current Node to the target Node, you can find childrens by their index position or unique name.
	 * since: 1.0
	 */
	public TreeNode get_child(T...)(T path)
	{
		auto current = this;
		TreeNode node = null;

		foreach(p; path)
		{
			static if (is(typeof(p) == int))
			{
				auto c_size = cast(int) current.childrens.length;

				if (p >= 0) {
					if (p > (c_size - 1)) {
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
			}
			else static if (is(typeof(p) == string))
			{
				bool found = false;

				foreach (c; current.childrens)
				{
					if (c.name == p)	// Compare the name with string path.
					{
						found = true;
						current = c;
						node = c;
						break;
					}
				}

				if (found == false) {
					return null;
				}
			}
			else
			{
				throw new Exception(format("Invalid type '%s' used in path.", typeof(p).stringof));
			}
		}

		return node;
	}
	

	/** 
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.

	 * It will first get all the childrens before the sub-childrens.
	 * 
	 * Returns: List of all iterators.
	 * since: 1.0
	 */
	public final TreeNodeWalkIterator[] walk_base(bool inverse = false)
	{
		TreeNodeWalkIterator[] walk;
		
		// [x]: array is not reversed but foreach and foreach_reverse are used.
		// D language has foreach_reverse wich will basically loop the array without creating a new one, how cool!
		// Too bad the code is bigger now... i've used this comment to tell this.

		if (inverse == false)
		{
			foreach (child; this.childrens)
			{
				TreeNodeWalkIterator step;

				step.node = child;
				step.path ~= this;
				walk ~= step;
			}

			foreach (child; this.childrens)
			{
				foreach (iter; child.walk_base(inverse = inverse))
				{
					iter.path = this ~ iter.path;
					walk ~= iter;
				}
			}
		}
		else
		{
			foreach_reverse (child; this.childrens)
			{
				TreeNodeWalkIterator step;

				step.node = child;
				step.path ~= this;
				walk ~= step;
			}

			foreach_reverse (child; this.childrens)
			{
				foreach (iter; child.walk_base(inverse = inverse))
				{
					iter.path = this ~ iter.path;
					walk ~= iter;
				}
			}
		}

		return walk;
	}


	/** 
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 *
	 * It will get childrens and sub-childrens sequencially.
	 *
	 * Returns: List of all iterators.
	 * since: 1.0
	 */
	public final TreeNodeWalkIterator[] walk_tree(bool inverse = false)
	{
		TreeNodeWalkIterator[] walk;

		// [x]: array is not reversed but foreach and foreach_reverse are used.
		// D language has foreach_reverse wich will basically loop the array without creating a new one, how cool!
		// Too bad the code is bigger now... i've used this comment to tell this.

		if (inverse == false)
		{
			foreach (child; this.childrens)
			{
				TreeNodeWalkIterator step;

				step.node = child;
				step.path ~= this;
				walk ~= step;

				foreach (iter; child.walk_tree(inverse = inverse))
				{
					iter.path = this ~ iter.path;
					walk ~= iter;
				}
			}
		}
		else
		{
			foreach_reverse (child; this.childrens)
			{
				TreeNodeWalkIterator step;

				step.node = child;
				step.path ~= this;
				walk ~= step;

				foreach (iter; child.walk_tree(inverse = inverse))
				{
					iter.path = this ~ iter.path;
					walk ~= iter;
				}
			}
		}

		return walk;
	}


	/**
	 * Convert the current Node into a string.
	 * since: 1.0
	 */
	public final string repr() @safe pure const
	{
		return format("<%s:'%s'>", this.classinfo.name, this.name);
	}


	/**
	* Convert the current Node structure into a fancy string.
	* since: 1.0
	*/
	public final string repr_tree()
	{
		string text = format((this.childrens.length > 0) ? "%s/" : "%s", this.repr());
	
		foreach (root; this.walk_tree())
		{
			text = format(
				(root.node.childrens.length > 0 ) ? "%s\n%s%s/" : "%s\n%s%s",
				text, "\t".repeat(root.path.length).join(), root.node.repr()
			);
		}

		return text;
	}


}


// -------------------------------------------------

