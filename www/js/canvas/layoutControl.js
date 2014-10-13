sections = 6;

$.ajaxSetup ({
    // Disable caching of AJAX responses
    cache: false
});

function drawSection(id,color) {  
    var canvas = document.getElementById('canvas' + id);
    var context = canvas.getContext('2d');
    context.lineWidth = 5;
    context.strokeStyle = color;
    context.stroke();
}

function drawLayout() {
	strait_section(1,50,90);
	add_section_box(1,150,90);
	right_turnout_down(2,250,90);
	add_section_box(2,315,120);
	strait_section(3,250+150,90);
	add_section_box(3,450,90);
	strait_section(4,250+150,90+55);
	add_section_box(4,450,90+55);
	left_turnout_up(5,250+150+200+150,90+55);
	add_section_box(5,250+150+275,120);
	strait_section(6,250+150+200+150,90+55);
	add_section_box(6,250+150+200+150+50,90+55);

	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function updateLayout() {
	$.ajax('data/config.json')
	  .done(function(data) {
		trains = data["trains"];
		occupiedSections = [];
		$.each(trains, function(i, obj) {
			train_id = obj.id;
			direction = obj.direction;
			conf_sections = obj.sections;
			for (i=0;i<conf_sections.length;i++) {
				section = conf_sections[i];
				occupySection(section,train_id,direction);
				occupiedSections[section] = true;	
			}
		});
		clearUnoccupiedSections(occupiedSections);
		updateLayout();
          })
	  .fail(function() {
		updateLayout();
          })
}

$(document).ready(function() {
	drawLayout();
	updateLayout();
});

 
