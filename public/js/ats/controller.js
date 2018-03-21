app.controller("atsctrl", function ($scope, atsfactory, Upload) {

    var ats={
        file:""
    };
    $scope.fileMessage="";
    $scope.results=true;
    $scope.tvTime="";
    $scope.summ=true;
    ///////////// Upload file ///////////////////////////
    $scope.fileUp = function (file) {
        Upload.upload({
            url: 'http://localhost:1234' + '/uploadFile', //webAPI exposed to upload the file
            data: {
                file: file
            } //pass file as data, should be user ng-model
        }).then(function (data) {
            if (data.data.message != "fail") {
                
                var dataArray=data.data.message;
                var ac = data.data.ac;

                $scope.analysis = dataArray.slice(2,12);
                $scope.kClusters = dataArray.slice(14,19);
                $scope.miClusters = dataArray.slice(21,26);
                $scope.meClusters = dataArray.slice(28,29);
                $scope.agClusters = dataArray.slice(31,32);
                $scope.results=false;
                
                $scope.summary= dataArray.slice(36,);

                var tvtime=dataArray[3];
                var i = tvtime.indexOf(':');
                tvtime = tvtime.slice(i+2,);
                $scope.tvTime = parseFloat(tvtime);

                var cvtime=dataArray[5];
                var j = cvtime.indexOf(':');
                cvtime = cvtime.slice(j+2,);
                $scope.cvTime = parseFloat(cvtime);

                var hvtime=dataArray[7];
                var k = hvtime.indexOf(':');
                hvtime = hvtime.slice(k+2,);
                $scope.hvTime = parseFloat(hvtime);
                
                var timestring=dataArray[33];
                var a=timestring.indexOf('a');
                var b=timestring.indexOf('b');
                var c=timestring.indexOf('c');
                var d=timestring.indexOf('d');
                var e=timestring.indexOf('e');
                var f=timestring.indexOf('f');
                var g=timestring.indexOf('g');
                var h=timestring.indexOf('h');

                var kTime=parseFloat(timestring.slice(a+1,b));
                var miTime=parseFloat(timestring.slice(c+1,d));
                var meTime=parseFloat(timestring.slice(e+1,f));
                var alTime=parseFloat(timestring.slice(g+1,h));
             
                
                var kmacc = ac.ka/1000;
                kmacc = Math.round(kmacc * 100) / 100;
                var minib = ac.mia/1000;
                minib = Math.round(minib * 100) / 100;
                var meanshif = ac.mea/1000;
                meanshif = Math.round(meanshif * 100) / 100;
                var aglom = ac.aga/1000;
                aglom = Math.round(aglom * 100) / 100;

                $scope.result=data.data.message;
                $scope.fileMessage = "Successfull";
                console.log(data.data);

                var newfreqData=[
                    {State:'Tfid V. Time',freq:{K_Means_Clustering:$scope.tvTime, Mini_Batch_Clustering:$scope.tvTime, Mean_Shift_Algorithm:$scope.tvTime, Agglomerative_Clustering:$scope.tvTime}}
                    ,{State:'Count V. Time',freq:{K_Means_Clustering:$scope.cvTime, Mini_Batch_Clustering:$scope.cvTime, Mean_Shift_Algorithm:$scope.cvTime, Agglomerative_Clustering:$scope.cvTime}}
                    ,{State:'Hash V. Time',freq:{K_Means_Clustering:$scope.hvTime, Mini_Batch_Clustering:$scope.hvTime, Mean_Shift_Algorithm:$scope.hvTime, Agglomerative_Clustering:$scope.hvTime}}
                    ,{State:'Accuracy',freq:{K_Means_Clustering:kmacc, Mini_Batch_Clustering:minib, Mean_Shift_Algorithm:meanshif, Agglomerative_Clustering:aglom}}
                    ,{State:'Algorithm Run Time',freq:{K_Means_Clustering:kTime, Mini_Batch_Clustering:miTime, Mean_Shift_Algorithm:meTime, Agglomerative_Clustering:alTime}}
                    ];
                    
                    
                    
                    
                dashboard('#dashboard',newfreqData);

            }
            else {
                $scope.fileMessage = "Error!";
            }
        }, function (error) {
            $scope.fileMessage = "!Error";
        });
    };
    $scope.validateFile = function () {
        if ($scope.uploadFile.file.$valid && $scope.ats.file) {
            $scope.fileUp($scope.ats.file);
            $scope.fileMessage = "Uploading.. & Analyzing..."
        }
        else {
            $scope.fileMessage = "Invalid file only .pdf,.doc,.txt of max 3mb allowed";
        }
    }




    // $scope.savef = function () {
    //     var userObject = {};
    //     var promise = atsfactory.myf(userObject);
    //     promise.then(function (data) {
    //         console.log("SUCCESS ", data.data.msg);
    //         $scope.result = data.data.msg;
    //     }, function (error) {
    //         $scope.result = error;
    //     });
    // }


})