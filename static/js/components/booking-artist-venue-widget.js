/* --- Booking Widget --- */

/*
  This Widget is for checking the status of a booking request for an event
  between an ARTIST and The event's VENUE.
*/

ko.components.register('booking-artist-venue-widget', {
    viewModel: function(params) {
      var self = this;

      // you

      var you = params.root.you();
      self.you = ko.observable(you);
      self.you_id = ko.observable(you.id);
      self.signed_in = ko.observable(params.root.signed_in());


      // the event and event_id

      var event = params.event.constructor === Function ? params.event() : params.event;
      self.event = ko.observable(event);
      self.event_id = ko.observable(event.id);


      // account

      // if you.type === "VENUE", params.account should be undefined
      // and have the type "ARTIST"; pass it to self.account()

      // if you.type === "ARTIST", params.account should NOT be defined
      // and defaults var account to event.host_rel, which is of type "VENUE"

      var account;
      if(params.account) {
        account = params.account.constructor === Function ? params.account() : params.account;
      }
      else {
        account = event.host_rel;
      }

      self.account = ko.observable(account);
      self.account_id = ko.observable(account.id);


      // the booking status

      self.booked = ko.observable(false);
      self.booking = ko.observable(false);
      self.booked_status_text = ko.observable('');
      self.booked_status_css = ko.observable('');

      self.booking_request = ko.observable(false);
      self.booking_request_exists = ko.observable(false);

      self.sender = ko.observable(null);
      self.receiver = ko.observable(null);

      // console.log(params);
      // console.log("booking component: ", params, self);

      // set status text and css

      self.set_text_css = function() {
        var text = self.booked() ? 'Booked!' : 'Not Booked';
        self.booked_status_text(text);

        var css = self.booked() ? 'text-color-green' : 'text-color-red';
        self.booked_status_css(css);
      }


      // check if booking/request already exists

      self.check_booking = function() {
        var account_id = you.type === "ARTIST" ? you.id : account.id;
        GET.check_booking(event.id, account_id)
        .then(function(resp){
          // console.log(resp);
          if(resp.error) {
            return;
          }

          if(resp.booked) {
            self.booked(resp.booked);
            self.booking(resp.booking);
          }
          else {
            self.check_booking_request();
          }

          self.set_text_css();
        })
        .catch(function(error){
          console.log(error);
        });
      }

      self.check_booking_request = function() {
        GET.check_booking_request(event.id, account.id)
        .then(function(resp){
          // console.log(resp);
          if(resp.error) {
            return;
          }

          self.booking_request_exists(resp.booking_request_exists);

          if(resp.booking_request_exists && resp.booking_request) {
            self.booking_request(resp.booking_request);
            self.sender(resp.booking_request.sender_rel);
            self.receiver(resp.booking_request.receiver_rel);
          }

          self.set_text_css();
        })
        .catch(function(error){
          console.log(error);
        });
      }

      var compare_types = booking_widget_compare_types(you.type, account.type);
      if(compare_types === true) {
        self.check_booking();
      }

      // send/cancel booking request functions

      self.send_booking_request = function() {
        if(self.booking_request() === true) {
          // console.log('booking request already exists');
          return;
        }

        POST.send_booking_request(event.id, account.id)
        .then(function(resp){
          console.log(resp);
          if(resp.error) {
            if(resp.booking_request_exists) {
              self.booking_request_exists(resp.booking_request_exists);
              self.booking_request(resp.booking_request);
              self.sender(resp.booking_request.sender_rel);
              self.receiver(resp.booking_request.receiver_rel);
            }
            if(resp.booked) {
              self.booked(resp.booked);
              self.booking(resp.booking);
            }

            Materialize.toast(resp.message, 3000);
            self.set_text_css();
            return;
          }

          self.booking_request_exists(resp.booking_request_exists);
          self.booking_request(resp.new_booking_request);
          self.sender(resp.new_booking_request.sender_rel);
          self.receiver(resp.new_booking_request.receiver_rel);

          Materialize.toast('Request Sent!', 3000);
          self.set_text_css();
        })
        .catch(function(error){
          console.log(error);
        });
      }

      self.cancel_booking_request = function() {
        if(self.booking_request() === false) {
          console.log('no booking request exists');
          return;
        }

        DELETE.cancel_booking_request(event.id, account.id)
        .then(function(resp){
          console.log(resp);
          if(resp.error) {
            self.booking_request_exists(resp.booking_request_exists);
            self.booking_request(false);
            self.sender(false);
            self.receiver(false);

            Materialize.toast(resp.message, 3000);
            self.set_text_css();
            return;
          }

          self.booking_request(false);
          self.booking_request_exists(false);
          self.sender(false);
          self.receiver(false);

          Materialize.toast('Request Canceled.', 3000);
          self.set_text_css();
        })
        .catch(function(error){
          console.log(error);
        });
      }

      // cancel booking

      self.cancel_booking = function() {
        if(self.booked() === false) {
          console.log('booking does not exists');
          return;
        }

        var ask = confirm('Are you sure that you want to cancel this booking?');
        if(ask === false) { return; }

        DELETE.cancel_booking(self.booking().id, account.id)
        .then(function(resp){
          console.log(resp);
          if(resp.error) {
            return;
          }

          var performer_id = self.booking().performer_id;

          self.booked(false);
          self.booking(false)
          self.booking_request(false);
          self.booking_request_exists(false);
          self.sender(false);
          self.receiver(false);
          Materialize.toast('Booking Canceled.', 3000);

          self.set_text_css();

          if(params.remove_performer) {
            params.remove_performer(performer_id);
          }
          if(params.root.remove_performer) {
            params.root.remove_performer(performer_id);
          }
        })
        .catch(function(error){
          console.log(error);
        });
      }

    },
    template: { fromUrl: 'booking-artist-venue-widget-markup.html', maxCacheAge: 1234 }
})
