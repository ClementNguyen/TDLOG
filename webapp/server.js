const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

var products_controller = require('./controllers/products-controller')
var recommended_controller = require('./controllers/recommended-controller')
var recommendations_controller = require('./controllers/recommendations-controller')

var whitelist = ['http://localhost:3000']
var corsOptions = {
  origin: function (origin, callback) {
    if (whitelist.indexOf(origin) !== -1) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  }
}

// Initialize the app
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cors());
//app.use(cors(corsOptions));


//Requests for list of products 
app.use('/', products_controller);

//Requests for products with recommendations
app.use('/recommended', recommended_controller);

//Requests for recommended product
app.use('/recommendations', recommendations_controller);

// Start the server
app.listen(4000,'0.0.0.0', () => {
  console.log('Listening on port 4000');
}); 