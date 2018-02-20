'use strict';

const Delete = function() {
  var self = this;

  self.delete_account = function() {
    return new Promise(function(resolve, reject){
      var params = {
        method: "DELETE",
        credentials: "include"
      }

      fetch('/account/delete', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.delete_event = function(event_id = 0) {
    if(event_id.constructor !== Number) { return; }
    return new Promise(function(resolve, reject){
      var params = {
        method: "DELETE",
        credentials: "include"
      }

      fetch('/event/' + event_id + '/delete', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.delete_comment = function(comment_id = 0) {
    if(comment_id.constructor !== Number) { return; }
    return new Promise(function(resolve, reject){
      var params = {
        method: "DELETE",
        credentials: "include"
      }

      fetch('/comment/' + comment_id + '/delete', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

}

// Create and Store New Instance In a Constant
const DELETE = Object.freeze(new Delete());
