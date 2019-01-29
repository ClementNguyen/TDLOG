var mysql = require('mysql');
var connection;

function connectDatabase() {
    if (!connection) {
        connection = mysql.createConnection({
            host: 'localhost',
            user: 'root',
            password: 'Tdlog77',
            database: 'mopsi'
        });
        connection.connect(function (err) {
            if (!err) {
                console.log('Database is connected!');
            } else {
                console.log('Error connecting database!');
            }
        });
    }
    return connection;
}

module.exports = connectDatabase();