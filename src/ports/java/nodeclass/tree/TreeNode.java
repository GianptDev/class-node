

/**
 * Tree Node,
 * allow chained objects in a tree-like pattern.
 * 
 * Each node can have one parent and multiple childrens
 * ordered in a hierarchy starting from a single node called root.
 */


// ---------------------------------------------------------


package nodeclass.tree;


// ---------------------------------------------------------


import java.util.ArrayList;
import java.util.Collections;


// ---------------------------------------------------------


/**
 * This is the base class of a Node, it contain all the base logic for parenting and building a tree objects structure.
 * <p>
 * These structures start with an initial Node called {@code root} and extend into a list of {@code childrens} and {@code parents} with more {@code childrens} parented with it.
 * 
 * @since 1.0
 */
public class TreeNode
{


	// ---------------------------------------------------------


	/**
	 * The index of a Node with no parent.
	 * 
	 * @since 1.0
	 */
	public static final int NODE_NO_INDEX = -1;


	/**
	 * This is an iterator used by the walk methods of the Node.
	 * 
	 * @since 1.0
	 */
	public record TreeNodeWalkIterator(ArrayList<TreeNode> path, TreeNode node) {}


	// ---------------------------------------------------------


	/**
	 * The Node object wich the current Node is child of.
	 * 
	 * @since 1.0
	 */
	private TreeNode parent;


	/**
	 * The list of Node objects wich are childrens of the current Node.
	 * 
	 * @since 1.0
	 */
	private ArrayList<TreeNode> childrens;


	/**
	 * The unique name of the current Node, it will automatically rename itself if the current Node become the child of a parent Node with already another child with the same name.
	 * 
	 * @since 1.0
	 */
	private String name;


	// ---------------------------------------------------------


	public TreeNode()
	{
		this.parent = null;
		this.childrens = new ArrayList<TreeNode>();
		this.name = "Node";
	}


	public TreeNode(String name)
	{
		this.parent = null;
		this.childrens = new ArrayList<TreeNode>();
		this.name = name;
	}


	public String toString()
	{
		return this.repr();
	}


	// ---------------------------------------------------------


	/**
	 * Executed before the current Node remove all references to itself to any other Node is connected to it.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	private void _free() {}


	/**
	 * Executed after the current Node has been manually renamed with {@code rename} or automatically to make his name unique.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	private void _renamed() {}


	/**
	 * Executed after the parent of the current Node has changed or removed.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	private void _changed_parent() {}


	/**
	 * Executed after a new node has been parented as a child.
	 * 
	 * @param child The child just added.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	private void _add_child(TreeNode child) {}


	/**
	 * Executed after a node has been unparented from being a child.
	 * 
	 * @param child The child just removed.
	 * 
	 * @since 1.0
	 * @virtual
	 */
	private void _removed_child(TreeNode child) {}


	// ---------------------------------------------------------


	/**
	 * Will help you to remove all references of the current Node from any connection.
	 * <p>
	 * Here the order of what will happen when executed:<p>
	 * 1. Will first execute the same method to all childrens, make sure to remove them before executing this method if you wish to keep them.<p>
	 * 2. Will execute the {@code _free} virtual.<p>
	 * 3. Will disconnect from the parent.<p>
	 * <p>
	 * After that you can destroy the object with no problem.
	 * 
	 * @since 1.0
	 */
	public final void free()
	{
		for (var child : new ArrayList<TreeNode>(this.childrens))
		{
			child.free();
		}

		this._free();

		if (this.parent != null) {
			this.parent.remove_child(this);
		}
	}


