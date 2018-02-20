'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});
    self.user = ko.observable({});

    //

    self.background_view = ko.observable(false);

    self.showsList = ko.observableArray([]);
    self.showsIDs = ko.observableArray([]);
    self.showsObj = {};

    self.min_show_id = 0;
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
        }
        self.get_user_shows();
      });
    }

    //

    self.toggle_background_view = function() {
      self.background_view( !self.background_view() )
    }

    self.get_user_shows = function() {
      disable_buttons();

      GET.get_artist_shows(self.user().id, self.min_show_id)
      .then(function(resp){
        console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.shows.length < 5) {
          self.end(true);
        }

        resp.shows.forEach(function(show){
          self.showsList.push(show);
          self.showsIDs.push(show.id);
          self.showsObj[show.unique_value] = show;
        });

        self.min_show_id = self.showsIDs().length > 0 ?
        Math.min(...self.showsIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.delete_event = function(event_id) {
      self.showsList.remove(function(show){
        return show.event_rel.id == event_id;
      });
    }

  }

  ko.applyBindings(new mvc());
})()
