/* --- Comments List --- */


ko.components.register('comments-list-widget', {
    viewModel: function(params) {
      var self = this;

      self.event_id = params.event_id();
      self.event_comments = params.event_comments();

      self.you_id = ko.observable(params.you_id());
      self.signed_in = ko.observable(params.signed_in());

      self.commentsLength = ko.observable(self.event_comments);
      self.comment_text = ko.observable('');

      self.commentsIDs = ko.observableArray([]);
      self.commentsList = ko.observableArray([]);
      self.min_comment_id = 0;

      self.end = ko.observable(false);
      self.hide_comments = ko.observable(true);

      // console.log(self, params);

      self.get_event_comments = function() {
        GET.get_event_comments(self.event_id, self.min_comment_id)
        .then(function(resp){
          // console.log(resp);
          if(resp.event_comments.length < 5) {
            self.end(true);
            // return;
          }

          resp.event_comments.forEach(function(comment){
            self.commentsIDs.push(comment.id);
            self.commentsList.push(comment);
          });

          self.min_comment_id = self.commentsIDs().length > 0 ?
          Math.min(...self.commentsIDs()) : 0;
        })
        .catch(function(error){
          console.log(error);
        })
      }.bind(self);
      self.get_event_comments();

      self.submitComment = function() {
        if(self.comment_text() === '') {
          return;
        }

        POST.create_event_comment(self.event_id, self.comment_text())
        .then(function(resp){
          // console.log(resp);
          if(resp.error) {
            alert(resp.message);
            return;
          }

          self.comment_text('');
          self.commentsIDs.unshift(resp.comment.id);
          self.commentsList.unshift(resp.comment);
          self.commentsLength(self.commentsLength() + 1);

          self.min_comment_id = self.commentsIDs().length > 0 ?
          Math.min(...self.commentsIDs()) : 0;
        })
        .catch(function(error){
          console.log(error);
        })
      }

      self.keyListener = function(data, event) {
        if(event.keyCode === 13) {
          self.submitComment();
        }
      }

      self.toggle_comments_view = function() {
        self.hide_comments( !self.hide_comments() );
      }

      self.delete_comment = function(comment_id) {
        self.commentsList.remove(function(comment){
          return comment.id == comment_id;
        });
        self.commentsLength(self.commentsLength() - 1);
      }

    },
    template:
        '<div class="">\
            <span data-bind="visible: commentsLength() > 0"> \
              <i class="fas fa-comment"></i> \
            </span> \
            <span data-bind="visible: commentsLength() == 0"> \
              <i class="far fa-comment"></i> \
            </span> \
            <span data-bind="text: commentsLength"></span> | <span class="info-text cursor-class" data-bind="click: toggle_comments_view">hide/show comments</span> \
            <br/> \
            <div data-bind="visible: hide_comments() === false"> \
              <br/> \
              <div data-bind="visible: signed_in() === true"> \
                <div class="row"> \
                  <div class="input-field col s12"> \
                    <input placeholder="Write a comment" data-bind="textInput: comment_text, event: { keyup: keyListener }" > \
                  </div> \
                </div> \
              </div> \
              <div data-bind="foreach: commentsList"> \
                <comment-widget params="parent: $parent, comment: $data, you_id: $parent.you_id(), signed_in: $parent.signed_in()"></comment-widget>\
              </div> \
              <br/> \
              <div data-bind="visible: end() == false"> \
                <p><a data-bind="click: get_event_comments">Load more comments</a></p>\
              </div> \
            </div> \
        </div>'
});
