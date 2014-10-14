<?php

	$loco = $_POST["loco"];
	$direction = $_POST["direction"];
	$speed = $_POST["speed"];
	
	if (!is_numeric($loco)){
		exit;
	}

	$string = $loco . ',direction,'.$direction;
	$cmd = "python /home/pi/rail/redis/redisControl.py " . $loco . " Direction " . $direction;
	if ($direction == "R" || $direction == "F") {
		exec($cmd);
	}

//	For some reason PHP Redis and Python don't talk nice to each other, hense the direct call to python
//	$redis = new Redis() or die("Can't load redis module");
//	$redis->set('loco','s/d,' . $loco . ',' . $direction . ',' . $speed); 	


# Stage 2, put on elite queue for consumption and processing
//	$redis->set('elite','s/d,' . $loco . ',' . $direction . ',' . $speed);

?>
