<?php

	$loco = $_POST["loco"];
	$direction = $_POST["direction"];
	$speed = $_POST["speed"];
	
# Stage 1, put on loco queue for redis to update the file.

	$redis = new Redis() or die("Can't load redis module");
	$redis->connect('127.0.0.1');
	$redis->set('loco','s/d,' . $loco . ',' . $direction . ',' . $speed); 	

# Stage 2, put on elite queue for consumption and processing
	$redis->set('elite','s/d,' . $loco . ',' . $direction . ',' . $speed);

?>
