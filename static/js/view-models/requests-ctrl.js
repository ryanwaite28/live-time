'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.requestsList = ko.observableArray([]);
    self.requestsIDs = ko.observableArray([]);
    self.requestsObj = {};

    self.min_request_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_account_requests();
    });

    //

    self.get_account_requests = function() {
      disable_buttons();

      GET.get_account_requests(self.min_request_id)
      .then(function(resp){
        console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.requests.length < 5) {
          self.end(true);
        }

        resp.requests.forEach(function(request){
          self.requestsList.push(request);
          self.requestsIDs.push(request.id);
          self.requestsObj[request.unique_value] = request;
        });

        self.min_request_id = self.requestsIDs().length > 0 ?
        Math.min(...self.requestsIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.accept_request = function(request) {
      // console.log(request);

      var ask = confirm('Accept this request?');
      if(ask === false) { return; }

      POST.accept_booking_request(request.event_id, request.sender_id)
      .then(function(resp){
        console.log(resp);
        if(resp.error) {
          if(resp.booking_request === false) {
            self.requestsList.remove(request);
          }
          Materialize.toast(resp.message, 4000);
          return;
        }

        self.requestsList.remove(request);
        Materialize.toast('Request Accepted!', 4000);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.decline_request = function(request) {
      // console.log(request);

      var ask = confirm('Decline this request?');
      if(ask === false) { return; }

      DELETE.decline_booking_request(request.event_id, request.sender_id)
      .then(function(resp){
        console.log(resp);
        if(resp.error) {
          if(resp.booking_request === false) {
            self.requestsList.remove(request);
          }
          Materialize.toast(resp.message, 4000);
          return;
        }

        self.requestsList.remove(request);
        Materialize.toast('Request Declined.', 4000);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    // Listen for new notes

    var source = new EventSource("/stream");

    source.onopen = function() {
      console.log("Listening for new messages...");
    };

    source.addEventListener('action', function(event) {
      var data = JSON.parse(event.data);
      console.log(data);
      if(data.for_id === self.you().id) {
        Materialize.toast(data.message, 5000);
      }
    }, false);

    source.addEventListener('error', function(event) {
      console.log(event);
    }, false);

  }

  ko.applyBindings(new mvc());
})()
