

// ---------------------------------------------------------


import {TreeNode as Node} from "./nodeclass/tree.js";


// ---------------------------------------------------------


function main()
{
	let n = new Node("root");
	let c = new Node();

	n.add_child(c);
	n.add_child(new Node());
	n.add_child(new Node());
	
	n.get_child(0).add_child(new Node("amogus"));

	for (let a = 0; a < 4; ++a)
	{
		n.add_child(new Node());
	}

	for (let a = 0; a < 4; ++a)
	{
		n.get_child(3).add_child(new Node());
	}

	n.add_child(new Node("AAAA"), -3000);

	//n.get_child(0).move(2);

	console.log(n.repr_tree());

	n.free();
}


// ---------------------------------------------------------


main();


// ---------------------------------------------------------

