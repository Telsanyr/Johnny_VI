"use strict";

$(document).ready(function () {
  // Url must be http://domain/events?date
  var date = window.location.search.substring(1)

  $.getJSON('./db/events/events_'+date+'.json', function(data) {
    var table = data.reverse()
    for(var i = 0; i< data.length; i++){
      $("#ZMQ-REQ-CODE-BOX").append(
          '<tr>'
          + '<td>' + table[i].timestamp + '</td>'
          + '<td>' + table[i].event + '</td>'
          + '<td nowrap>' + JSON.stringify(table[i].args) + '</td>'
        + '</tr>');
    }
  });
});
