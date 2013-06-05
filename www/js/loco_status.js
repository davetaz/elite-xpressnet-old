$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

$(document).ready(function() {
	loco_monitor();
});

var prev = new Array();
prev[3] = 0;

function loco_monitor() {
	$.ajax('data/locos.json')
	  .done(function(data) {
		if (prev[3] != data) {
			console.log(data);
			$('#loco-3').val(data);
			$('#loco-3').slider('refresh');
			prev[3] = data;
        	}
		loco_monitor();
          })
	  .fail(function() {
		loco_monitor();
          })
}
