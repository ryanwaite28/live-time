'use strict';

const Put = function() {
  var self = this;

  self.signin = function(data) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify(data)
      }

      fetch('/signin', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

}

// Create and Store New Instance In a Constant
const PUT = Object.freeze(new Put());
