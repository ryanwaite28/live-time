'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.background_view = ko.observable(false);

    self.attendingList = ko.observableArray([]);
    self.attendingIDs = ko.observableArray([]);
    self.attendingObj = {};

    self.min_attending_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_user_attending();
    });

    //

    self.toggle_background_view = function() {
      self.background_view( !self.background_view() )
    }

    self.get_user_attending = function() {
      disable_buttons();

      GET.get_user_attending(self.you().id, self.min_attending_id)
      .then(function(resp){
        console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.attending.length < 5) {
          self.end(true);
        }

        resp.attending.forEach(function(attend){
          self.attendingList.push(attend);
          self.attendingIDs.push(attend.id);
          self.attendingObj[attend.unique_value] = attend;
        });

        self.min_attending_id = self.attendingIDs().length > 0 ?
        Math.min(...self.attendingIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

  }

  ko.applyBindings(new mvc());
})()
