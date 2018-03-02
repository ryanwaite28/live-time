'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.background_view = ko.observable(false);

    self.event = ko.observable({});

    self.eventsList = ko.observableArray([]);
    self.eventsIDs = ko.observableArray([]);
    self.eventsObj = {};

    self.search_msg = ko.observable('');
    self.search_query = ko.observable('');
    self.search_type = ko.observable('');
    self.artistsList = ko.observableArray([]);

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

    self.set_query_type = function(type) {
      self.search_type(type);
    }

    self.search_artists = function(data, event) {
      if(self.signed_in() === false) { return; }
      var query = self.search_query().toLowerCase().trim();
      if(!query) { self.artistsList([]); self.search_msg(''); return; }

      GET.search_artists(self.search_type(), query)
      .then(function(resp) {
        // console.log(resp);

        var performer_ids = [];
        self.event().performers.forEach(function(p){
          performer_ids.push(p.performer_id);
        });

        var filtered = resp.artists.filter(function(a){
          return performer_ids.indexOf(a.id) === -1
        });

        self.artistsList(filtered);
        var msg = filtered.length + ' result(s)';
        self.search_msg(msg);
      })
      .catch(function(error){
        console.log(error);
      });
    }

    self.get_event = function() {
      var splitter = location.href.split('/');
      var event_id = splitter[splitter.length - 1];

      GET.get_event_by_id(event_id)
      .then(function(resp){
        // console.log(resp);
        self.event(resp.event);
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

    self.remove_performer = function(performer_id) {
      var new_event = self.event();
      new_event.performers = new_event.performers.filter(function(p){ return p.performer_id !=  performer_id});
      self.eventsList.replace(self.event(), new_event);
    }.bind(self)

  }

  ko.applyBindings(new mvc());
})()
