const express = require('express');
const bodyParser = require('body-parser');
const mysql      = require('mysql');
const cors = require('cors');

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

const connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'Caocabenoe78',
  database : 'mopsi'
});

// Initialize the app
const app = express();

app.use(cors());
//app.use(cors(corsOptions));

// https://expressjs.com/en/guide/routing.html
app.get('/', function (req, res) {
    //connection.connect();

    connection.query('SELECT * FROM jumia_products LIMIT 0, 20', function (error, results, fields) {
      if (error) throw error;
      res.send(results)
    });

    //connection.end();
});
// Start the server
app.listen(4000, () => {
 console.log('Go to http://localhost:4000/ to see data');
});