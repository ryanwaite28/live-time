/* --- Comment Like --- */


ko.components.register('comment-likes-widget', {
    viewModel: function(params) {
      var self = this;

      self.comment_id = params.comment_id();
      self.comment_likes = params.comment_likes();
      self.you_id = ko.observable(params.you_id());
      self.signed_in = ko.observable(params.signed_in());

      self.likesLength = ko.observable(self.comment_likes);
      self.liked = ko.observable(false);

      // console.log(params, self)

      self.check_comment_like = function() {
        GET.check_comment_account_like(self.comment_id, self.you_id())
        .then(function(resp) {
          // console.log(resp);
          self.liked(resp.liked);
          // console.log(self);
        })
        .catch(function(error){
          console.log(error);
        })
      }.bind(self);
      self.check_comment_like();

      self.toggle_like = function() {
        if(self.signed_in() === false) { return }

        POST.toggle_comment_like(self.comment_id)
        .then(function(resp){
          // console.log(resp);
          self.liked(resp.liked);

          if(resp.liked == true) {
            self.comment_likes++;
          }
          else {
            self.comment_likes--;
          }

          self.likesLength(self.comment_likes);
        })
        .catch(function(error){
          console.log(error);
        })
      }.bind(self);

    },
    template:
        '<div class="">\
            <span class="cursor-class" data-bind="click: toggle_like, visible: liked()"> \
              <i class="fas fa-heart"></i> \
            </span> \
            <span class="cursor-class" data-bind="click: toggle_like, visible: !liked()"> \
              <i class="far fa-heart"></i> \
            </span> \
            <span data-bind="text: likesLength"></span>\
        </div>'
});
