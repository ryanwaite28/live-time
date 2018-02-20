'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    self.title = ko.observable('');
    self.desc = ko.observable('');
    self.categories = ko.observable('');
    self.location = ko.observable('');
    self.link = ko.observable('');

    //

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
    });

    //

    self.create_event = function() {
      var title = self.title().trim();
      var desc = self.desc().trim();
      var categories = self.categories().trim();
      var location = self.location().trim();
      var link = self.link().trim();

      /* --- */

      if(title.length > 125 || title.length < 10) {
        alert('Title must be between 10 and 125 characters');
        return;
      }
      if(desc.length > 250 || desc.length < 10) {
        alert('Description must be between 10 and 250 characters');
        return;
      }
      if(categories.length > 250 || categories.length < 10) {
        alert('Categories must be between 10 and 250 characters');
        return;
      }
      if(location.length > 250 || location.length < 10) {
        alert('Location must be between 10 and 250 characters');
        return;
      }
      if(link) {
        if(!validateLink(link)) {
          alert('Link input is in bad format');
          return;
        }
      }

      var hours = parseInt($('#event_hours_input').val());
      if(!hours || hours === NaN || !/^[0-9]{2}$/.test(String(hours)) || hours < 0 || hours > 23) {
        alert('Hours input is in bad format');
        return;
      }
      var minutes = parseInt($('#event_minutes_input').val());
      if(!minutes || minutes === NaN || !/^[0-9]{2}$/.test(String(minutes)) || minutes < 0 || minutes > 59) {
        alert('Minutes input is in bad format');
        return;
      }
      if(!$('#event_date_input').val()) {
        alert('Please select a date');
        return;
      }
      var today = new Date();
      var event_date_input = $('#event_date_input').val();
      var date_concat = event_date_input + ' ' + hours + ':' + minutes + ':' + '00';
      var event_date = new Date(date_concat);
      console.log(today, ' --- ', event_date);
      if(today >= event_date) {
        alert('Event date cannot be the same as/before today\'s date');
        return;
      }

      var file = get_image_file('event-icon-input');

      /* --- */

      var ask = confirm("Are Edits Correct?");
      if(ask === false) { return; }

      var data = {
        title: title,
        desc: desc,
        categories: categories,
        location: location,
        link: link,
        date_concat: date_concat,
        event_date: event_date,
        file: file
      }

      disable_buttons();

      POST.create_event(data)
      .then(function(resp){
        console.log(resp);
        enable_buttons();
        alert(resp.message);
        if(resp.error) {
          return;
        }
        self.title('')
        self.desc('')
        self.categories('')
        self.location('')
        self.link('')
        $('#event_date_input').val('');
        $('#event_hours_input').val('');
        $('#event_minutes_input').val('');
        $('#event-icon-input').val('');
        $('#event-icon-input-text').val('');
      })
      .catch(function(error){
        console.log(error);
      })

    }

  }

  ko.applyBindings(new mvc());
})()
