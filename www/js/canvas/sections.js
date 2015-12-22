sectionIsOccupied = [];
for (i=1;i<=sections;i++) {
	sectionIsOccupied[i] = false;
}

function goTo(id,x,y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
}

function strait_section(id,x,y,length) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x+length,y);
}

function strait_section_free(id,x,y,to_x,to_y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(to_x,to_y);
}

function third_degree(id,x,y,angle) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	angle2 = angle + 0.25;
	if (angle2 == 2) {
		angle2 = 0;
	}
	context.arc(x,y+200,200,(Math.PI * angle),(Math.PI * angle2),false);
}

function second_degree(id,x,y,angle) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	angle2 = angle + 0.25;
	if (angle2 == 2) {
		angle2 = 0;
	}
	context.arc(x,y+205,145,(Math.PI * angle),(Math.PI * angle2),false);
}

function first_degree(id,x,y,angle) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	angle2 = angle + 0.25;
	if (angle2 == 2) {
		angle2 = 0;
	}
	context.arc(x,y+210,110,(Math.PI * angle),(Math.PI * angle2),false);
}

function add_section_box(id,x,y) {
	x = x - 15;
	y = y - 15;
	var canvas = document.getElementById('body');
	var html = '<div id="sectionText' + id + '" style="position:absolute; left: '+x+'px; top:'+y+'px; border: 1px solid black; border-radius: 5px; padding: 2px 5px 2px 5px; width: 40px; height: 20px; color: white; background-color: black;">T----</div>';
	canvas.insertAdjacentHTML('beforeEnd',html);
	var elements = document.getElementById('elements');
	elem_val = elements.val;
	if (elem_val) {
		elem_val = elem_val + ",sectionText" + id;
	} else {
		elem_val = "sectionText" + id;
	}
	elements.val = elem_val;
}

function sectionMarker(id,x,y) {
	var canvas = document.getElementById('static');
	var context = canvas.getContext('2d');
	context.rect(x,y,15,15);
}

function clear_section_box(id) {
	var box = document.getElementById('sectionText'+id);
	box.innerHTML = "T----"
}
function update_section_box(id,tid,dir) {
	if (tid < 10) {
		outid = "T00" + tid;
	} else if (tid < 100) {
		outid = "T0" + tid;
	}
	if (dir == "F" || dir == "f") {
		outid = outid + "&gt;";
	}
	if (dir == "R" || dir == "r") {
		outid = "&lt;" + outid;
	}
	document.getElementById('sectionText'+id).innerHTML = outid;
}
function occupySection(id,tid,dir) {
    sectionIsOccupied[id] = true;
    update_section_box(id,tid,dir);
    var color='red';
    var canvas = document.getElementById('canvas' + id);
    var context = canvas.getContext('2d');
    context.lineWidth = 5;
    context.strokeStyle = color;
    context.stroke();
}
function clearSection(id) {
    if (sectionIsOccupied[id] == false) {
    	return;
    }
    sectionIsOccupied[id] = false; 
    clear_section_box(id);
    var color='black';
    var canvas = document.getElementById('canvas' + id);
    var context = canvas.getContext('2d');
    context.lineWidth = 5;
    context.strokeStyle = color;
    context.stroke();
}
function clearUnoccupiedSections(occupiedSections) {
    for (i=1;i<=sections;i++) {
    	if (occupiedSections[i]) {
	} else {
		clearSection(i);
	}
    }
}

