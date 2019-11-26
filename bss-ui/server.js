//Install express server
const express = require('express');
const path = require('path');

const app = express();

// Serve only the static files form the dist directory
app.use(express.static(__dirname + '/dist/itucsdb1941'));

app.get('/*', function(req,res) {
    
res.sendFile(path.join(__dirname+'/dist/itucsdb1941/index.html'));
});

app.get('/sign-page', function(req, res) {
    res.sendFile(path.join(__dirname, 'src', 'sign-page.component.html'));
});

// Start the app by listening on the default Heroku port
app.listen(process.env.PORT || 8080);