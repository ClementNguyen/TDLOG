const express = require('express');
const bodyParser = require('body-parser');
const mysql      = require('mysql');
const cors = require('cors');
const tree = require('./product_tree')

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
  password : 'Tdlog77',
  database : 'mopsi'
});

// Initialize the app
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cors());
//app.use(cors(corsOptions));

// https://expressjs.com/en/guide/routing.html
/* app.get('/', function (req, res) {
    connection.query('SELECT * FROM jumia_products WHERE LEFT(Categories,20)="Root Category, Books" LIMIT 0, 20', function (error, results, fields) {
      if (error) throw error;
      res.send(results) 
    });
}); */

function buildSQLQuery(body) {
  sql_query =  'SELECT * FROM jumia_products'
  category = '"Root Category, '+body.post+'"'
  sql_query += ' WHERE LEFT(Categories,'+String(category.length-2)+')='+category
  return sql_query+ ' LIMIT 0, ' +String(body.post_length) 
}

app.post('/', (req, res) => {
  connection.query(buildSQLQuery(req.body), function (error, results, fields) {
    if (error) throw error;
    res.send(results)
  });
});

// Start the server
app.listen(4000, () => {
 console.log('Go to http://localhost:4000/ to see data');
});