/* --- Event --- */

ko.components.register('event-view-widget', {
    viewModel: function(params) {
      var self = this;

      self.you = ko.observable(params.parent.you());
      self.you_id = ko.observable(params.parent.you().id);
      self.signed_in = ko.observable(params.parent.signed_in());

      self.root = ko.observable(params.root);

      var event = params.event.constructor === Function ? params.event() : params.event;
      self.event = ko.observable(event);
      self.event_id = ko.observable(event.id);

      self.hide_performers = ko.observable(true);

      // console.log(params, self);

      self.toggle_performers_view = function() {
        self.hide_performers( !self.hide_performers() );
      }

    },
    template: { fromUrl: 'event-view-markup.html', maxCacheAge: 1234 }
});
