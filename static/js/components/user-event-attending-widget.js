/* --- Comment Like --- */


ko.components.register('user-event-attending-widget', {
    viewModel: function(params) {
      var self = this;

      self.you_id = ko.observable(params.root.you().id);
      self.you_type = ko.observable(params.root.you().type);
      self.signed_in = ko.observable(params.root.signed_in());

      var event_id = params.event_id.constructor === Function ? params.event_id() : params.event_id;
      self.event_id = ko.observable(event_id);

      self.event_attending = params.event_attending();
      self.attendingLength = ko.observable(self.event_attending);
      self.attending = ko.observable(false);

      // console.log(params);
      // console.log(self);

      self.check_event_attending = function() {
        GET.check_event_attending(event_id)
        .then(function(resp) {
          if(resp.error) {
            console.log(resp);
            return;
          }

          self.attending(resp.attending);
        })
        .catch(function(error){
          console.log(error);
        })
      }

      if(self.signed_in() === true && self.you_type() === 'USER') {
        self.check_event_attending();
      }

      self.toggle_event_attending = function() {
        if(self.signed_in() === false) { return }
        if(self.you_type() !== 'USER') { Materialize.toast('Only USERs can attend Events', 2000); return }

        POST.toggle_event_attending(event_id)
        .then(function(resp){
          // if(resp.message) { alert(resp.message); }
          if(resp.error) {
            console.log(resp);
            return;
          }

          self.attending(resp.attending);

          if(resp.attending == true) {
            self.event_attending++;
          }
          else {
            self.event_attending--;
          }

          self.attendingLength(self.event_attending);
        })
        .catch(function(error){
          console.log(error);
        })
      }

    },
    template:
        '<div class=""> \
            <span title="toggle attending status" class="cursor-class" data-bind="click: toggle_event_attending, if: attending()"> \
              <i class="fas fa-user"></i> \
            </span> \
            <span title="toggle attending status" class="cursor-class" data-bind="click: toggle_event_attending, if: !attending()"> \
              <i class="far fa-user"></i> \
            </span> \
            <span data-bind="text: attendingLength"></span> | <a style="text-transform: none;	color: #039be5; margin-right: 0px" class="cursor-class" data-bind="attr: { title: \'Event Attending\', href: \'/events/\' + event_id() + \'/attending\' }">Users Attending</a> \
            <span data-bind="if: you_type() === \'USER\'"> \
              <span data-bind="if: attending() === true">(<span class="text-color-green">Attending!</span>)</span> \
              <span data-bind="if: attending() === false">(<span class="text-color-red">Not Attending</span>)</span> \
            </span> \
        </div>'
});
