// Variables
var ws = undefined; // websocket instance
var logs = [];
var logsLimit = 3;
var blinkstr = " ";

// Initialize the WebSocket
function initWebSocket() {
    var ipName = window.location.hostname;      //manually input wifi chip IP address to test
    if (ws) {
        ws.onclose(); // close the websocket if open.
    }
    ws = new WebSocket('ws://' + ipName + '/socket');

    ws.onopen = function () { // when handshake is complete:
        log('WebSocket open to aws server ' + ipName);
        
        //Blink recording
        blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
        
    };

    ws.onclose = function () { // when socket is closed:
        log('WebSocket connection to ' + ipName + ' has been closed!');
        
        //Turn off recording blink
        document.getElementById("recordblink").innerHTML = "";
        ws = undefined;
    };

    ws.onmessage = function (event) { // when client receives a WebSocket message:
        //*** Display a new timestamp ***//
        var time = new Date().getTime();
        var date = new Date(time);
        document.getElementById("timestamp").innerHTML = date.toString();
        
        //*** Set the source of the image to the image on the WiFi chip ***//
        document.getElementById("pic").src = "/images/face.jpg?time=" + new Date().getTime();
        
        //Blink recording
        blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
        
    };
	
	ws.onerror = function () { // when an error occurs
		ws.onclose();
		log('Websocket error');
		
	}
}

// Set up event listeners
//*** When the button is clicked, disable it, and depending on whether a Websocket is open or not, either run "initWebSocket()" or "ws.close()" ***//


// Other functions
function log(txt) {
    logs.push({
        'content': txt,
        'type': 'log'
    });
    showLog(logs, 'log', logsLimit);
}

function showLog(logArray, logId, logLimit) {
    var logContent = '';
    var logLength = logArray.length;
    var iStart = logLength - logLimit - 1;
    if (iStart < 0) {
        iStart = 0;
    }
    for (var index = iStart; index < logLength; ++index) {
        logItem = logArray[index];
        logContent += '<span class="' + logItem.type + '">' + logItem.content + '</span><br/>\n'
    }
    document.getElementById(logId).innerHTML = logContent;
}

function initJoy() {
/*	var joystick = new VirtualJoystick({
		container : document.getElementById('joyContainer'),
		mouseSupport : true,
	});
	
	setInterval(function() {
		if(joystick.up())
		{
			console.log("up detected");
		}
		else if(joystick.down())
		{
			console.log("down detected");
		}
		if(joystick.left())
		{
			console.log("left detected");
		}
		else if(joystick.right())
		{
			console.log("right detected");
		}
	}, 1/10 * 1000);	
*/
	//window.addEventListener("keydown", getKey, false);
}

function getKey(e) {
	var keyCode = e.keyCode;
	if(enable) {
		if (keyCode == 87)
		{	
			ws.send(JSON.stringify({
				command: "up"
			}));
		}
		else if (keyCode == 83)
		{	
			ws.send(JSON.stringify({
				command: "down"
			}));
		}

		if (keyCode == 65)
		{	
			ws.send(JSON.stringify({
				command: "left"
			}));
		}
		else if (keyCode == 68)
		{	
			ws.send(JSON.stringify({
				command: "right"
			}));
		}
	}
}

// Define initialization function
function init() {
    initWebSocket();
	//initJoy();
}

// Open Websocket as soon as page loads

//test code for blink
/*function blinkthat() {
    blinkstr = "Recording";
        document.getElementById("recordblink").innerHTML = blinkstr.blink();
}
window.addEventListener("load", blinkthat);*/  
window.addEventListener("load", init, false);
