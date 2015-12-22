<?php

$services = ["track","pi-interface"];
$service = $_GET["service"];

if (!in_array($service,$services)) {
	echo "NO SUCH SERVICE";
	exit(1);
}

$operations = ["start","stop","restart","status"];
$operation = $_GET["operation"];

if (!in_array($operation,$operations)) {
	echo "NO SUCH OPERATION";
	exit(1);
}

system('sudo -u pi service ' . $service .  ' ' . $operation . ' 2>&1 > /dev/null',$status);
echo($status);

exit($status);

?>
