var signalColors = [];
var signalData = [];

function toggleSignal(control) {
	id = control.id;
	parts = id.split("-");
	id = parts[1];
	console.log(control);
}

function getAutoBlock(id,x,y,signalID) {
	var auto = true;
	try {
		auto = signalData[signalID].auto;
	} catch(err) {}
	var html = '<control class="control" id="signal-' + id + '-tog-con">Auto:';
	html = html + '<div id="signal-'+id+'-tog" onclick="toggleSignal(this);" style="display: inline-block;" class="toggles toggle-modern" data-toggle-on="'+auto+'" data-toggle-height="24" data-toggle-width="70"></div>';
	html = html + '</control>';
	return html;
}

function getColorControlBlock(id,signalID) {
	var auto = true;
	var aspects = 2;
	try {
		aspects = signalData[signalID].aspects;
		auto = signalData[signalID].auto;
	} catch (err) {}
	var classList = "signal_color";
	if (auto == "true") {
		classList += " signal_disabled";
	}
	var html = '<control class="control" id="signal-'+id+'-color">';
	var colors = ['red','amber','green','amber2'];
	for (i=0;i<aspects;i++) {
		html += '<div id="'+id+'-'+colors[i]+'" class="'+classList+' signal_'+colors[i]+'" onclick="requestSignalChange(\''+signalID+'\',\''+colors[i]+'\');"></div>';
	}
	html += '</control>';
	return html;
}


function loadSignalData(data) {
	var signals = data['signals'];
	$.each(signals, function(i,signal) {
		signalData[signal.id] = signal;
        });
}

function addSignalClickElement(id,x,y) {
	var canvas = document.getElementById('body');
	var signalID = id;
	id = id.replace(",","_");
	id = id.replace(",","_");
	var html = '<div id="signal-' + id + '" onclick="toggleControl(\'signal-'+id+'-controls\');" style="position:absolute; left: '+x+'px; top:'+y+'px; width: 12px; height: 12px;">&nbsp;</div>';
        canvas.insertAdjacentHTML('beforeEnd',html);
	var html = '<div class="signal controls" id="signal-'+id+'-controls" style="position: absolute; left: '+(x-50)+'px; top:'+(y-70)+'px; display: none; z-index: -30; width: 115px; height: 60px; padding-right: 10px;">';
	var auto = getAutoBlock(id,x,y,signalID); html = html + auto;
	var colorControl = getColorControlBlock(id,signalID); html = html + colorControl;
        canvas.insertAdjacentHTML('beforeEnd',html);
/*
	var elements = document.getElementById('elements');
	elem_val = elements.val;
	if (elem_val) {
		elem_val = elem_val + ",signal-" + id;
	} else {
		elem_val = "signal-" + id;
	}
	elements.val = elem_val;
*/
}
function addForwardSignal(id,x,y,color) {
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.arc(x+16,y-16,6,2 * Math.PI, false);
	context.fillStyle = color;
	context.fill();
	context.lineWidth = 1;
	context.strokeStyle = 'black';
	context.stroke();
	addSignalClickElement(id,x+9,y-23);
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
	addSignalClickElement(id,x-23,y+9);
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
	addSignalClickElement(id,x-23,y-23);
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
	var sid = id.replace(",","_");
	sid = sid.replace(",","_");
	$('#'+sid+'-'+color).addClass('current_color');
	if (color == "amber") {
		color = "#FF7E00"
	}
	var canvas = document.getElementById('signal' + id);
	var context = canvas.getContext('2d');
	context.fillStyle = color;
	context.fill();
	context.stroke();
}

function requestSignalChange(id,color) {
	var auto = signalData[id].auto;
        if (auto == "true") {
		return;
        }
        console.log('reqesting colour change for signal ' + id + ' to color ' + color);
        $.post("server.php", { "signal": id, "color": color })
                .done(function(data) {
                        console.log(data);
                });
}

