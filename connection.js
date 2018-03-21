// Step - 1 require the mongoose module
var mongoose = require("mongoose");
var dbconfig = require("./dbconfig");
// Step -2 Connect to the DB
mongoose.connect(dbconfig.dburl);
module.exports = mongoose;
