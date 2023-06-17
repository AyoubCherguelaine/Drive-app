const express = require('express');

const http = require('http');
const socketIO = require('socket.io');
const session = require('express-session');



const auth = require("./controllers/Auth")
const dashboard = require("./controllers/dashboad")

const app = express();
const server = http.createServer(app);
const io = socketIO(server);

// Serve static files from a folder called 'public'
app.use(express.static('public'));




// Configure session middleware
app.use(session({
  secret: 'your-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 24 * 60 * 60 * 1000 // 24 hours in milliseconds
  }
}));

// Set up EJS as the template engine
app.set('view engine', 'ejs');
// Middleware to parse the request body
app.use(express.urlencoded({ extended: true }));

app.use(auth)
app.use(dashboard)




// Start the server
const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});