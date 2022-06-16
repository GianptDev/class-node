

// -------------------------------------------------


void main()
{
	import std.stdio : writeln;
	import nodeclass.tree : TreeNode;

	writeln("Hello world");

	auto n = new TreeNode("root");

	n.add_child(new TreeNode());
	n.add_child(new TreeNode());
	n.add_child(new TreeNode());
	n.add_child(new TreeNode());

	n.get_child(1).add_child(new TreeNode());
	n.get_child(1).add_child(new TreeNode());
	n.get_child(1).add_child(new TreeNode());

	n.get_child(0).add_child(new TreeNode());
	//n.get_child(0.0);

	//writeln(n.repr());

	writeln(n.get_child("Node2").repr());
	writeln(n.get_child(1,0).get_path());

	n.add_child(new TreeNode("test"), 3000);

	writeln(n.repr_tree());

	writeln(n.get_child(-100));

	//n.remove_child(n.get_child(0));

	n.free();
}


// -------------------------------------------------

