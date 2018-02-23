'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.background_view = ko.observable(false);

    self.events_search_msg = ko.observable('');
    self.events_search_query = ko.observable('');
    self.events_search_type = ko.observable('');
    self.events_list = ko.observableArray([]);

    self.venues_search_msg = ko.observable('');
    self.venues_search_query = ko.observable('');
    self.venues_search_type = ko.observable('');
    self.venues_list = ko.observableArray([]);

    self.artists_search_msg = ko.observable('');
    self.artists_search_query = ko.observable('');
    self.artists_search_type = ko.observable('');
    self.artists_list = ko.observableArray([]);

    self.users_search_msg = ko.observable('');
    self.users_search_query = ko.observable('');
    self.users_search_type = ko.observable('');
    self.users_list = ko.observableArray([]);

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
    });

    //

    self.set_events_query_type = function(type) {
      self.events_search_type(type);
    }
    self.set_venues_query_type = function(type) {
      self.venues_search_type(type);
    }
    self.set_artists_query_type = function(type) {
      self.artists_search_type(type);
    }
    self.set_users_query_type = function(type) {
      self.users_search_type(type);
    }

    //

    self.search_events = function(data, event) {
      var query = self.events_search_query().toLowerCase().trim();
      if(!query) { self.events_list([]); self.events_search_msg(''); return; }

      GET.search_events(self.events_search_type(), query)
      .then(function(resp) {
        console.log(resp);
        self.events_list(resp.events);
        var msg = resp.events.length + ' results';
        self.events_search_msg(msg);
      })
      .catch(function(error){
        console.log(error);
      });
    }

    self.search_venues = function(data, event) {
      var query = self.venues_search_query().toLowerCase().trim();
      if(!query) { self.venues_list([]); self.venues_search_msg(''); return; }

      GET.search_venues(self.venues_search_type(), query)
      .then(function(resp) {
        console.log(resp);
        self.venues_list(resp.venues);
        var msg = resp.venues.length + ' results';
        self.venues_search_msg(msg);
      })
      .catch(function(error){
        console.log(error);
      });
    }

    self.search_artists = function(data, event) {
      var query = self.artists_search_query().toLowerCase().trim();
      if(!query) { self.artists_list([]); self.artists_search_msg(''); return; }

      GET.search_artists(self.artists_search_type(), query)
      .then(function(resp) {
        console.log(resp);
        self.artists_list(resp.artists);
        var msg = resp.artists.length + ' results';
        self.artists_search_msg(msg);
      })
      .catch(function(error){
        console.log(error);
      });
    }

    self.search_users = function(data, event) {
      var query = self.users_search_query().toLowerCase().trim();
      if(!query) { self.users_list([]); self.users_search_msg(''); return; }

      GET.search_users(self.users_search_type(), query)
      .then(function(resp) {
        console.log(resp);
        self.users_list(resp.users);
        var msg = resp.users.length + ' results';
        self.users_search_msg(msg);
      })
      .catch(function(error){
        console.log(error);
      });
    }

  }

  ko.applyBindings(new mvc());
})()
