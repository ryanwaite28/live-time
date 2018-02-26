/* --- Account --- */

ko.components.register('account-widget-two', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.root.you().id);
      self.signed_in = ko.observable(params.root.signed_in());

      var account = params.account.constructor === Function ? params.account() : params.account;
      self.account = ko.observable(account || {});

      var enableLink = params.enableLink == undefined ? true : params.enableLink;
      self.enableLink = ko.observable(enableLink);

      // console.log(params);
      // console.log(self);

    },
    template: { fromUrl: 'account-markup-two.html', maxCacheAge: 1234 }
});
