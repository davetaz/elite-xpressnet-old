//TODO - Not allow closing of active locos
//FIXME - Speed, Function and Direction feedback, there is a massive race condition, well done Dave! 

directionLock = [];
currentDirection = []; 

$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

$(document).ready(function() {
	$('.toggles').toggles();
	display_3_only();
	loco_monitor();
	setInterval(function(){loco_monitor();},500);
	setInterval(function(){status_monitor();},3000);
	register_event_handlers();
	for (lk=3;lk<20;lk++) {
		register_loco_functions(lk);
	}
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
	$('#pi-interface').on('toggle', function (e, active) {
		if (active) {
			service_control("pi-interface","start");	
		} else {
			service_control("pi-interface","stop");	
		}
	});
	$('#track').on('toggle', function (e, active) {
		if (active) {
			service_control("track","start");	
		} else {
			service_control("track","stop");	
		}
	});
	$('#train').on('toggle', function (e, active) {
		if (active) {
			service_control("train","start");	
		} else {
			service_control("train","stop");	
		}
	});
}

function service_control(service,operation) {
	$.ajax('bin/service.php?service=' + service + '&operation=' + operation)
	.done(function(data) {
		console.log(data);
	})
	.fail(function() {
        })
}

function register_loco_functions(lk) {
	$('#F0-' + lk).on('toggle', function (e, active) {
			if (active) console.log("F0-" + lk + " ON");
			if (!active) console.log("F0-" + lk + " OFF");
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

function status_monitor() {
	$.ajax('data/status.php')
	  .done(function(data) {
		piinterface = false;
		track = false;
		if (data["pi-interface"] == "true") { piinterface = true; }
		if (data["track"] == "true") { track = true; }
		$('#pi-interface-tog').data('toggles').toggle(piinterface);
		$('#track-tog').data('toggles').toggle(track);
	  })
	  .fail(function() {
          })
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
