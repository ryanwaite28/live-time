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

  self.create_event = function(data) {
    return new Promise(function(resolve, reject){
      var form_data = new FormData();
      form_data.append("title", data.title);
      form_data.append("desc", data.desc);
      form_data.append("categories", data.categories);
      form_data.append("location", data.location);
      form_data.append("link", data.link);
      form_data.append("date_str", data.date_str);
      form_data.append("date_concat", data.date_concat);
      if(data.file) {
        form_data.append("event_photo", data.file);
      }

      var params = {
        method: "POST",
        credentials: "include",
        body: form_data
      }

      fetch('/venue/create_event', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.toggle_event_attending = function(event_id) {
    return new Promise(function(resolve, reject){
      fetch('/event/' + event_id + '/toggle_attending', {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.toggle_event_like = function(event_id) {
    return new Promise(function(resolve, reject){
      fetch('/event/' + event_id + '/toggle_like', {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.toggle_comment_like = function(comment_id) {
    return new Promise(function(resolve, reject){
      fetch('/comment/' + comment_id + '/toggle_like', {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.toggle_account_follow = function(account_id) {
    return new Promise(function(resolve, reject){
      fetch('/accounts/' + account_id + '/toggle_follow', {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.create_event_comment = function(event_id = 0, text = '') {
    if(!event_id || event_id.constructor !== Number) { return; }
    if(!text || text.constructor !== String) { return; }
    return new Promise(function(resolve, reject){
      var params = {
        method: "POST",
        credentials: "include",
        header: headers_json(),
        body: JSON.stringify({text: text.trim()})
      }

      fetch('/event/' + event_id + '/create_comment', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.send_account_message = function(account_id = 0, message = '') {
    if(!account_id || account_id.constructor !== Number) { return; }
    if(!message || message.constructor !== String) { return; }
    return new Promise(function(resolve, reject){
      var params = {
        method: "POST",
        credentials: "include",
        header: headers_json(),
        body: JSON.stringify({message: message.trim()})
      }

      fetch('/accounts/' + account_id + '/send_message', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.send_booking_request = function(event_id, receiver_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/send_booking_request/' + receiver_id, {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.accept_booking_request = function(event_id, sender_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/accept_booking_request/' + sender_id, {method: "POST", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

}

// Create and Store New Instance In a Constant
const POST = Object.freeze(new Post());
