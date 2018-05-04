var ContinuousVisualization = function(height, width, context) {
    var height = height;
    var width = width;
    var context = context;
    var fontArgs = context.font.split(' ');
    var fontSize = fontArgs[0];

    this.draw = function(objects) {
	for (var i in objects) {
            var p = objects[i];
            if (p.Shape === "airport")
		this.drawAirport(p.x, p.y, p.r, p.Color, p.Filled, p.name, p.queues, p.text_color);
            if (p.Shape === "uav")
		this.drawUAV(p.x, p.y, p.r, p.Color, p.Filled, p.name, p.payload_mass, p.payload_qty, p.fuel, p.src, p.dest, p.text_color);
	};		

    };

    this.drawUAV = function(x, y, radius, color, fill, name, payload_mass, payload_qty, fuel, src, dest, text_color) {
	var cx = x * width;
	var cy = y * height;
	var r = radius;

        context.beginPath();
	context.arc(cx, cy, r, 0, Math.PI * 2, false);
	context.closePath();

	context.strokeStyle = color;
	context.stroke();

	if (fill) {
            context.fillStyle = color;
            context.fill();
	}
	// This part draws the text inside the Circle
        if (name !== undefined) {
            context.fillStyle = text_color;
            context.textAlign = 'start';
            context.textBaseline= 'hanging';
            context.fillText('UAV: ' + name, cx, cy);
            context.fillText('Payload Mass: ' + payload_mass, cx , cy+10);
            context.fillText('Payload Qty: ' + payload_qty, cx , cy+20);
            context.fillText('Fuel: ' + fuel, cx , cy+30);
            context.fillText('Src: ' + src , cx , cy+40);
            context.fillText('Dest: ' + dest , cx , cy+50);
    	};
    };

    this.drawAirport = function(x, y, radius, color, fill, name, queues, text_color) {
	var cx = x * width;
	var cy = y * height;
	var r = radius;

	context.beginPath();
	context.arc(cx, cy, r, 0, Math.PI * 2, false);
	context.closePath();

        context.strokeStyle = color;
	context.stroke();

	if (fill) {
            context.fillStyle = color;
            context.fill();
	}
	// This part draws the text 
        var json_queues = JSON.parse(queues);
        console.log("Drawing airport: " + name);            
        console.log("This airport's queues are:" + queues);
    
        if (name !== undefined) {
            context.fillStyle = text_color;
            context.textAlign = 'start';
            context.textBaseline= 'hanging';
            context.fillText(name, cx, cy);
            context.fillText('Parcels To:', cx , cy+10);
            var i=0;
            for (var key in json_queues){
                if (json_queues.hasOwnProperty(key)) {
                    //context.fillText(" To " + key + ": " + json_queues[key] , cx , cy+i*10+20);
                    context.fillText("-" + key + ": " + json_queues[key][0] 
                            + " / Avg Age [hr]: " + json_queues[key][1]
                            + " / Oldest [hr]: " + json_queues[key][2], cx+2 , cy+i*10+20);
                    i++;
                };
            };

    	};
    };
    
    this.drawRectange = function(x, y, w, h, color, fill) {
        context.beginPath();
	var dx = w * width;
	var dy = h * height;

	// Keep the drawing centered:
	var x0 = (x*width) - 0.5*dx;
	var y0 = (y*height) - 0.5*dy;

	context.strokeStyle = color;
	context.fillStyle = color;
	if (fill)
            context.fillRect(x0, y0, dx, dy);
        else
            context.strokeRect(x0, y0, dx, dy);
	};

    this.resetCanvas = function() {
        context.clearRect(0, 0, height, width);
        context.beginPath();
	};
};

var Simple_Continuous_Module = function(canvas_width, canvas_height) {
	// Create the element
	// ------------------

	// Create the tag:
        var canvas_id = "a";
	var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
	canvas_tag += "style='border:1px dotted'></canvas>";
	// Append it to body:
	var canvas = $(canvas_tag)[0];
	$("#elements").append(canvas);

	// Create the context and the drawing controller:
	var context = canvas.getContext("2d");
	var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

	this.render = function(data) {
		canvasDraw.resetCanvas();
		canvasDraw.draw(data);
	};

	this.reset = function() {
		canvasDraw.resetCanvas();
	};

};