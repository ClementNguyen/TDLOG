const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');
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
  host: 'localhost',
  user: 'root',
  password: 'Tdlog77',
  database: 'mopsi'
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
  sql_query = 'SELECT * FROM jumia_products'
  length = body.post_length
  //If request is search by ID
  if (length == -1) {
    sql_query += ' WHERE ID="' + body.post + '"'
    length = 1
  }
  //If request is search recommendations
  else if (length == -2) {
    id = body.post
    sql_query += ' WHERE ID="' + id[0].ID + '"'
    for (let i = 0; i < id.length; i++) {
      sql_query += ' OR ID="' + id[i].ID + '"'
    }
    length = id.length
  }
  else {
    category = '"Root Category, ' + body.post + '"'
    sql_query += ' WHERE LEFT(Categories,' + String(category.length - 2) + ')=' + category
  }
  return sql_query + ' LIMIT 0, ' + String(length)
}

//Requests for list of products 
app.post('/', (req, res) => {
  connection.query(buildSQLQuery(req.body), function (error, results, fields) {
    if (error) throw error;
    res.send(results)
  });
});


//Requests for products with recommendations
app.post('/recommendations', (req, res) => {
  connection.query('SELECT ID FROM recommendations', function (error, results, fields) {
    if (error) throw error;
    res.send(results)
  });
});

//Requests for recommended product
app.post('/recommendations1', (req, res) => {
  rec_id = []
  //connection.query('SELECT Recommendation1, Recommendation2, Recommendation3 FROM recommendations WHERE ID="BA204EL1M2GAYNAFAMZ"', function (error, results, fields) {
  connection.query('SELECT Recommendation1, Recommendation2, Recommendation3 FROM recommendations WHERE ID="' + req.body.ID +'"', function (error, results, fields) {
    if (error) throw error;
    res1 = results[0]
    rec_id = [res1.Recommendation1, res1.Recommendation2, res1.Recommendation3]
    connection.query('SELECT * FROM jumia_products WHERE ID="' + rec_id[0] + '" OR ID="' + rec_id[1] + '" OR ID="' + rec_id[2] + '"', function (error, results, fields) {
      if (error) throw error;
      res.send(results)
    });
  });
});


// Start the server
app.listen(4000, () => {
  console.log('Go to http://localhost:4000/ to see data');
});