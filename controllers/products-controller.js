var express = require('express');
var connection = require('../mysql-connection');
var router = express.Router()

//Get list of products 

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

router.post('/', (req, res) => {
  connection.query(buildSQLQuery(req.body), function (error, results, fields) {
    if (error) throw error;
    res.send(results)
  });
});

module.exports = router;