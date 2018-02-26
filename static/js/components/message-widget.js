/* --- Account --- */

ko.components.register('message-widget', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.root.you().id);
      self.signed_in = ko.observable(params.root.signed_in());

      self.account_id = ko.observable(params.account_id());

      self.message_input = ko.observable('');
      self.showing = ko.observable(false);

      console.log(params);
      console.log(self);

      self.show_form = function() {
        self.showing( !self.showing() );
      }

      self.send_message = function() {
        if(self.signed_in() === false) { return }
        if(self.you_id() === self.account_id()) { return }
        if(self.message_input().trim().length < 2) { alert('messages must be at least 2 characters.'); return }

        POST.send_account_message(self.account_id(), self.message_input())
        .then(function(resp){
          if(resp.error) {
            console.log(resp);
            return
          }

          self.showing(false);
          self.message_input('');
          Materialize.toast('Message Sent!', 2000)
        })
      }

    },
    template: { fromUrl: 'message-widget-markup.html', maxCacheAge: 1234 }
});
