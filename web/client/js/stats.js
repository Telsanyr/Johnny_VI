"use strict";

var GAME_EVENTS = [];
var DATE_LIST = [];
var POKEMON_DATABASE = [];
var ALL_DENSITY = 0;
var NBR_SPAWN = 0;

$(document).ready(function () {
  retrieveEventsData();
});

function retrieveEventsData(){
  for(var year=2018; year<2019; year++){
    for(var month=1; month<=12; month++){
      for(var day=1; day<=31; day++){
        var s_year = year + '';
        var s_month = month + '';
        if(s_month.length === 1){
          s_month = "0" + s_month;
        }
        var s_day = day + '';
        if(s_day.length === 1){
          s_day = "0" + s_day;
        }
        var s_date = s_year + '-' + s_month + '-' + s_day;
        DATE_LIST.push(s_date);
      }
    }
  }

  //getEventsFromDate();
  // @DEBUG
  getEventsFromDate()
}

// date must be formated YYYY-MM-DD
function getEventsFromDate(){
  if(DATE_LIST.length === 0) {
    // Fin de l'extraction des events.
    retrievePokemonDatabase();
  } else {
    var date = DATE_LIST.pop();
    //@DEBUG : console.log("Date: "+date);
    $.getJSON('./db/events/events_'+date+'.json', function(data) {
      GAME_EVENTS = GAME_EVENTS.concat(data);
      //@DEBUG : console.log("DATA : " + GAME_EVENTS.length);
    }).always(function() {
      getEventsFromDate(); // Meme si le fichier n'existe pas, il faut continuer d'explorer la liste DATE_LIST
    });
  }
}

function retrievePokemonDatabase(){
  //@DEBUG : console.log("--- END DATA RETRIEVING ---");
  $.getJSON('./db/pokemons.json', function(data) {
    POKEMON_DATABASE = data
    for(var i=1; i<152; i++){
      POKEMON_DATABASE[i-1].spawn = 0;
      POKEMON_DATABASE[i-1].catch = 0;
    }

    extractDataFromEvents();
  }).fail(function() {
    $("#pokedex_section").html('<div class="unknown_player">Unable to load pokemon database.</div>')
  });
}

function extractDataFromEvents(){
  var size = GAME_EVENTS.length



  for(var i=0; i < size; i++){
    if(GAME_EVENTS[i].event === "ARENA_SPAWN"){
      var pokemon_id = GAME_EVENTS[i].args.pokemon;
      POKEMON_DATABASE[pokemon_id-1].spawn++;
      NBR_SPAWN++;
    } else if (GAME_EVENTS[i].event === "ARENA_CATCH_SUCCESS"){
      POKEMON_DATABASE[pokemon_id-1].catch++;
    }
  }

  startHtmlInjection();
}

function startHtmlInjection(){
  for(var i=1; i<152; i++){
    ALL_DENSITY += POKEMON_DATABASE[i-1].density;
  }

  for(var i=1; i<152; i++){
    var index = (1000+i).toString().substring(1)
    var name = POKEMON_DATABASE[i-1].name // ID = Index+1
    var theo_spawn_pourcent = 100.0 * POKEMON_DATABASE[i-1].density / ALL_DENSITY;
    var s_theo_spawn_rate = Number.parseFloat(theo_spawn_pourcent).toFixed(3) + '%';
    var appearance = POKEMON_DATABASE[i-1].spawn;
    var s_appearance = appearance + '';
    var app_pourcent = 100.0 * POKEMON_DATABASE[i-1].spawn / NBR_SPAWN;
    var s_app_rate = Number.parseFloat(app_pourcent).toFixed(3) + '%';
    var catched = POKEMON_DATABASE[i-1].catch;
    var s_catched = catched + '';
    $("#pokedex_section").append(''
      + '<div class="pokemon_box">'
        + '<div class="image_box">'
          + '<div class="pokemon_image" style="background-image: url(\'../resources/pokemons/'+name.toLowerCase()+'.png\');"></div>'
          + '<div class="pokemon_info">#'+index+' '+name+'</div>'
        + '</div>'
        + '<div class="stats_box">'
          + 'Theo. spawn rate: '+s_theo_spawn_rate+' </br>'
          + 'Appearances: '+s_appearance+'</br>'
          + 'Appearance rate: '+s_app_rate+' </br>'
          + 'Captured: '+ s_catched
        + '</div>'
      + '</div>')
  }
}
