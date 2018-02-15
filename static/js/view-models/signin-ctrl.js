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
      if(resp.user) { self.you(resp.user) }
    });

    //

    self.sign_in = function() {

    }

  }

  ko.applyBindings(new mvc());
})()
