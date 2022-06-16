<?php

	require "./nodeclass/nodeclass.php";

	$r = new nodeclass\TreeNode("root");

	$c = new nodeclass\TreeNode();
	$r->add_child($c);
	$r->add_child(new nodeclass\TreeNode("start"), 10);
	//echo json_encode($r->get_childrens());
	$r->add_child(new nodeclass\TreeNode("test"));
	$r->add_child(new nodeclass\TreeNode());
	$r->add_child(new nodeclass\TreeNode());
	$r->add_child(new nodeclass\TreeNode());
	$r->get_child(0)->add_child(new nodeclass\TreeNode());
	$r->get_child(0)->add_child(new nodeclass\TreeNode());
	$r->get_child(0)->add_child(new nodeclass\TreeNode());
	$r->get_child(0)->add_child(new nodeclass\TreeNode());
	$r->get_child("Node2")->add_child(new nodeclass\TreeNode());

	echo $r->repr_tree(), "\n\n";

	echo $r->get_child(0,0)->repr_path(), "\n";

	$r->free();
	
?>