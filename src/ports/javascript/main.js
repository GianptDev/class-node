

// ---------------------------------------------------------


import {TreeNode} from "./nodeclass/tree.js";
import {ChainNode} from "./nodeclass/chain.js";


// ---------------------------------------------------------


function main()
{


	let n = new ChainNode();

	return;

	n = new TreeNode("root");
	let c = new TreeNode();

	n.add_child(c);
	n.add_child(new TreeNode());
	n.add_child(new TreeNode());
	
	n.get_child(0).add_child(new TreeNode("amogus"));

	for (let a = 0; a < 4; ++a)
	{
		n.add_child(new TreeNode());
	}

	for (let a = 0; a < 4; ++a)
	{
		n.get_child(3).add_child(new TreeNode());
	}

	n.add_child(new TreeNode("AAAA"), -3000);

	//n.get_child(0).move(2);

	console.log(n.repr_tree());

	n.free();
}


// ---------------------------------------------------------


main();


// ---------------------------------------------------------

