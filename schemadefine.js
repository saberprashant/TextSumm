// Step -3 Represent Schema
var mongoose = require("./connection");
var Schema = mongoose.Schema;
// Step -4  Creating Schema for the Collection
var docSchema= new Schema({
    filename:String,
});

var doc = mongoose.model("documents",docSchema); 

module.exports=doc;