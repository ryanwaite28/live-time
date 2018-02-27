'use strict';

const Get = function() {
  var self = this;

  // self.welcome_event = function() {
  //   fetch('/welcome_event', {method: "GET", credentials: "include"})
  //   .then(function(resp){ return resp.json(); })
  //   .then(function(resp){ /* console.log(resp); */ })
  //   .catch(function(error){
  //     return reject(error);
  //   });
  // }

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

  self.get_account_by_username = function(username) {
    return new Promise(function(resolve, reject){
      fetch('/get/account/' + username, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.get_event_by_id = function(event_id) {
    return new Promise(function(resolve, reject){
      fetch('/get/event/' + event_id, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json(); })
      .then(function(resp){ return resolve(resp); })
      .catch(function(error){
        return reject(error);
      });
    });
  }

  self.get_venue_events = function(account_id = 0, event_id = 0) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/venue/' + account_id + '/events/' + event_id, params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_artist_shows = function(account_id = 0, event_performer_id = 0) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/artist/' + account_id + '/shows/' + event_performer_id, params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_user_attending = function(account_id = 0, attend_id = 0) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/user/' + account_id + '/attending/' + attend_id, params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_account_notifications = function(notification_id = 0) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/account/notifications/' + notification_id, params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_account_conversations = function() {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/account/conversations', params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_conversation_messages = function(c_id, cm_id) {
    return new Promise(function(resolve, reject){
      var params = {
        method: "GET",
        credentials: "include",
        header: headers_json()
      }

      fetch('/conversation/' + c_id + '/messages/' + cm_id, params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_random_events = function() {
    return new Promise(function(resolve, reject){
      fetch('/get/random/events', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_random_venues = function() {
    return new Promise(function(resolve, reject){
      fetch('/get/random/venues', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_random_artists = function() {
    return new Promise(function(resolve, reject){
      fetch('/get/random/artists', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_random_users = function() {
    return new Promise(function(resolve, reject){
      fetch('/get/random/users', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.check_event_account_like = function(event_id, account_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/account_like/' + account_id, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.check_comment_account_like = function(comment_id, account_id) {
    return new Promise(function(resolve, reject){
      fetch('/comment/' + comment_id + '/account_like/' + account_id, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.check_account_follow = function(account_id) {
    return new Promise(function(resolve, reject){
      fetch('/accounts/' + account_id + '/following', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.check_event_attending = function(event_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/attending', {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.check_booking_request = function(event_id, account_id) {
    return new Promise(function(resolve, reject){
      fetch('/events/' + event_id + '/check_booking/' + account_id, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.get_event_comments = function(event_id, comment_id) {
    return new Promise(function(resolve, reject){
      fetch('/event/' + event_id + '/comments/' + comment_id, {method: "GET", credentials: "include"})
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.search_events = function(type, query) {
    return new Promise(function(resolve, reject) {
      var params = {
        method: "GET",
        credentials: "include"
      }

      fetch('/search/events/' + type + '/' + query.replace(/\s/gi,'_space_'), params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.search_venues = function(type, query) {
    return new Promise(function(resolve, reject) {
      var params = {
        method: "GET",
        credentials: "include"
      }

      fetch('/search/venues/' + type + '/' + query.replace(/\s/gi,'_space_'), params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.search_artists = function(type, query) {
    return new Promise(function(resolve, reject) {
      var params = {
        method: "GET",
        credentials: "include"
      }

      fetch('/search/artists/' + type + '/' + query.replace(/\s/gi,'_space_'), params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

  self.search_users = function(type, query) {
    return new Promise(function(resolve, reject) {
      var params = {
        method: "GET",
        credentials: "include"
      }

      fetch('/search/users/' + type + '/' + query.replace(/\s/gi,'_space_'), params)
      .then(function(resp){ return resp.json() })
      .then(function(json){ return resolve(json); })
      .catch(function(error){ return reject(error) })
    });
  }

}

// Create and Store New Instance In a Constant
const GET = Object.freeze(new Get());
