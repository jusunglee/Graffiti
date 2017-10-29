// Copyright (c) 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

/**
 * Get the current URL.
 *
 * @param {function(string)} callback called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });

  // Most methods of the Chrome extension APIs are asynchronous. This means that
  // you CANNOT do something like this:
  //
  // var url;
  // chrome.tabs.query(queryInfo, (tabs) => {
  //   url = tabs[0].url;
  // });
  // alert(url); // Shows "undefined", because chrome.tabs.query is async.
}

/**
 * Change the background color of the current page.
 *
 * @param {string} color The new background color.
 */
function changeBackgroundColor(color) {
  var script = 'document.body.style.backgroundColor="' + color + '";';
  // See https://developer.chrome.com/extensions/tabs#method-executeScript.
  // chrome.tabs.executeScript allows us to programmatically inject JavaScript
  // into a page. Since we omit the optional first argument "tabId", the script
  // is inserted into the active tab of the current window, which serves as the
  // default.
  chrome.tabs.executeScript({
    code: script
  });
}

/**
 * Gets the saved background color for url.
 *
 * @param {string} url URL whose background color is to be retrieved.
 * @param {function(string)} callback called with the saved background color for
 *     the given url on success, or a falsy value if no color is retrieved.
 */
function getSavedBackgroundColor(url, callback) {
  // See https://developer.chrome.com/apps/storage#type-StorageArea. We check
  // for chrome.runtime.lastError to ensure correctness even when the API call
  // fails.
  chrome.storage.sync.get(url, (items) => {
    callback(chrome.runtime.lastError ? null : items[url]);
  });
}

/**
 * Sets the given background color for url.
 *
 * @param {string} url URL for which background color is to be saved.
 * @param {string} color The background color to be saved.
 */
function saveBackgroundColor(url, color) {
  var items = {};
  items[url] = color;
  // See https://developer.chrome.com/apps/storage#type-StorageArea. We omit the
  // optional callback since we don't need to perform any action once the
  // background color is saved.
  chrome.storage.sync.set(items);
}

function wrapDiv() {
  var div = document.createElement("div");
  div.id = "commentable-area";
  while (document.body.firstElementChild)
  {
    div.appendChild(document.body.firstElementChild);
    
  }
  document.body.appendChild(div);
  
  var array = document.getElementsByTagName('P');
  for (var i = 0; i < array.length; i++) {
    array[i].dataset.sectionId = i.toString();
    array[i].className += " commentable-section";
  }
    
  console.log("divs initialized");
}

wrapDiv();

var SideComments = require('side-comments');
var currentUser = {id: 1,
  avatarUrl: "http://f.cl.ly/items/0s1a0q1y2Z2k2I193k1y/default-user.png",
  name: "Test"};
var existingComments = [
  {
    "sectionId": "1",
    "comments": [
      {
        "authorAvatarUrl": "http://f.cl.ly/items/1W303Y360b260u3v1P0T/jon_snow_small.png",
        "authorName": "Jon Sno",
        "comment": "I'm Ned Stark's bastard. Related: I know nothing."
      },
      {
        "authorAvatarUrl": "http://f.cl.ly/items/2o1a3d2f051L0V0q1p19/donald_draper.png",
        "authorName": "Donald Draper",
        "comment": "I need a scotch."
      }
    ]
  },
  {
    "sectionId": "3",
    "comments": [
      {
        "authorAvatarUrl": "http://f.cl.ly/items/0l1j230k080S0N1P0M3e/clay-davis.png",
        "authorName": "Senator Clay Davis",
        "comment": "These Side Comments are incredible. Sssshhhiiiiieeeee."
      }
    ]
  }
];

sideComments = new SideComments('#commentable-area', currentUser, existingComments);
sideComments.on('commentPosted', function( commentobj ) {
    params = {url:encodeURIComponent(window.location.href) , comment:commentobj.comment, location:commentobj.sectionId};
    console.log(params);
    $.ajax({
        url: 'https://graffitihacktx.herokuapp.com/addcomment',
        type: 'POST',
        data: params,
        success: function( savedComment ) {
            // Once the comment is saved, you can insert the comment into the comment stream with "insertComment(comment)".
            sideComments.insertComment(commentobj);
        }
    });
});
