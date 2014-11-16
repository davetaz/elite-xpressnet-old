//TODO - Not allow closing of active locos
//FIXME - Speed, Function and Direction feedback, there is a massive race condition, well done Dave! 

directionLock = [];
currentDirection = []; 

$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

$(document).ready(function() {
	display_3_only();
	loco_monitor();
	setInterval(function(){loco_monitor();},500);
	register_event_handlers();
});

function display_3_only() {
	for(i=4;i<128;i++) {
		$('#loco_'+i).css('display','none');
	}
}

function lockDirection(loco) {
	console.log("locking " + loco);
	directionLock[loco] = true;
}

function unlockDirection(loco) {
	console.log("unlocking " + loco);
	directionLock[loco] = false;
}

function register_event_handlers() {
	$("a").click(function(event) {
    		id = this.id;
		bits = id.split('_');
		if (bits[0] == "reverse" || bits[0] == "forward") {
			set_direction(bits[0],bits[1],this);
			lockDirection(bits[1]);
			setTimeout(function(){unlockDirection(bits[1]);},3000);
		}
		if (bits[0] == "hide") {
			node = "loco_" + bits[1];
			$("#"+node).fadeOut('slow');
		}
	});
}

function requestDirectionChange(loco,direction) {
	if (direction == "forward") {
		direction = "F";
	} else if (direction == "reverse") {
		direction = "R";
	} else {
		return;
	}
	console.log('reqested');
	$.post("server.php", { "loco": loco, "direction": direction })
		.done(function(data) {
			console.log(data);
		});
}

function set_direction(direction,loco,element) {
	if (directionLock[loco]) {
		return;
	}
	if (direction != currentDirection[loco]) {
		requestDirectionChange(loco,direction);
	}
	if (direction == "F" || direction == "f") {
		direction = "forward";
	}
	if (direction == "R" || direction == "r") {
		direction = "reverse";
	}
	if (element == null) {
		element = {};
		element.id = direction + "_" + loco;
	}
	opposite_id = "forward_" + loco;
	if(direction == "forward") {
		opposite_id = "reverse_" + loco;
	}
	if ($('#'+element.id).hasClass('ui-btn-down-c')) {
	} else {
		$('#'+element.id).addClass('ui-btn-down-c');
		$('#'+opposite_id).removeClass('ui-btn-down-c');
	}
}

var prev = new Array();
for (i=3;i<128;i++) {
	prev[i] = 0;
}

var autoRouteTimeout;

function autoRoute(obj) {
	if (autoRouteTimeout) return;
	sections = obj.sections;
	speed = obj.speed;
	direction = obj.direction;
	if (sections.length > 1) return;
	if (speed > 0 ) return;
	if (sections[0] == 1 && direction == "R") {
		console.log("Forward timeout request");
		autoRouteTimeout = setTimeout(function() { requestDirectionChange(obj.id,"forward"); autoRouteTimeout = false; },10000);
	} else if (sections[0] == 6 && direction == "F") {
		console.log("Reverse timeout request");
		autoRouteTimeout = setTimeout(function() { requestDirectionChange(obj.id,"reverse"); autoRouteTimeout = false; },10000);
	}
}

function loco_monitor() {
	$.ajax('data/config.json')
	  .done(function(data) {
		trains = data["trains"];
		$.each(trains, function(i, obj) {
			node_id = "loco_" + obj.id;
			if (!$("#"+node_id).is(':visible') && obj.speed > 0) {
				$("#"+node_id).fadeIn('slow');
			}
			if (prev[obj.id] != obj.speed) {
				$('#speed-'+obj.id).val(obj.speed);
				$('#speed-'+obj.id).slider('refresh');
				prev[obj.id] = 	obj.speed;
			}
			set_direction(obj.direction,obj.id,null);
			currentDirection[obj.id] = obj.direction;
			autoRoute(obj);
		});
          })
	  .fail(function() {
          })
}
