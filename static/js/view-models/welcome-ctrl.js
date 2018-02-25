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

    self.check_session = function() {
      GET.check_session()
      .then(function(resp){
        console.log(resp);
        self.signed_in(resp.online);
        if(resp.account) {
          self.you(resp.account);
        }
      });
    }
    self.check_session();
    setTimeout(function(){ Materialize.toast('Welcome To Live Time!', 4000) }, 1000);

    //

    self.get_random_data = function() {
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
    self.get_random_data();

  }

  ko.applyBindings(new mvc());
})()
