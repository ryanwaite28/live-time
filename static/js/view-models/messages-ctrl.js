'use strict';

(function(){

  function mvc() {
    var self = this;
    window.logmvc = function() { console.log(self); }

    self.signed_in = ko.observable(false);
    self.you = ko.observable({});

    //

    self.current_conversation = ko.observable(null);
    self.current_conversation_id = ko.observable(null);
    self.conversationsList = ko.observableArray([]);

    self.account = ko.observable(null);
    self.account_id = ko.observable(null);
    self.message_input = ko.observable('');

    self.messagesList = ko.observableArray([]);
    self.messagesIDs = ko.observableArray([]);
    self.messagessObj = {};

    self.min_message_id = 0;
    self.end = ko.observable(false);

    GET.check_session()
    .then(function(resp){
      // console.log(resp);
      self.signed_in(resp.online);
      if(resp.account) {
        self.you(resp.account);
      }
      self.get_account_conversations();
    });

    //

    self.get_account_conversations = function() {
      disable_buttons();

      GET.get_account_conversations()
      .then(function(resp){
        // console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        self.conversationsList(resp.conversations);
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.get_conversation_messages = function() {
      disable_buttons();

      GET.get_conversation_messages(self.current_conversation_id(), self.min_message_id)
      .then(function(resp){
        // console.log(resp);
        enable_buttons();

        if(resp.error) {
          alert(resp.message);
          return;
        }

        if(resp.conversation_messages.length < 5) {
          self.end(true);
        }

        resp.conversation_messages.forEach(function(conversation_message){
          self.messagesList.unshift(conversation_message);
          self.messagesIDs.unshift(conversation_message.id);
          self.messagessObj[conversation_message.unique_value] = conversation_message;
        });

        self.min_message_id = self.messagesIDs().length > 0 ?
        Math.min(...self.messagesIDs()) : 0;
      })
      .catch(function(error){
        console.log(error);
      })
    }

    self.set_current_conversation = function(conversation) {
      // console.log(conversation);
      self.current_conversation(conversation);
      self.current_conversation_id(conversation.id);

      var account = self.you().id == conversation.account_A_id ?
      conversation.account_B_rel : conversation.account_A_rel;

      var account_id = self.you().id == conversation.account_A_id ?
      conversation.account_B_id : conversation.account_A_id;

      self.account(account);
      self.account_id(account_id);

      self.messagesList([]);
      self.messagesIDs([]);
      self.messagessObj = {};

      self.min_message_id = 0;
      self.end(false);

      self.get_conversation_messages();
    }

    self.send_message = function() {
      if(self.signed_in() === false) { return }
      if(self.account_id() === null) { return }
      if(self.message_input().trim().length < 2) { alert('messages must be at least 2 characters.'); return }

      POST.send_account_message(self.account_id(), self.message_input())
      .then(function(resp){
        if(resp.error) {
          console.log(resp);
          return
        }

        // self.messagesList.push(resp.new_message);
        // self.messagesIDs.push(resp.new_message.id);
        // self.messagessObj[resp.new_message.unique_value] = resp.new_message;

        self.message_input('');
        Materialize.toast('Message Sent!', 2000)
      })
    }

    // Listen For New Messages

    var source = new EventSource("/stream");

    source.onopen = function() {
      console.log("Listening for new messages...");
    };

    source.addEventListener('action', function(event) {
      var data = JSON.parse(event.data);
      console.log(data);
      if(data.for_id === self.you().id) {
        Materialize.toast(data.message, 5000);
      }
    }, false);

    source.addEventListener('message', function(event) {
      var data = JSON.parse(event.data);
      console.log(data);
      if(data.conversation_message.conversation_id === self.current_conversation_id()) {
        self.messagesList.push(data.conversation_message);
        self.messagesIDs.push(data.conversation_message.id);
        self.messagessObj[data.conversation_message.unique_value] = data.conversation_message;
      }
    }, false);

    source.addEventListener('error', function(event) {
      console.log(event);
    }, false);

  }

  ko.applyBindings(new mvc());
})()
