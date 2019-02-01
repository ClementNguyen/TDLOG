var express = require('express');
var connection = require('../mysql-connection');
var router = express.Router()

//Get products with recommendations 

router.post('/', (req, res) => {
    connection.query('SELECT ID FROM recommendations', function (error, results, fields) {
      if (error) throw error;
      res.send(results)
    });
  });

module.exports = router;