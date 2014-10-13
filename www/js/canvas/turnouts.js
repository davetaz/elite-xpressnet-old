/*
	left_turnout_up
	top_left ends: x-150,y-55
	bottom_left ends: x-150,y
*/
function left_turnout_up(id,x,y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x-30,y);
	context.quadraticCurveTo(x-50,y,x-60,y-15);
	context.lineTo(x-80,y-40);     
	context.quadraticCurveTo(x-90,y-55,x-110,y-55);
	context.lineTo(x-150,y-55);
	context.moveTo(x-30,y);
	context.lineTo(x-150,y);
}

/*
	left_turnout_down
	top_left ends x-150,y
	bottom_left ends: x-150,y+55
*/
function left_turnout_down(id,x,y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x-30,y);
	context.quadraticCurveTo(x-50,y,x-60,y+15);
	context.lineTo(x-80,y+40);     
	context.quadraticCurveTo(x-90,y+55,x-110,y+55);
	context.lineTo(x-150,y+55);
	context.moveTo(x-20,y);
	context.lineTo(x-150,y);
}

/*
	right_turnout_down
	top_right ends x+150,y
	bottom_right x+150,y+55
*/
function right_turnout_down(id,x,y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x+30,y);
	context.quadraticCurveTo(x+50,y,x+60,y+15);
	context.lineTo(x+80,y+40);     
	context.quadraticCurveTo(x+90,y+55,x+110,y+55);
	context.lineTo(x+150,y+55);
	context.moveTo(x+30,y);
	context.lineTo(x+150,y);
}

/*
	right_turnout_up
	top_right ends x+150,y+55
	bottom_rights ends x+150,y
*/
function right_turnout_up(id,x,y) {
	var canvas = document.getElementById('canvas' + id);
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x+30,y);
	context.quadraticCurveTo(x+50,y,x+60,y-15);
	context.lineTo(x+80,y-40);     
	context.quadraticCurveTo(x+90,y-55,x+110,y-55);
	context.lineTo(x+150,y-55);
	context.moveTo(x+30,y);
	context.lineTo(x+150,y);
}
