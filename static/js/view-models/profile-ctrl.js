'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.background_view = ko.observable(false);

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
    setTimeout(function(){ Materialize.toast('Welcome!', 4000) }, 1000);

    //

    self.toggle_background_view = function() {
      self.background_view( !self.background_view() )
    }

  }

  ko.applyBindings(new mvc());
})()
