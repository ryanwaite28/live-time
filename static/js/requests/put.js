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

      fetch('/user/update_info', params)
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

      fetch('/user/update_icon', params)
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

      fetch('/user/update_background', params)
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

      fetch('/user/update_social', params)
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

      fetch('/user/update_username', params)
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

      fetch('/user/update_account_email', params)
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

      fetch('/user/update_booking_email', params)
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

      fetch('/user/update_password', params)
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  /* --- */

}

// Create and Store New Instance In a Constant
const PUT = Object.freeze(new Put());
