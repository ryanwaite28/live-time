'use strict';

const Get = function() {
  var self = this;

  self.check_session = function() {
    return new Promise(function(resolve, reject){
      fetch('/check_session', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

}

// Create and Store New Instance In a Constant
const GET = Object.freeze(new Get());
