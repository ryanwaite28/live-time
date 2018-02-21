/* --- Account --- */

ko.components.register('account-widget', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.root.you().id);
      self.signed_in = ko.observable(params.root.signed_in());

      self.account = ko.observable(params.account || {});

      // console.log(params);
      // console.log(self);

    },
    template: { fromUrl: 'account-markup.html', maxCacheAge: 1234 }
});
