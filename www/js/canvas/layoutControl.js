sections = 11;

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

function tpLayoutF() {
	tpLayoutE();
	sections = 11;
	
	strait_section(8,340,190,240);
	left_turnout_down(6,580,190);
	strait_section_free(9,350,350,505,210);
	
	add_section_box(8,410,190);
	add_section_box(9,410,290);

	sectionMarker(7,580,182);	
	sectionMarker(7,540,182);	
	sectionMarker(8,490,182);	
	sectionMarker(8,490,210);	
	sectionMarker(8,470,182);	
	sectionMarker(9,470,227);	
	sectionMarker(9,356,330);	

	addForwardSignal("36,B,1",530,225,"white");
	addForwardSignalBreakout(1,530,225,180);	
	addForwardSignal("37,B,1",493,188,"white");
	addForwardSignalBreakout(7,488,188,0);	
	addForwardSignal("38,B,1",477,220,"white");
	addForwardSignalBreakout(7,477,220,-45);	

	


/*	
	addForwardSignal("36,B,16",645,575,"white");
	addForwardSignalBreakout(7,645,575,180);	
	addForwardSignal("37,B,16",645,575,"white");
	addForwardSignalBreakout(7,645,575,180);	
	addForwardSignal("38,B,16",645,575,"white");
	addForwardSignalBreakout(7,645,575,180);	
*/	
	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function tpLayoutE() {
	tpLayoutD();
	sections = 7;
	right_turnout_down(2,507,490);
	goTo(2,658,540);	
	first_degree(2,658,220,0.5);		
	strait_section(2,658,540,30);
	strait_section_free(7,930,80,930,350);	
	third_degree(7,730,140,0);
	third_degree(7,730,140,0.25);
	strait_section(7,680,540,50);
	
	sectionMarker(2,640,533);
	sectionMarker(7,700,533);
	sectionMarker(7,923,100);

	addForwardSignal("35,B,1",645,575,"white");
	addForwardSignalBreakout(7,645,575,180);	
	
	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function tpLayoutD() {
	tpLayoutC();
	sections = 6;
	
	right_turnout_up(5,590,435,true);
	first_degree(6,630,90,1.5);
	first_degree(6,630,90,1.75);
	first_degree(6,630,90,0);
	strait_section(6,340,190,290);
	strait_section_free(5,660,420,708,378);
	
	sectionMarker(5,660,405);
	sectionMarker(6,350,183);	
	sectionMarker(6,715,355);	
	
	add_section_box(6,730,300);
	
	// End of bottom right arc
	addForwardSignal("35,B,16",690,420,"white");
	addForwardSignalBreakout(6,690,420,135);
	
	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function tpLayoutC() {
	tpLayoutB();
	sections = 5;
	
	second_degree(3,750,-25,1.5);
	strait_section(4,600,145,75);
	
	second_degree(5,675,85,1.5);
	second_degree(5,675,85,1.75);
	second_degree(5,675,85,0);
	second_degree(5,675,85,0.25);

	left_turnout_up(2,675,490);	
	right_turnout_down(5,507,435);
	
	strait_section(5,530,435,110);
	strait_section(5,635,435,40);	
	strait_section(2,400,435,125);
	add_section_box(5,775,380);
	sectionMarker(5,700,142);
	sectionMarker(5,570,445);
	sectionMarker(2,590,462);
	
	addForwardSignal("34,B,1",640,180,"white");
	addForwardSignalBreakout(1,640,180,180);
	
	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function tpLayoutB() {
	tpLayoutA();
	sections = 4;
	
	left_turnout_up(2,675,490);
	
	strait_section(2,400,435,125);
	first_degree(2,520,335,1.5);
	sectionMarker(2,430,428);
	second_degree(4,400,85,0.5);
	second_degree(4,400,85,0.75);
	second_degree(4,400,85,1);
	second_degree(4,400,85,1.25);
	strait_section(4,400,145,200);
	add_section_box(4,280,200);
	sectionMarker(4,360,424);
	sectionMarker(4,550,138);
	
	// Section 4 arc
	addForwardSignal("33,B,16",400,435,"white");
	addForwardSignalBreakout(1,400,435,0);

	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}

function tpLayoutA() {
	sections = 4;
	
	third_degree(1,400,90,1.25);
	right_turnout_up(1,400,90);
	first_degree(1,556,-65,1.25);
	strait_section(3,550,35,200);	
	add_section_box(3,650,35);
	sectionMarker(3,570,27);
	sectionMarker(3,710,27);

	strait_section(1,500,90,125);
	third_degree(1,675,90,1.5);
	third_degree(1,675,90,1.75);
	third_degree(1,675,90,0);
	add_section_box(1,725,100);
	sectionMarker(1,274,120);
	sectionMarker(1,830,400);
	sectionMarker(1,510,35);
	
	// End of top left arc	
	addForwardSignal("32,B,1",245,140,"white");
	addForwardSignalBreakout(1,245,140,-45);

	third_degree(2,675,90,0.25);
	strait_section(2,400,490,275);
	third_degree(2,400,90,0.5);
	third_degree(2,400,90,0.75);
	third_degree(2,400,90,1);
	add_section_box(2,320,480);
	sectionMarker(2,235,160);
	sectionMarker(2,785,445);
	
	// End of bottom right arc
	addForwardSignal("32,B,16",800,473,"white");
	addForwardSignalBreakout(1,800,473,135);
	
	// End of bottom right arc
	addInvertSignal("33,B,1",550,35,"white");
	addInvertSignalBreakout(1,550,35,0);

	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
		
}

function tpBasic() {
	sections = 2;
	//A basic oval with third_degree curved track
	//2 sections - Sections start one curve before the strait bit
	
	//Section 1
	third_degree(1,400,90,1.25);
	strait_section(1,400,90,100);
	third_degree(1,500,90,1.5);
	third_degree(1,500,90,1.75);
	third_degree(1,500,90,0);
	add_section_box(1,550,100);
	sectionMarker(1,274,120);
	sectionMarker(1,655,400);

	//Section 2
	third_degree(2,500,90,0.25);
	strait_section(2,400,490,100);
	third_degree(2,400,90,0.5);
	third_degree(2,400,90,0.75);
	third_degree(2,400,90,1);
	add_section_box(2,320,480);
	sectionMarker(2,235,160);
	sectionMarker(2,610,445);

	// End of top left arc	
	addForwardSignal("32,B,1",245,140,"white");
	addForwardSignalBreakout(1,245,140,-45);

	// End of top right arc
//	addForwardSignal("32,B,16",650,170,"white");
//	addForwardSignalBreakout(1,650,170,45);
	
	// End of bottom right arc
	addForwardSignal("32,B,16",623,473,"white");
	addForwardSignalBreakout(1,623,473,135);

	// End of bottom left arc
//	addForwardSignal("32,B,1",217,444,"white");
//	addForwardSignalBreakout(1,217,444,225);

	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
}


function drawLayout() {
	sections = 6;
	strait_section(1,50,90,200);
	add_section_box(1,150,90);
	right_turnout_down(2,250,90);
	goTo(2,400,90+55);	
	first_degree(2,400,-175,0.5);
	add_section_box(2,315,120);
	strait_section(3,350,90,250);
	add_section_box(3,450,90);
	first_degree(5,600,-10,1.5);
	strait_section(4,400,90+55,250);
	add_section_box(4,450,90+55);
	left_turnout_up(5,250+150+200+150,90+55);
	add_section_box(5,250+150+275,120);
	strait_section(6,250+150+200+150,90+55,200);
	add_section_box(6,250+150+200+150+50,90+55);

	for (i=1;i<=sections;i++) {
		drawSection(i,'black');
	}
	
	addForwardSignal("33,B,16",250,90,"white");
	addForwardSignalBreakout(1,250,90);
	addForwardSignal("32,B,16",600,90,"white");
	addForwardSignalBreakout(1,600,90);
	
	addReverseSignal("32,B,1",250+150+200+150,90+55,"white");
	addReverseSignalBreakout(1,250+150+200+150,90+55);
	addReverseSignal("33,B,1",250+150,90+55,"white");
	addReverseSignalBreakout(1,250+150,90+55);
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
		signals = data["signals"];
		$.each(signals, function(i,signal) {
			updateSignalColor(signal.id,signal.color);
		});
          })
	  .fail(function() {
          })
}
