'use strict';

const Put = function() {
  var self = this;

  /* --- */

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

  /* --- */

  self.update_info = function(data) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify(data)
      }

      fetch('/account/update_info', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_icon = function(file, prev_ref) {
    return new Promise(function(resolve, reject){
      var form_data = new FormData();
      form_data.append("icon_photo", file);
      form_data.append("prev_ref", prev_ref);

      var params = {
        method: "PUT",
        credentials: "include",
        body: form_data
      }

      fetch('/account/update_icon', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_background = function(file, prev_ref) {
    return new Promise(function(resolve, reject){
      var form_data = new FormData();
      form_data.append("background_photo", file);
      form_data.append("prev_ref", prev_ref);

      var params = {
        method: "PUT",
        credentials: "include",
        body: form_data
      }

      fetch('/account/update_background', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_social = function(data) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify(data)
      }

      fetch('/account/update_social', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_username = function(username) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify({ username: username })
      }

      fetch('/account/update_username', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_account_email = function(email) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify({ email: email })
      }

      fetch('/account/update_account_email', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_booking_email = function(booking_email) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify({ booking_email: booking_email })
      }

      fetch('/account/update_booking_email', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_password = function(password) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        headers: headers_json(),
        body: JSON.stringify({ password: password })
      }

      fetch('/account/update_password', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.update_event = function(event_id, data) {
    return new Promise(function(resolve, reject){
      var form_data = new FormData();
      form_data.append("title", data.title);
      form_data.append("desc", data.desc);
      form_data.append("categories", data.categories);
      form_data.append("location", data.location);
      form_data.append("link", data.link);
      form_data.append("prev_ref", data.prev_ref);
      form_data.append("date_str", data.date_str);
      form_data.append("date_concat", data.date_concat);
      if(data.file) {
        form_data.append("event_photo", data.file);
      }

      var params = {
        method: "PUT",
        credentials: "include",
        body: form_data
      }

      fetch('/event/' + event_id + '/update', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.edit_comment = function(comment_id = 0, text = '') {
    if(!text || text.constructor !== String) { return; }
    return new Promise(function(resolve, reject){
      var params = {
        method: "PUT",
        credentials: "include",
        header: headers_json(),
        body: JSON.stringify({text: text.trim()})
      }

      fetch('/comment/' + comment_id + '/edit', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  /* --- */

}

// Create and Store New Instance In a Constant
const PUT = Object.freeze(new Put());
