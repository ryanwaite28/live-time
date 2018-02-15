'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.account_type_options = ko.observableArray(["USER", "ARTIST", "VENUE"]);

    self.account_username_input = ko.observable('');
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
      if(resp.account) { self.you(resp.account) }
    });

    //

    self.update_signup_account_type = function(data, event) {
      self.account_type_input(event.target.value);
    }

    self.sign_up = function() {
      var account_username_input = self.account_username_input().trim().toLowerCase();
      var account_email_input = self.account_email_input().trim().toLowerCase();
      var booking_email_input = self.booking_email_input().trim().toLowerCase();
      var account_type_input = self.account_type_input();
      var password_input = self.password_input();
      var verify_password_input = self.verify_password_input();

      if(!validateUsername(account_username_input)) {
        alert('usernames must be: letters and/or numbers (dashes, periods, underscores are allowed); minimum of 3 characters.');
        return;
      }
      if(!validateEmail(account_email_input)) {
        alert('account email is in bad format.');
        return;
      }
      if(!validateEmail(booking_email_input)) {
        alert('booking email is in bad format.');
        return;
      }
      if(!validatePassword(password_input)) {
        alert('passwords must be: \n\n \
        letters and/or numbers (dashes, periods, underscores, special characters are allowed)\n \
        minimum of 7 characters.');
        return;
      }
      if(password_input !== verify_password_input) {
        alert('passwords do not match');
        return;
      }
      if(!account_type_input) {
        alert('Account Type Is Required');
        return;
      }

      var data = {
        username: account_username_input,
        account_email: account_email_input,
        booking_email: booking_email_input,
        account_type: account_type_input,
        password: password_input,
      }

      disable_buttons()

      POST.signup(data)
      .then(function(resp){
        enable_buttons();
        console.log(resp);
        alert(resp.message);
        if(!resp.error) { window.location.href = '/profile' }
      })
      .catch(function(error){
        console.log(error);
      })

    }

  }

  ko.applyBindings(new mvc());
})()
