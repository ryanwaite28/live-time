'use strict';

const Post = function() {
  var self = this;

  self.signup = function(data) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "POST",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify(data)
      }

      fetch('/signup', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

}

// Create and Store New Instance In a Constant
const POST = Object.freeze(new Post());
