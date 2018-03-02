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

  self.cancel_booking = function(booking_id, account_id) {
    return new Promise(function(resolve, reject){
      fetch('/booking/' + booking_id + '/cancel/' + account_id, {method: "DELETE", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.cancel_booking_request = function(event_id, receiver_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/cancel_booking_request/' + receiver_id, {method: "DELETE", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.decline_booking_request = function(event_id, sender_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/decline_booking_request/' + sender_id, {method: "DELETE", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

}

// Create and Store New Instance In a Constant
const DELETE = Object.freeze(new Delete());
