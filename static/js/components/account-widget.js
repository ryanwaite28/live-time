/* --- Account --- */

ko.components.register('account-widget', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.parent.you_id());
      self.signed_in = ko.observable(params.parent.signed_in());

      self.account = ko.observable(params.account || {});

    },
    template: { fromUrl: 'account-markup.html', maxCacheAge: 1234 }
});
