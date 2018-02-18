'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }
    self.account_type_options = ko.observableArray(["USER", "ARTIST", "VENUE"]);

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.bio = ko.observable('');
    self.categories = ko.observable('');
    self.type = ko.observable('');
    self.displayname = ko.observable('');
    self.link = ko.observable('');
    self.location = ko.observable('');
    self.phone = ko.observable('');
    self.eventbrite = ko.observable('');

    self.icon = ko.observable('');

    self.background = ko.observable('');

    self.username = ko.observable('');

    self.email = ko.observable('');

    self.booking_email = ko.observable('');

    self.bandcamp = ko.observable('');
    self.datpiff = ko.observable('');
    self.facebook = ko.observable('');
    self.google_plus = ko.observable('');
    self.instagram = ko.observable('');
    self.itunes = ko.observable('');
    self.google_play = ko.observable('');
    self.last_fm = ko.observable('');
    self.pandora = ko.observable('');
    self.snapchat = ko.observable('');
    self.soundcloud = ko.observable('');
    self.spinrilla = ko.observable('');
    self.spotify = ko.observable('');
    self.tidal = ko.observable('');
    self.twitter = ko.observable('');
    self.youtube = ko.observable('');

    self.password_input = ko.observable('');
    self.verify_password_input = ko.observable('');

    //

    GET.check_session()
    .then(function(resp){
      console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
        Object.keys(resp.account).forEach(function(key){
          if(self[key]) {
            self[key](resp.account[key]);
          }
        });
      }
    });

    //

    self.update_account_type = function(data, event) {
      self.type(event.target.value);
    }

    /* --- */

    self.update_info = function() {
      if(self.bio().trim().length > 250) {
        alert('Bio is over the max length: 250 characters.');
        return;
      }
      if(self.displayname().trim().length > 50) {
        alert('Displayname is over the max length: 50 characters.');
        return;
      }
      if(self.categories().trim().length > 250) {
        alert('Categories is over the max length: 250 characters.');
        return;
      }
      if(self.location().trim().length > 150) {
        alert('Location is over the max length: 250 characters.');
        return;
      }

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      var data = {
        bio: self.bio().trim(),
        displayname: self.displayname().trim(),
        categories: self.categories().trim(),
        location: self.location().trim(),
        type: self.type().trim(),
        phone: self.phone().trim(),
        link: self.link().trim(),
        eventbrite: self.eventbrite().trim()
      }

      disable_buttons();

      PUT.update_info(data)
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_icon = function() {
      var file = get_image_file('icon-input');
      if(file === null) {
        alert("File must be an image: jpg, png, or gif");
        return;
      }

      disable_buttons();

      PUT.update_icon(file, getFileName(self.you().icon))
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.icon(resp.icon);
        $('#icon-input').val('');
        $('#icon-input-text').val('');
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_background = function() {
      var file = get_image_file('background-input');
      if(file === null) {
        alert("File must be an image: jpg, png, or gif");
        return;
      }

      disable_buttons();

      PUT.update_background(file, getFileName(self.you().background))
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.background(resp.background);
        $('#background-input').val('');
        $('#background-input-text').val('');
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_social = function() {
      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      var data = {
        facebook: self.facebook().trim(),
        twitter: self.twitter().trim(),
        youtube: self.youtube().trim(),
        instagram: self.instagram().trim(),
        soundcloud: self.soundcloud().trim(),
        snapchat: self.snapchat().trim(),
        itunes: self.itunes().trim(),
        google_play: self.google_play().trim(),
        last_fm: self.last_fm().trim(),
        spotify: self.spotify().trim(),
        google_plus: self.google_plus().trim(),
        tidal: self.tidal().trim(),
        pandora: self.pandora().trim(),
        last_fm: self.last_fm().trim(),
        spinrilla: self.spinrilla().trim(),
        bandcamp: self.bandcamp().trim(),
      }

      disable_buttons();

      PUT.update_social(data)
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_username = function() {
      if(self.you().username === self.username()) {
        return;
      }
      if(!validateUsername(self.username())) {
        alert('usernames must be: letters and/or numbers (dashes, periods, underscores are allowed); minimum of 3 characters.');
        return;
      }

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      disable_buttons();

      PUT.update_username(self.username())
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_account_email = function() {
      if(self.you().email === self.email()) {
        return;
      }
      if(!validateEmail(self.email())) {
        alert('account email is in bad format.');
        return;
      }

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      disable_buttons();

      PUT.update_account_email(self.email())
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_booking_email = function() {
      if(self.you().booking_email === self.booking_email()) {
        return;
      }
      if(!validateEmail(self.booking_email())) {
        alert('booking email is in bad format.');
        return;
      }

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      disable_buttons();

      PUT.update_booking_email(self.booking_email())
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.update_password = function() {
      if(!validatePassword(self.password_input())) {
        alert('passwords must be: \n\n \
        letters and/or numbers (dashes, periods, underscores, special characters are allowed)\n \
        minimum of 7 characters, no spaces.');
        return;
      }
      if(self.password_input() !== self.verify_password_input()) {
        alert('passwords do not match');
        return;
      }

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      disable_buttons();

      PUT.update_password(self.password_input())
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.password_input('');
        self.verify_password_input('');
        self.you(resp.account);
      })
      .catch(function(error){
        console.log(error);
      })
    }

  }

  ko.applyBindings(new mvc());
})()
