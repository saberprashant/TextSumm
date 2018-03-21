app.factory("atsfactory",function($http,$q){
    //var data= {key,value};
    var object = {
        registerUser:function(userObject){
          var defer = $q.defer(); $http.post('http://localhost:1234/register',userObject).then(function(data){
               defer.resolve(data);
           },function(error){
               defer.reject(error);
           }) 
            return defer.promise;
        }
        
        };
    return object;
    });