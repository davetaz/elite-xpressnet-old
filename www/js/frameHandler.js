$('#layoutFrame').load(function() {
	addFrameListeners();
});

function addFrameListeners() {
	var iframe = $('#layoutFrame').contents();
	elements = iframe.find('#elements');
	elements = elements[0].val;
	elems = elements.split(',');
	for (i=0;i<elems.length;i++) {
		addFrameListener(iframe,elems[i]);
	}
}

function addFrameListener(frame,thing) {
	elem = frame.find('#' + thing);
	elem.click(function() {
		// We know what the user has clicked in the layout :)
		console.log('captured click in iframe for ' + thing);	
	});
}
