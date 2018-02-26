/* --- event Likes --- */

ko.components.register('event-like-widget', {
    viewModel: function(params) {
      var self = this;
      // console.log(params);

      self.event = params.event();
      self.event_id = params.event_id();
      self.event_likes = params.event_likes();
      self.you_id = ko.observable(params.you_id());
      self.signed_in = ko.observable(params.signed_in());

      self.likesLength = ko.observable(self.event_likes);
      self.liked = ko.observable(false);

      self.check_event_like = function() {
        GET.check_event_account_like(self.event_id, self.you_id())
        .then(function(resp) {
          // if(resp.message) { alert(resp.message); }
          if(resp.error) {
            console.log(resp);
            return;
          }

          self.liked(resp.liked);
        })
        .catch(function(error){
          console.log(error);
        })
      }.bind(self);

      if(self.signed_in() === true) {
        self.check_event_like();
      }

      self.toggle_like = function() {
        if(self.signed_in() === false) { return }

        POST.toggle_event_like(self.event_id)
        .then(function(resp){
          // if(resp.message) { alert(resp.message); }
          if(resp.error) {
            console.log(resp);
            return;
          }

          self.liked(resp.liked);

          if(resp.liked == true) {
            self.event_likes++;
          }
          else {
            self.event_likes--;
          }

          self.likesLength(self.event_likes);
        })
        .catch(function(error){
          console.log(error);
        })
      }.bind(self);

    },
    template:
        '<div class="">\
            <span data-bind="click: toggle_like, if: liked()"> \
              <i class="fas fa-heart"></i> \
            </span> \
            <span data-bind="click: toggle_like, if: !liked()"> \
              <i class="far fa-heart"></i> \
            </span> \
            <span data-bind="text: likesLength"></span> | Likes \
        </div>'
});
