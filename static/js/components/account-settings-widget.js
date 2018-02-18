ko.components.register('account-settings-widget', {
    viewModel: function(params){
      var self = this;

      // self.signed_in = ko.observable('');

      console.log(params, self);
    },
    template: { fromUrl: 'account-settings-widget.html', maxCacheAge: 1234 }
});
