//TODO - Not allow closing of active locos
//FIXME - Speed, Function and Direction feedback, there is a massive race condition, well done Dave! 


$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

$(document).ready(function() {
	display_3_only();
	loco_monitor();
	register_event_handlers();
});

function display_3_only() {
	for(i=4;i<128;i++) {
		$('#loco_'+i).css('display','none');
	}
}

function register_event_handlers() {
	$("a").click(function(event) {
    		id = this.id;
		bits = id.split('_');
		if (bits[0] == "reverse" || bits[0] == "forward") {
			set_direction(bits[0],bits[1],this);
		}
		if (bits[0] == "hide") {
			node = "loco_" + bits[1];
			$("#"+node).fadeOut('slow');
		}
	});
}

function set_direction(direction,loco,element) {
	if (direction == "f") {
		direction = "forward";
	}
	if (direction == "r") {
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

function loco_monitor() {
	$.ajax('data/locos.json')
	  .done(function(data) {
		$.each(data, function(i, obj) {
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
		});
		loco_monitor();
          })
	  .fail(function() {
		loco_monitor();
          })
}
