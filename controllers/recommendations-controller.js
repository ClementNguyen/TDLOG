var express = require('express');
var connection = require('../mysql-connection');
var router = express.Router()

//Get recommendations of a product

router.post('/', (req, res) => {
    connection.query('SELECT Similar, Complementary FROM recommendations WHERE ID="' + req.body.ID + '"', function (error, results, fields) {
        if (error) throw error;
        if (results.length==0) {
            res.send([,])
        }
        else {
            var similar = (results[0].Similar).split('  ')
            var complementary = (results[0].Complementary).split('  ')
            let sql_query_similar = 'SELECT * FROM jumia_products WHERE ID="' + similar[0] + '"'
            let sql_query_complementary = 'SELECT * FROM jumia_products WHERE ID="' + complementary[0] + '"'
            for (let i = 1; i < similar.length; i++) {
                sql_query_similar += ' OR ID="' + similar[i] + '"'
            }
            for (let i = 1; i < complementary.length; i++) {
                sql_query_complementary += ' OR ID="' + complementary[i] + '"'
            }
            connection.query(sql_query_similar, function (error, results1, fields) {
                if (error) throw error;
                connection.query(sql_query_complementary, function (error, results2, fields) {
                    if (error) throw error;
                    res.send([results1, results2])
                });
            });
        }
    });
});

module.exports = router; 