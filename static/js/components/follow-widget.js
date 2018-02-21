/* --- Comment Like --- */


ko.components.register('follow-widget', {
    viewModel: function(params) {
      var self = this; console.log(params);

      self.you_id = ko.observable(params.root.you().id);
      self.signed_in = ko.observable(params.root.signed_in());

      self.account_id = ko.observable(params.account_id);

      self.following = ko.observable(false);

      console.log(self)

      self.check_account_follow = function() {
        GET.check_account_follow(self.account_id())
        .then(function(resp) {
          // console.log(resp);
          self.following(resp.following);
        })
        .catch(function(error){
          console.log(error);
        })
      }
      self.check_account_follow();

      self.toggle_follow = function() {
        if(self.signed_in() === false) { return }
        if(self.you_id() === self.account_id()) { return }

        POST.toggle_account_follow(self.account_id())
        .then(function(resp){
          // console.log(resp);
          self.following(resp.following);
        })
        .catch(function(error){
          console.log(error);
        })
      }

    },
    template:
        '<div class="cursor-class">\
            <span class="cursor-class" data-bind="click: toggle_follow, visible: following()"> \
              <i class="fas fa-star"></i> \
            </span> \
            <span class="cursor-class" data-bind="click: toggle_follow, visible: !following()"> \
              <i class="far fa-star"></i> \
            </span> \
            <span data-bind="text: following() === true ? \'Following\' : \'Follow\'"></span> \
        </div>'
});
