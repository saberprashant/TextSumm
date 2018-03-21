var express = require("express");
var app = express();
app.use(express.static('public'));

var bodyParser = require("body-parser");
var PythonShell = require('python-shell');
var com=require('comp');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(function (request, response, next) {
    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});


const multer = require('multer');
const crypto = require('crypto');


/////functions
var genRandomString= function (length) {
    return crypto.randomBytes(Math.ceil(length / 2))
        .toString('hex')     /** convert to hexadecimal format */
        .slice(0, length);   /** return required number of characters */
};


var summarize = function(filename,response){

    var options = {
    //   mode: 'binary',
      //pythonPath: 'path/to/python',
    //   pythonOptions: ['-u'],
      scriptPath: 'pythonscripts',
      args: [filename]
    };
    
    var array=[];

    var pyshell=new PythonShell.run('summarize2.py',options);
    pyshell.on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        
        array.push(message);
    });
    
    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err){
            throw err;
        };
    
        console.log('finished');

        var kmeans=com.c1(array.slice(14,19),array.slice(36,array.length));
        var minibatch=com.c2(array.slice(21,26),array.slice(36,array.length));
        var meanshift = com.c3(array.slice(28,29),array.slice(36,array.length));
        var aglomerative = com.c4(array.slice(31,32),array.slice(36,array.length));
        
        
        var ac={
            ka:kmeans,
            mia:minibatch,
            mea:meanshift,
            aga:aglomerative
        }

        response.json({"message":array,"ac":ac});

    });

};


/////

var fileStorage = multer.diskStorage({
    destination: function (request, file, callback) {
        callback(null, "./public/Input_Files");
    },
    filename: function (request, file, callback) {
        callback(null, request.myfile.name + '.txt');
    }
});

var uploadFile = multer({
    storage: fileStorage,
    limits: { fileSize: 3000000 },
    fileFilter: function (request, file, cb) {
        if (file.mimetype === 'text/plain') {
            request.myfile.extension = '.txt';
        }
        else if (file.mimetype != 'text/plain') {
            request.fileValidationError = true;
            return cb(null, false, new Error('Invalid file type'));
        }
        cb(null, true);
    }
}).single('file');


app.post('/uploadFile', function (request, response) {

    request.fileValidationError = false;
    request.myfile={};
    request.myfile.name = genRandomString(8);
    try {
        uploadFile(request, response, function (error) {
            if (error) {
                response.json({ message: "fail" });
            } else if (request.fileValidationError === true) {
                response.json({ message: "fail" });
            }
            else {
                console.log("file upload success");
                summarize(request.myfile.name,response);
                // response.json({"message":"success"});
                
            }
        })
    }
    catch (error) {
        logger.error(error);
    }


});


// summarize();
app.listen(1234, function () {
    console.log("Server Start...");
});