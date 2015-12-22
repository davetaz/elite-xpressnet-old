<?php

	$loco = $_POST["loco"];
	$direction = $_POST["direction"];
	$speed = $_POST["speed"];
	$signal = $_POST["signal"];
	$color = $_POST["color"];
	
	if (isset($loco) {
		processLoco($loco,$direction,$speed);
	}
	
	if (isset($signal) {
		processSignal($signal,$mode,$color);
	}

function callRedis($arg) {
	$cmd = "python /home/pi/elite-xpressnet/redis/redisControl.py " . $arg;
	exec($cmd);
}

function processSignal($signal,$mode,$color) {
	$arg = "signals " . $signal . " " . $mode . " " . $color;
	callRedis($arg);
}

function processLoco($loco,$direction,$speed) {
	if (!is_numeric($loco)){
		exit;
	}

	$arg = "trains " . $loco . " Direction " . $direction;
	if ($direction == "R" || $direction == "F") {
		callRedis($cmd);
	}
}
//	For some reason PHP Redis and Python don't talk nice to each other, hense the direct call to python
//	$redis = new Redis() or die("Can't load redis module");
//	$redis->set('loco','s/d,' . $loco . ',' . $direction . ',' . $speed); 	


# Stage 2, put on elite queue for consumption and processing
//	$redis->set('elite','s/d,' . $loco . ',' . $direction . ',' . $speed);

?>
