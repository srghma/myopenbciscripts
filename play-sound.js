var { Server } = require('node-osc')
var Speaker = require("speaker");
var lame = require("lame");
var fs = require("fs");
var volume = require("pcm-volume");

var readable = fs.createReadStream("pinknoise.wav");

// see node-lame documentation for more information
var decoder = new lame.Decoder({
    channels: 2,
    bitDepth: 16,
    sampleRate: 44100,
    bitRate: 128,
    outSampleRate: 22050,
    mode: lame.STEREO
});

// Initialize speaker
var speaker = new Speaker();


// Create a volume instance
var v = new volume();

// Wait 5s, then change the volume to 50%
setTimeout(function() {
  v.setVolume(0.5);
}, 5000)

v.pipe(new Speaker()); // pipe volume to speaker
decoder.pipe(v); // pipe PCM data to volume
readable.pipe(decoder); // pipe file input to decoder

var audio = new Audio("pinknoise.wav");
audio.play();

var oscServer = new Server(4546, '0.0.0.0', () => {
  console.log('OSC Server is listening');
});

oscServer.on('/feedback/0', function (msg) { console.log(`Message0: ${msg}`); });
oscServer.on('/feedback/1', function (msg) { console.log(`Message1: ${msg}`); });
