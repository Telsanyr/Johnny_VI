"use strict";
var ideaTableToHtml = function(table, archived){
  var s = "";
  for(var i = 0; i < table.length; i++){
    if (archived == table[i].archive){
      s += '<tr><th scope="row">'+table[i].id +'</th><td>'+table[i].vote +'</td><td>'+table[i].description +'</td></tr>'
    }
  }

  return s;
}

$(document).ready(function () {
  $.getJSON('./db/ideabox.json', function(data) {
    var ideas = data.ideas
    var table = ideas.sort(function(a,b){return b.vote - a.vote;})

    $("#current_table").html(ideaTableToHtml(table, false))
    $("#archive_table").html(ideaTableToHtml(table, true))

  });
});
