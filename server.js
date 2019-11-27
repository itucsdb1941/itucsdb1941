//Install express server
const express = require('express');
const path = require('path');

const app = express();
const server = require('http').Server(app);

app.use(express.static(__dirname, 'dist', {index: false}));

server.listen(port, function() {
    console.log("App running on port " + port);
})
// Serve only the static files form the dist directory
app.use(express.static(__dirname + '/dist/itucsdb1941'));


// Start the app by listening on the default Heroku port
app.listen(process.env.PORT || 8080);