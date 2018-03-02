'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.event = ko.observable({});
    self.eventsList = ko.observableArray([]);

    self.attendingList = ko.observableArray([]);
    self.attendingIDs = ko.observableArray([]);

    self.min_attend_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_event();
    });

    //

    self.get_event = function() {
      var splitter = location.href.split('/');
      var event_id = splitter[splitter.length - 2];

      GET.get_event_by_id(event_id)
      .then(function(resp){
        // console.log(resp);
        self.event(resp.event);
        self.eventsList.push(resp.event);

        self.get_event_attending();
      });
    }

    self.get_event_attending = function() {
      var splitter = location.href.split('/');
      var event_id = splitter[splitter.length - 2];
      disable_buttons();

      GET.get_event_attending(event_id, self.min_attend_id)
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
        });

        self.min_attend_id = self.attendingIDs().length > 0 ?
        Math.min(...self.attendingIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

  }

  ko.applyBindings(new mvc());
})()
