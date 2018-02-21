'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});
    self.user = ko.observable({});
    self.userFollowing = ko.observable(0);
    self.userFollowers = ko.observable(0);

    self.user_loaded = ko.observable(false);

    //

    self.background_view = ko.observable(false);
    self.following = ko.observable(false);

    self.eventsList = ko.observableArray([]);
    self.eventsIDs = ko.observableArray([]);
    self.eventsObj = {};

    self.min_event_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_account_by_username();
    });

    self.get_account_by_username = function() {
      var splitter = location.href.split('/');
      var username = splitter[splitter.length - 2];

      GET.get_account_by_username(username)
      .then(function(resp){
        console.log(resp);
        if(resp.account) {
          self.user(resp.account);
          self.userFollowing(resp.account.following);
          self.userFollowers(resp.account.followers);
          self.user_loaded(true);
          self.check_account_follow();
        }
        self.get_user_events();
      });
    }

    //

    self.check_account_follow = function() {
      GET.check_account_follow(self.user().id)
      .then(function(resp) {
        console.log(resp);
        self.following(resp.following);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.toggle_follow = function() {
      if(self.signed_in() === false) { return }

      POST.toggle_account_follow(self.user().id)
      .then(function(resp){
        // console.log(resp);
        self.following(resp.following);

        if(self.following() === true) {
          self.userFollowers( self.userFollowers() + 1 );
        }
        else {
          self.userFollowers( self.userFollowers() - 1 );
        }
      })
      .catch(function(error){
        console.log(error);
      })
    }

    //

    self.toggle_background_view = function() {
      self.background_view( !self.background_view() )
    }

    self.get_user_events = function() {
      disable_buttons();

      GET.get_venue_events(self.user().id, self.min_event_id)
      .then(function(resp){
        console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.events.length < 5) {
          self.end(true);
        }

        resp.events.forEach(function(event){
          self.eventsList.push(event);
          self.eventsIDs.push(event.id);
          self.eventsObj[event.unique_value] = event;
        });

        self.min_event_id = self.eventsIDs().length > 0 ?
        Math.min(...self.eventsIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.delete_event = function(event_id) {
      self.eventsList.remove(function(event){
        return event.id == event_id;
      });
    }

  }

  ko.applyBindings(new mvc());
})()
