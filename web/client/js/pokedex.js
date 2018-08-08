"use strict";
$(document).ready(function () {
  // Url must be http://domain/pokedex?UserName
  var username = window.location.search.substring(1)
  $("#page_title").text("Pokedex de " + username)

  var POKEMON_DATABASE = []
  $.getJSON('./db/pokemons.json', function(data) {
    POKEMON_DATABASE = data

    $.getJSON('./db/players.json', function(data) {
      var player = undefined
      for(var i=0; i<data.length; i++){
        if (data[i].username === username){
          player = data[i]
        }
      }

      if (player !== undefined){
        var pokedex = player.pokedex
        // Title

        for(var i=1; i<152; i++){
          var pokemon = pokedex[i]
          var index = (1000+i).toString().substring(1)
          var name = POKEMON_DATABASE[i-1].name // ID = Index+1
          var div_class = "pokemon_box" + ((pokemon.amount === 0)? " not_owned" : "") + ((pokemon.amount >= 1)? " owned" : "") + ((pokemon.amount > 1)? " double" : "")
          var image_class = "pokemon_image" + ((pokemon.amount === 0)? " pokemon_missing" : "")
          var amount_html = (pokemon.amount > 1)? '<div class="amount">'+pokemon.amount+'</div>' : ""
          $("#pokedex_section").append(''
            + '<div class="'+div_class+'">'
              + '<div class="'+image_class+'" style="background-image: url(\'../resources/pokemons/'+name.toLowerCase()+'.png\');"></div>'
              + '<div class="pokemon_info">#'+index+' '+name+'</div>'
              + amount_html
            + '</div>')
        }

      // If player does not exist in database
      } else {
        $("#pokedex_section").html('<div class="unknown_player">This player does not exist in database.</div>')
      }
    // If getJSON fail
    }).fail(function() {
      $("#pokedex_section").html('<div class="unknown_player">Unable to load game database.</div>')
    });




  }).fail(function() {
    $("#pokedex_section").html('<div class="unknown_player">Unable to load pokemon database.</div>')
  });
});
