'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.background_view = ko.observable(false);

    self.eventsList = ko.observableArray([]);
    self.eventsIDs = ko.observableArray([]);
    self.eventsObj = {};

    self.min_event_id = 0;
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
      var event_id = splitter[splitter.length - 1];

      GET.get_event_by_id(event_id)
      .then(function(resp){
        console.log(resp);
        self.eventsList.push(resp.event);
        self.eventsIDs.push(resp.event.id);
        self.eventsObj[resp.event.unique_value] = resp.event;
      });
    }

    self.delete_event = function(event_id) {
      self.eventsList.remove(function(event){
        return event.id == event_id;
      });
      window.location.href = '/';
    }

  }

  ko.applyBindings(new mvc());
})()
