/* --- Booking Widget --- */

/*
  This Widget is for checking the status of a booking request for an event
  between an ARTIST and The event's VENUE.
*/

ko.components.register('booking-artist-venue-widget', {
    viewModel: function(params) {
      var self = this;

      // you and the account

      self.you = ko.observable(params.root.you());
      self.signed_in = ko.observable(params.root.signed_in());

      var account = params.account.constructor === Function ? params.account() : params.account;
      self.account = ko.observable(account);

      // the event id

      var event_id = params.event_id.constructor === Function ? params.event_id() : params.event_id;
      self.event_id = ko.observable(event_id);

      // the booking status

      self.booking_request_exists = ko.observable(false);

      self.sender = ko.observable(null);
      self.receiver = ko.observable(null);

      // check if a request already exists

      GET.check_booking_request(event_id, account.id)
      .then(function(resp){
        console.log(resp);
        if(resp.error) {
          return;
        }
      })
      .catch(function(error){
        console.log(error);
      });

      //



    },
    template: { fromUrl: 'booking-artist-venue-widget-markup.html', maxCacheAge: 1234 }
});)
