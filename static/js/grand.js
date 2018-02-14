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

function validateUsername(username) {
  var re = /^[a-z0-9\-\_\.]{3,}$/;
  return re.test(username.toLowerCase());
}

function validateEmail(email) {
  var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email.toLowerCase());
}

function validatePassword(password) {
  var re = /^[a-zA-Z0-9\-\_\.\!\@\#\$\%\&\?]{7,}$/;
  return re.test(password);
}

function headers_json() {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json; charset=UTF-8");
  myHeaders.append("Accept", "application/json");
  return myHeaders;
}

function getFileName(link) {
  return link && link.constructor == String ? link.split('?')[0].split('/o/')[1] : '';
}
