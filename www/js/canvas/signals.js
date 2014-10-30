signalColors = [];
function addForwardSignal(id,x,y,color) {
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.arc(x+16,y-16,6,2 * Math.PI, false);
	context.fillStyle = color;
	context.fill();
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function addReverseSignal(id,x,y,color) {
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.arc(x-16,y+16,6,2 * Math.PI, false);
	context.fillStyle = color;
	context.fill();
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function addInvertSignal(id,x,y,color) {
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.arc(x-16,y-16,6,2 * Math.PI, false);
	context.fillStyle = color;
	context.fill();
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function addForwardSignalBreakout(id,x,y,angle) {
	var canvas = document.getElementById('static');
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	if (angle == 45) {
		x=x-8;
		y=y-20;
		context.moveTo(x,y);
		context.lineTo(x+10,y-10);
		context.lineTo(x+20,y);
	} else if (angle == -45) {
		x=x+12;
		y=y+8;
		context.moveTo(x,y);
		context.lineTo(x-10,y-10);
		context.lineTo(x,y-20);
	} else if (angle == 135) {
		x=x+20;
		y=y-40;
		context.moveTo(x,y);
		context.lineTo(x+10,y+10);
		context.lineTo(x,y+20);
	} else if (angle == 180) {
		x=x+36;
		y=y-32;
		context.moveTo(x,y);
		context.lineTo(x,y+16);
		context.lineTo(x-16,y+16);
	} else if (angle == 225) {
		x=x+40;
		y=y-11;
		context.moveTo(x,y);
		context.lineTo(x-10,y+10);
		context.lineTo(x-20,y);
	} else {
		context.lineTo(x,y-16);
		context.lineTo(x+16,y-16);
	}
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function addReverseSignalBreakout(id,x,y,angle) {
	var canvas = document.getElementById('static');
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x,y+16);
	context.lineTo(x-16,y+16);
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function addInvertSignalBreakout(id,x,y,angle) {
	var canvas = document.getElementById('static');
	var context = canvas.getContext('2d');
	context.moveTo(x,y);
	context.lineTo(x,y-16);
	context.lineTo(x-16,y-16);
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
}
function updateSignalColor(id,color) {
	if (signalColors[id] == color) {
		return;
	} 
	signalColors[id] == color;
	if (color == "amber") {
		color = "#FF7E00"
	}
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.fillStyle = color;
	context.fill();
	context.stroke();
}
