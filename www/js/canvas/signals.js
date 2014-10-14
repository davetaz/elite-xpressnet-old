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
