/* --- Comment --- */


ko.components.register('comment-widget', {
    viewModel: function(params) {
      var self = this;

      self.comment = params.comment;
      self.comment_id = ko.observable(params.comment.id);
      self.comment_likes = ko.observable(params.comment.likes);

      self.you_id = ko.observable(params.you_id());
      self.signed_in = ko.observable(params.signed_in());

      self.text = ko.observable(params.comment.text);
      self.date_created = ko.observable(params.comment.date_created);

      self.show_editor = ko.observable(false);
      self.edit_text = ko.observable(params.comment.text);

      self.owner_username = ko.observable(params.comment.owner_rel.username);
      self.owner_icon = ko.observable(params.comment.owner_rel.icon);
      self.owner_id = ko.observable(params.comment.owner_rel.id);

      // console.log(params, self);

      self.submitCommentEdits = function() {
        if(self.edit_text() === '') {
          return;
        }

        PUT.edit_comment(self.comment.id, self.edit_text())
        .then(function(resp){
          // if(resp.message) { alert(resp.message); }
          if(resp.error) {
            console.log(resp);
            return;
          }

          self.text(self.edit_text());
          self.show_editor(false);
        })
        .catch(function(error){
          console.log(error);
        })
      }

      self.keyListener = function(data, event) {
        if(event.keyCode === 13) {
          self.submitCommentEdits();
        }
      }

      self.toggle_show_editor = function() {
        self.edit_text = ko.observable(self.text());
        self.show_editor( !self.show_editor() );
      }

      self.delete_comment = function() {
        var ask = confirm("Delete this comment?");
        if(ask === false) { return; }

        DELETE.delete_comment(self.comment.id)
        .then(function(resp){
          // console.log(resp);
          if(resp.error) {
            alert(resp.message);
            return;
          }

          params.parent.delete_comment(self.comment.id);
        })
        .catch(function(error){
          console.log(error);
        })

      }

    },
    template:
        '<div class="space-1">\
          <div class="chip"> \
            <img data-bind="attr: { alt: owner_username, src: owner_icon }"> \
            <a style="color: #039be5; text-transform: lowercase; margin-right: 0px;" data-bind="attr: { title: owner_username(), href: \'\/accounts\/\' + owner_username() }"> \
              <span data-bind="text: owner_username"></span> \
            </a> \
          </div>  \
          <br/> \
          <div> \
            <p class="comment-text" data-bind="text: text"></p> \
            <span class="caption-1"> \
              Created: <em class="text-grey" data-bind="text: date_formatter(date_created())"></em> \
            </span> \
          </div> \
          <div> \
            <comment-likes-widget params="comment_likes: comment_likes(), comment_id: comment_id(), you_id: you_id(), signed_in: signed_in()"></comment-likes-widget> \
          </div> \
          <div data-bind="if: signed_in() && show_editor() === true"> \
            <div class="row"> \
              <div class="input-field col s12"> \
                <input placeholder="Write a comment" data-bind="textInput: edit_text, event: { keyup: keyListener }" > \
              </div> \
            </div> \
          </div> \
          <div data-bind="if: signed_in() && you_id() === owner_id()"> \
            <br/> \
            <span class="action-item transition cursor-class" data-bind="click: toggle_show_editor"><i class="far fa-edit"></i> edit</span> | \
            <span class="action-item transition cursor-class" data-bind="click: delete_comment"><i class="far fa-times-circle"></i> delete</span> \
          </div> \
        </div>'
});
