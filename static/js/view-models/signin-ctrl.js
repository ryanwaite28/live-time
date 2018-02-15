'use strict';

(function(){

  function mvc() {
    var self = this;
    // window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.email_input = ko.observable('');
    self.password_input = ko.observable('');

    //

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) { self.you(resp.account) }
    });

    //

    self.sign_in = function() {
      var email_input = self.email_input().trim().toLowerCase();
      var password_input = self.password_input();

      if(!validateEmail(email_input)) {
        alert('account email is in bad format.');
        return;
      }
      if(!validatePassword(password_input)) {
        alert('passwords must be: \n\n \
        letters and/or numbers (dashes, periods, underscores, special characters are allowed)\n \
        minimum of 7 characters.');
        return;
      }

      var data = {
        email: email_input,
        password: password_input
      }

      disable_buttons()

      PUT.signin(data)
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
