

// ---------------------------------------------------------


import nodeclass.tree.TreeNode;


// ---------------------------------------------------------


public class Main
{
	public static void main(String[] args)
	{
		System.out.print("Node features test:\n");


		var n = new TreeNode("root");
		System.out.print(String.format("New '%s' instanced at: %s\n\n", n.get_name(), n));

		
		for (int a = 0; a < 4; ++a) {
			var c = new TreeNode();
			n.add_child(c);
		}
		System.out.print(String.format("Add 4 childs:\n%s\n\n", n.repr_tree()));
		

		for (int a = 0; a < 4; ++a) {
			var c = new TreeNode("Amogos");
			n.get_child(2).add_child(c);
		}
		System.out.print(String.format("Add more childs:\n%s\n\n", n.repr_tree()));

		//System.out.print(n.get_child(2, 0).get_path());

		System.out.print(n.get_child(2, 0).repr_path());

		n.free();

		
	}
}


// ---------------------------------------------------------

