const express = require('express');
const app = express();
const server = require('http').createServer(app);
const fs = require('fs');

// ------------------------------------
// ---           WEBSITE            ---
// ------------------------------------
// Static folders (the whole folder is reachable)
app.use('/db', express.static(__dirname + '/client/db'));
app.use('/css', express.static(__dirname + '/client/css'));
app.use('/libs', express.static(__dirname + '/client/libs'));
app.use('/js', express.static(__dirname + '/client/js'));
app.use('/resources', express.static(__dirname + '/client/resources'));


app.get('/ideabox', function (req, res) {
  res.sendFile(__dirname + '/client/ideabox.html');
});

app.get('/help', function (req, res) {
  res.sendFile(__dirname + '/client/help.html');
});

app.get('/patchnote', function (req, res) {
  res.sendFile(__dirname + '/client/patchnote.html');
});

app.get('/events', function (req, res) {
  res.sendFile(__dirname + '/client/events.html');
});

app.get('/pokedex', function (req, res) {
  res.sendFile(__dirname + '/client/pokedex.html');
});

app.get('/stats', function (req, res) {
  res.sendFile(__dirname + '/client/stats.html');
});

// ------------------------------------
// ---          WEB SERVER          ---
// ------------------------------------

// Launch the Web Server on port 80
server.listen(14623);
