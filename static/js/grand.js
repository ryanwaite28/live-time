'use strict';

const templateFromUrlLoader = {
    loadTemplate: function(name, templateConfig, callback) {
        if (templateConfig.fromUrl) {
            // Uses jQuery's ajax facility to load the markup from a file
            var fullUrl = '/static/html/' + templateConfig.fromUrl + '?cacheAge=' + templateConfig.maxCacheAge;
            $.get(fullUrl, function(markupString) {
                // We need an array of DOM nodes, not a string.
                // We can use the default loader to convert to the
                // required format.
                ko.components.defaultLoader.loadTemplate(name, markupString, callback);
            });
        } else {
            // Unrecognized config format. Let another loader handle it.
            callback(null);
        }
    }
};

// Register it
ko.components.loaders.unshift(templateFromUrlLoader);



const viewModelCustomLoader = {
    loadViewModel: function(name, viewModelConfig, callback) {
        if (viewModelConfig.viaLoader) {
            // You could use arbitrary logic, e.g., a third-party
            // code loader, to asynchronously supply the constructor.
            // For this example, just use a hard-coded constructor function.
            var viewModelConstructor = function(params) {
                this.prop1 = 123;
            };

            // We need a createViewModel function, not a plain constructor.
            // We can use the default loader to convert to the
            // required format.
            ko.components.defaultLoader.loadViewModel(name, viewModelConstructor, callback);
        } else {
            // Unrecognized config format. Let another loader handle it.
            callback(null);
        }
    }
};

// Register it
ko.components.loaders.unshift(viewModelCustomLoader);


/* --- */

const validateUsername = function(username) {
  var re = /^[a-z0-9\-\_\.]{3,24}$/;
  return re.test(username.toLowerCase());
}

const validateEmail = function(email) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email.toLowerCase());
}

const validatePassword = function(password) {
  var re = /^[a-zA-Z0-9\-\_\.\!\@\#\$\%\&\?]{7,}$/;
  return re.test(password);
}

const validateLink = function(link) {
  var re = /(^|[\s\n]|<[A-Za-z]*\/?>)((?:https?|ftp):\/\/[\-A-Z0-9+\u0026\u2019@#\/%?=()~_|!:,.;]*[\-A-Z0-9+\u0026@#\/%=~()_|])/gi;
  return re.test(link);
}

const date_formatter = function(date) {
  // format --- December 23, 2017 - 10:40 PM
  // console.log(date);
  return moment(date).format('MMMM D, YYYY - h:mm A');
}

const headers_json = function() {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json; charset=UTF-8");
  myHeaders.append("Accept", "application/json");
  return myHeaders;
}

const getFileName = function(link) {
  return link && link.constructor == String ? link.split('?')[0].split('/o/')[1] : '';
}

const disable_buttons = function() {
  $('button.btn').addClass("disabled");
}
const enable_buttons = function() {
  $('button.btn').removeClass("disabled");
}

const get_image_file = function(elem_id = '') {
  if(!elem_id || elem_id.constructor !== String) {
    console.log('string is required...', elem_id);
    return null;
  }

  var file = document.getElementById(elem_id).files[0];

  if(file) {
    var accepted_file_types = ['jpg', 'jpeg', 'png', 'gif'];
    var type = file.type.split("/");
    if (type[0] !== "image" || accepted_file_types.indexOf(type[1]) === -1) {
      console.log("File must be an image: jpg, png, or gif", elem_id, file);
      return null;
    }
    else {
      return file;
    }
  }
  else {
    return null;
  }
}
