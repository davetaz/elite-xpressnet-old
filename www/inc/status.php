<?php

$services = ["track","pi-interface"];

function getStatus() {
	global $services;
	for($i=0;$i<count($services);$i++) {
		$out[$services[$i]] = getServiceStatus($services[$i]);
	}
	header('Content-Type: application/json');
	echo json_encode($out);
}

function getServiceStatus($item) {
	system('/usr/sbin/service ' . $item .  ' status 2>&1 > /dev/null',$status);
	if ($status > 0) {
		$status = "false";
	} else {
		$status = "true";
	}
	return $status;
}


?>
