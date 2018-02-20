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

}

// Create and Store New Instance In a Constant
const POST = Object.freeze(new Post());