	/**
	 * Will change the name of the current node and execute the {@code _renamed} virtual after.
	 * <p>
	 * If the name is already used by another child it will start a counter to find an new unique name.
	 * 
	 * @param name The new desired name.
	 * 
	 * @since 1.0
	 */
	public final void rename(String name)
	{

		if (this.parent != null)
		{
			String fix_name = name;
			int count = 0;

			while (true)
			{
				boolean found = false;

				for (var child : this.parent.childrens)
				{
					if ((child != this) && (fix_name.equals(child.name) == true)) {
						found = true;
						break;
					}
				}

				if (found == true) {
					++count;
					fix_name = String.format("%s%d", name, count);
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
	 * <p>
	 * If no parent exist it will throw an exception.
	 * 
	 * @since 1.0
	 */
	public final void remove()
	{
		
		if (this.parent == null) {
			throw new Error("The current Node has no parent and can't be removed.");
		}
		
		this.parent.remove_child(this);
	}


	/**
	 * Will move his index position inside the childrens vector from the parent Node.
	 * <p>
	 * If no parent exist it will throw an exception.
	 * 
	 * @param index the desired index position.
	 * 
	 * @since 1.0
	 */
	public final void move(int index)
	{

		if (this.parent == null) {
			throw new Error("The current Node has no parent and can't be removed.");
		}

		this.parent.move_child(this, index);
	}


	/**
	 * Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.
	 * <p>
	 * If the input Node is already parented with another Node or is invalid an exception will throw.
	 * 
	 * @param node The new node to parent.
	 * 
	 * @since 1.0
	 */
	public final void add_child(TreeNode node)
	{
		this.add_child(node, -1);
	}


	/**
	 * Will add as a child the input Node and set his parent as the current Node and add it inside the childres list, virutal methods are executed.
	 * <p>
	 * If the input Node is already parented with another Node or is invalid an exception will throw.
	 * 
	 * @param node The new node to parent.
	 * @param index	Optional index of his position.
	 * 
	 * @since 1.0
	 */
	public final void add_child(TreeNode node, int index)
	{

		if (node == null) {
			throw new Error("Tried to add as a child class 'null'.");
		}

		if (node.parent != null) {

			if (node.parent == this) {
				throw new Error("Tried to add as a child a Node wich is already parented with the current Node.");
			}

			throw new Error("Tried to add as a child a Node wich is already parented with another Node.");
		}

		var c_size = this.childrens.size();

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

		this.childrens.add(index, node);
		node.parent = this;
		node.rename(node.name);	// Make sure to update the name.
		node._changed_parent();
		this._add_child(node);
	}


	/**
	 * Will remove the input Node from being the parent of the current Node and will remove it from the childrens list.
	 * <p>
	 * If the input Node is not parented with the current Node or is invalid an exception will throw.
	 * 
	 * @param child The child to remove.
	 * 
	 * @since 1.0
	 */
	public final void remove_child(TreeNode child)
	{
		
		if (child == null) {
			throw new Error("Tried to remove as a child class 'null'.");
		}

		if (child.parent != this) {
			throw new Error("Tried to remove as a child a Node wich is not parented with the current Node.");
		}

		child.parent = null;
		this.childrens.remove(child);
		child._changed_parent();
		this._removed_child(child);
	}


	/**
	 * Will move the index position of the input Node inside the current Node.
	 * <p>
	 * If the input Node is not parented with the current Node or is invalid an exception will throw.
	 * 
	 * @param node The node to move.
	 * @param index The new index position.
	 * 
	 * @since 1.0
	 */
	public final void move_child(TreeNode node, int index)
	{

		if (node == null) {
			throw new Error("Tried to move as a child class 'null'.");
		}

		if (node.parent != this) {
			throw new Error("Tried to move as a child a Node wich is not parented with the current Node.");
		}

		var child_index = this.childrens.indexOf(node);

		this.childrens.remove(child_index);
		this.childrens.add(index, node);
	}


	// ---------------------------------------------------------


	/**
	 * @return The parent of the current Node.
	 * @since 1.0
	 */
	public final TreeNode get_parent()
	{
		return this.parent;
	}


	/**
	 * @return The childrens of the current Node.
	 * @since 1.0
	 */
	public final ArrayList<TreeNode> get_childrens()
	{
		return this.childrens;
	}


	/**
	 * @return The name of the current Node.
	 * @since 1.0
	 */
	public final String get_name()
	{
		return this.name;
	}


	/**
	 * Get the index position inside the parent list of the current Node.
	 * 
	 * @return The index position of the curret Node or {@code NODE_NO_INDEX} if no parent exist.
	 * @since 1.0
	 */
	public final int get_index()
	{
		return (this.parent == null) ? NODE_NO_INDEX : this.parent.childrens.indexOf(this);
	}


	/**
	 * Will get the top-level Node wich is parented with all the Nodes of the current tree.
	 * 
	 * @since 1.0
	 */
	public final TreeNode get_root()
	{
		var node = this;

		while(node.parent != null) {
			node = node.parent;
		}

		return node;
	}


	/**
	 * Get the reference of all Nodes between the root Node and the current Node.
	 * 
	 * @since 1.0
	 */
	public final ArrayList<TreeNode> get_path()
	{
		var path = new ArrayList<TreeNode>();
		var node = this;

		while(node.parent != null) {
			node = node.parent;
			path.add(0, node);
		}

		return path;
	}


	/**
	 * Will give the total amount of childrens parented with the current Node.
	 * 
	 * @return The size of childrens list.
	 * @since 1.0
	 */
	public final int get_child_count()
	{
		return this.childrens.size();
	}


	/**
	 * Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).
	 * 
	 * @param path The path of index positions from the current Node to the target Node.
	 * 
	 * @return The found Node or {@code null} if not found.
	 * @since 1.0
	 */
	public final TreeNode get_child(int ... path)
	{
		var current = this;
		TreeNode node = null;

		for (var p : path)
		{
			var c_size = current.childrens.size();

			if (p >= 0) {
				if (p > (c_size - 1)) {
					return null;
				} else {
					current = current.childrens.get(p);
				}
			} else {
				if (-p > c_size) {
					return null;
				} else {
					current = current.childrens.get(c_size + p);
				}
			}

			node = current;
		}

		return node;
	}



	/**
	 * Will find a Node from the current Node (if 1 argoument is used) or travel trought sub-childrens (if more argouments are used).
	 * 
	 * @param path The path of unique names from the current Node to the target Node.
	 * 
	 * @return The found Node or {@code null} if not found.
	 * @since 1.0
	 */
	public final TreeNode get_child(String ... path)
	{
		var current = this;
		TreeNode node = null;

		for (var p : path)
		{
			boolean found = false;

			for (var child : current.childrens)
			{
				if (child.name.equals(p) == true)
				{
					found = true;
					current = child;
					node = child;
					break;
				}
			}

			if (found == false) {
				return null;
			}
		}

		return node;
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will first get all the childrens before the sub-childrens.
	 * 
	 * @return List of all iterators.
	 * @since 1.0
	 */
	public final ArrayList<TreeNodeWalkIterator> walk_base()
	{
		return this.walk_base(false);
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will first get all the childrens before the sub-childrens.
	 * 
	 * @param inverse Will invert the iteration from top-down to bottom-up.
	 * 
	 * @return List of all iterators.
	 * @since 1.0
	 */
	public final ArrayList<TreeNodeWalkIterator> walk_base(boolean inverse)
	{
		var walk = new ArrayList<TreeNodeWalkIterator>();
		var walk_childrens = this.childrens;

		if (inverse == true)
		{
			walk_childrens = new ArrayList<TreeNode>(this.childrens);
			Collections.reverse(walk_childrens);
		}

		for (var child : walk_childrens)
		{
			var step = new TreeNodeWalkIterator(new ArrayList<TreeNode>(), child);

			step.path.add(this);
			walk.add(step);
		}

		for (var child : walk_childrens)
		{
			for (var iter : child.walk_base(inverse))
			{
				iter.path.add(0, this);
				walk.add(iter);
			}
		}

		return walk;
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will get childrens and sub-childrens sequencially.
	 * 
	 * @return List of all iterators.
	 * @since 1.0
	 */
	public final ArrayList<TreeNodeWalkIterator> walk_tree()
	{
		return this.walk_tree(false);
	}


	/**
	 * Get all the childrens and sub-childrens from the current Node and give a list of iterators with the path and the target Node of the iteration.
	 * <p>
	 * It will get childrens and sub-childrens sequencially.
	 * 
	 * @param inverse Will invert the iteration from top-down to bottom-up.
	 * 
	 * @return List of all iterators.
	 * @since 1.0
	 */
	public final ArrayList<TreeNodeWalkIterator> walk_tree(boolean inverse)
	{
		var walk = new ArrayList<TreeNodeWalkIterator>();
		var walk_childrens = this.childrens;

		if (inverse == true)
		{
			walk_childrens = new ArrayList<TreeNode>(this.childrens);
			Collections.reverse(walk_childrens);
		}

		for (var child : walk_childrens)
		{
			var step = new TreeNodeWalkIterator(new ArrayList<TreeNode>(), child);

			step.path.add(this);
			walk.add(step);

			for (var iter : child.walk_tree(inverse))
			{
				iter.path.add(0, this);
				walk.add(iter);
			}
		}

		return walk;
	}


	/**
	 * Convert the current Node into a string.
	 * 
	 * @return The string with a rappresentation of the current Node.
	 * @since 1.0
	 */
	public final String repr()
	{
		return String.format("<%s:'%s'>", this.getClass().getName(), this.name);
	}


	/**
	 * Convert the current Node structure into a fancy string.
	 * 
	 * @return The string with a rappresentation of the tree.
	 * @since 1.0
	 */
	public final String repr_tree()
	{
		String string = String.format(
			(this.childrens.size() <= 0) ? "%s" : "%s/", this.repr());
	
		for (var root : this.walk_tree(false))
		{
			string = String.format(
				(root.node.childrens.size() <= 0) ? "%s\n%s%s" : "%s\n%s%s/",
				string, "\t".repeat(root.path.size()), root.node.repr()
			);
		}
	
		return string;
	}


	/**
	 * Convert the path of the current Node into a fancy string, you can put a string between each name.
	 * 
	 * @return The string with a rappresentation of the path, current node is excluded.
	 * @since 1.0
	 */
	public final String repr_path()
	{
		return this.repr_path(" => ");
	}


	/**
	 * Convert the path of the current Node into a fancy string, you can put a string between each name.
	 * 
	 * @param arrow A custom string added in between of each node rappresented.
	 * 
	 * @return The string with a rappresentation of the path, current node is excluded.
	 * @since 1.0
	 */
	public final String repr_path(String arrow)
	{
		String string = "";

		for (var p : this.get_path())
		{
			if (string.equals("") == false) {
				string = String.format("%s%s", string, arrow);
			}
			
			string = String.format("%s%s", string, p.repr());
		}

		return string;
	}


}


// ---------------------------------------------------------

