(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.account_type_options = ko.observableArray(["USER", "ARTIST", "VENUE"]);

    self.account_email_input = ko.observable('');
    self.booking_email_input = ko.observable('');
    self.account_type_input = ko.observable('USER');
    self.password_input = ko.observable('');
    self.verify_password_input = ko.observable('');

    //

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.user) { self.you(resp.user) }
    });

    //

    self.update_signup_account_type = function(data, event) {
      self.account_type_input(event.target.value);
    }

    self.sign_up = function() {

    }

  }

  ko.applyBindings(new mvc());
})()
