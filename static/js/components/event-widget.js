/* --- Event --- */

ko.components.register('event-widget', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.parent.you().id);
      self.signed_in = ko.observable(params.parent.signed_in());

      self.root = ko.observable(params.root);

      self.event = ko.observable(params.event || {});

      self.event_id = ko.observable(params.event.id);
      self.event_likes = ko.observable(params.event.likes);
      self.event_comments = ko.observable(params.event.comments);

      self.commentsLength = ko.observable(params.event.comments);
      self.performers = ko.observableArray(params.event.performers);
      self.attending = ko.observableArray(params.event.attending);

      self.hide_performers = ko.observable(true);

      // console.log(params, self);

      self.toggle_performers_view = function() {
        self.hide_performers( !self.hide_performers() );
      }

      self.edit_event = function(event) {

      }

      self.delete_event = function() {
        var ask = confirm('Are you sure that you want to delete this event?');
        if(ask === false) { return; }

        DELETE.delete_event(self.event().id)
        .then(function(resp) {
          // console.log(resp);
          if(resp.error) {
            alert(resp.message);
            return;
          }

          params.parent.delete_event(self.event().id);
        })
        .catch(function(error){
          console.log(error);
        })


      }

    },
    template: { fromUrl: 'event-markup.html', maxCacheAge: 1234 }
});
