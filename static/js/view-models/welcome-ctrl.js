'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.randomEvents = ko.observableArray([]);
    self.randomVenues = ko.observableArray([]);
    self.randomArtists = ko.observableArray([]);

    //

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
    });

    //

    var random_events_promise = GET.get_random_events();
    var random_venues_promise = GET.get_random_venues();
    var random_artists_promise = GET.get_random_artists();

    Promise.all([ random_events_promise, random_venues_promise, random_artists_promise ])
    .then(function(values){
      console.log(values);
      var events = values[0].events;
      var venues = values[1].venues;
      var artists = values[2].artists;

      self.randomEvents(events);
      self.randomVenues(venues);
      self.randomArtists(artists);
    })
    .catch(function(error){
      console.log(error);
    })

  }

  ko.applyBindings(new mvc());
})()
