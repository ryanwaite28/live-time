'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.notificationsList = ko.observableArray([]);
    self.notificationsIDs = ko.observableArray([]);
    self.notificationsObj = {};

    self.min_notification_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_account_notifications();
    });

    //

    self.get_account_notifications = function() {
      disable_buttons();

      GET.get_account_notifications(self.you().id, self.min_notification_id)
      .then(function(resp){
        console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.notifications.length < 5) {
          self.end(true);
        }

        resp.notifications.forEach(function(notification){
          self.notificationsList.push(notification);
          self.notificationsIDs.push(notification.id);
          self.notificationsObj[notification.unique_value] = notification;
        });

        self.min_notification_id = self.notificationsIDs().length > 0 ?
        Math.min(...self.notificationsIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

  }

  ko.applyBindings(new mvc());
})()
