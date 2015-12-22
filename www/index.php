<?php
	require_once('inc/status.php');	
?>
<!DOCTYPE html>
<html>
<head>
	<title>DCC xPressNet Control</title>
	<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="css/rail.css" />
	<link rel="stylesheet" href="css/jquery.mobile-1.3.1.min.css" />
	<link rel="stylesheet" href="css/toggles.css" />
	<link rel="stylesheet" href="css/themes/toggles-modern.css" />
	<script src="js/jquery-1.9.1.min.js"></script>
	<script src="js/jquery.mobile-1.3.1-davetaz.js"></script>
	<script src="js/toggles.js"></script>
	<script src="js/toggles-min.js"></script>
	<script src="js/loco_status.js"></script>
</head>

<body>
<div data-role="page" style="min-width: 430px">
	<div data-role="header">
		<h1>xPressNet Control</h1>
		<a href="#" id="loco-chooser" data-role="button" data-icon="plus" data-iconpos="left" data-mini="true" data-inline="true" class="ui-btn-right">Add Loco</a>
	</div>
	<div id="layout">
	<iframe id="layoutFrame" src="layout.html?layout=endtoend" style="width: 100%; height: 200px;"></iframe>
	</div>
	<div class="loco controls">
		<b>Systems</b><br/>
		<control class="control" id="pi-interface">Commander:<div id="pi-interface-tog" style="display: inline-block;" class="toggles toggle-modern" data-toggle-on="<?php echo getServiceStatus('pi-interface'); ?>" data-toggle-height="24" data-toggle-width="70"></div></control>
		<control class="control" id="track">Track electronics:<div id="track-tog" style="display: inline-block;" class="toggles toggle-modern" data-toggle-on="<?php echo getServiceStatus('track'); ?>" data-toggle-height="24" data-toggle-width="70"></div></control>
		<control class="control" id="train">DCC control:<div id="train-tog" style="display: inline-block;" class="toggles toggle-modern" data-toggle-on="false" data-toggle-height="24" data-toggle-width="70"></div></control>
	</div>
<?php
	for ($i=3;$i<20;$i++) {
		draw_loco($i);
	}

?>

	</div><!-- /content -->
<!--
	<div data-role="footer">
		<h4>&copy; David Tarrant</h4>
	</div>
-->
</div><!-- /page -->

<script src="js/frameHandler.js"></script>

</body>
</html>

<?php

function draw_loco($id) {
echo '		<form id="loco_'.$id.'" class="loco">
		    <label class="loco_label" for="loco-'.$id.'">Loco '.$id.':</label>
		    <a class="hide" href="#" id="hide_'.$id.'" data-role="button" data-mini="true" data-icon="delete" data-iconpos="notext" class="ui-btn-right"></a>
		    <input type="range" name="speed-'.$id.'" id="speed-'.$id.'" data-highlight="true" min="0" max="127" value="0">
		    <div id="direction_panel" class="direction_panel">
		    	<div data-role="controlgroup" data-type="horizontal">
				<a href="#" id="reverse_'.$id.'" data-role="button" data-icon="arrow-l" data-iconpos="left" data-mini="true" data-inline="true">Rev.</a>
				<a href="#" id="forward_'.$id.'" data-role="button" data-icon="arrow-r" data-iconpos="right" data-mini="true" data-inline="true" class="ui-btn-down-c">Fw.</a>
			</div>
		    </div>
		    <div id="function_panel" class="function_panel">
		    	<label class="function_label" for="F0-'.$id.'">Direction Lights:</label>
			<div id="F0-'.$id.'" style="display: inline-block;" class="toggles toggle-modern" data-toggle-on="false" data-toggle-height="24" data-toggle-width="70"></div>
		    </div>
		</form>';
}
?>

