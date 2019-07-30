"use strict";

var GAME_EVENTS = [];
var DATE_LIST = [];
var POKEMON_DATABASE;
var PLAYERS_DATABASE;
var ALL_DENSITY = 0;
var NBR_SPAWN = 0;
var POKEMON_TRY_BY_LEVEL = [undefined, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]; // from 1 to 10
var PLAYERS_LIST = [];
var PROBABILITY_REF = [undefined, [undefined,'-','-','-','-','-','-','-','-','-','-'], [undefined,'-','-','-','-','-','-','-','-','-','-'], [undefined,'-','-','-','-','-','-','-','-','-','-'], [undefined,'-','-','-','-','-','-','-','-','-','-']];
var BOXES_AVG_REF = [undefined, 3.00, 0.50, 0.03, 3.00, 0.99, 0.005, 0.005, 0.005];
var BOXES_OPENING_STATS = [];

$(document).ready(function () {
  retrieveEventsData();
});

function retrieveEventsData(){
  for(var year=2018; year<=2019; year++){
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

  getEventsFromDate();
}

// date must be formated YYYY-MM-DD
function getEventsFromDate(){
  if(DATE_LIST.length === 0) {
    // End of events extraction
    retrievePokemonDatabase();
  } else {
    var date = DATE_LIST.pop();
    //@DEBUG : console.log("Date: "+date);
    $.getJSON('./db/events/events_'+date+'.json', function(data) {
      GAME_EVENTS = GAME_EVENTS.concat(data);
      //@DEBUG : console.log("DATA : " + GAME_EVENTS.length);
      $("#loading_text").text("Loading database ("+GAME_EVENTS.length+" events found).");
    }).always(function() {
      getEventsFromDate(); // If file is not found it will failed but we still want to keep exploring data files (from DATE_LIST)
    });
  }
}

function retrievePokemonDatabase(){
  //@DEBUG : console.log("--- END DATA RETRIEVING ---");
  $("#loading_text").text("Loading pokemons database.");
  $.getJSON('./db/pokemons.json', function(data) {
    POKEMON_DATABASE = data
    for(var i=1; i<152; i++){
      POKEMON_DATABASE[i-1].spawn = 0;
      POKEMON_DATABASE[i-1].catch = 0;
    }

    retrievePlayers();
  }).fail(function() {
    $("#pokedex_section").html('<div class="unknown_player">Unable to load pokemon database.</div>')
  });
}

function retrievePlayers(){
  $("#loading_text").text("Loading players database.");
  $.getJSON('./db/players.json', function(data) {
    PLAYERS_DATABASE = data;
    for(var i=0; i<data.length; i++){
      PLAYERS_LIST.push(data[i].username);
    }
    extractDataFromEvents();
  });
}

function extractDataFromEvents(){
  $("#loading_text").text("Computing statistics.");
  var size = GAME_EVENTS.length;
  for(var i=0; i < size; i++){
    if(GAME_EVENTS[i].event === "ARENA_SPAWN"){
      var pokemon_id = GAME_EVENTS[i].args.pokemon;
      POKEMON_DATABASE[pokemon_id-1].spawn++;
      NBR_SPAWN++;

    } else if (GAME_EVENTS[i].event === "ARENA_CATCH_SUCCESS"){
      var pokemon_id = GAME_EVENTS[i].args.pokemon;
      POKEMON_DATABASE[pokemon_id-1].catch++;

      extractLuckFromEvent(GAME_EVENTS[i].args, true);  // Luck computation
    } else if (GAME_EVENTS[i].event === "ARENA_CATCH_FAIL"){

      extractLuckFromEvent(GAME_EVENTS[i].args, false);  // Luck computation
    } else if (GAME_EVENTS[i].event === "OPEN_LOOTBOX"){

      extractBoxesFromEvent(GAME_EVENTS[i].args);
    }
  }

  playersBoxesHtmlInjection();
  playersLuckHtmlInjection();
  pokemonHtmlInjection();
}

function extractBoxesFromEvent(args){
  var player = args.player;
  if(BOXES_OPENING_STATS[player] === undefined){
    BOXES_OPENING_STATS[player] = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  }

  for(var i=0; i < args.loots.length; i++){
    var amount = (args.loots[i]).amount;
    var pokestuff = (args.loots[i]).pokestuff;
    if(pokestuff >= 1 && pokestuff <= 8){
      BOXES_OPENING_STATS[player][0] += 1;
      BOXES_OPENING_STATS[player][pokestuff] += amount;
    }
  }
}

function extractLuckFromEvent(args, success){
  var pokemon_id = args.pokemon;
  var player = args.player;
  var amount = args.amount;
  var pokestuff = args.pokestuff;
  var lvl = POKEMON_DATABASE[pokemon_id-1].power;
  if((POKEMON_TRY_BY_LEVEL[lvl])[player] === undefined){
    (POKEMON_TRY_BY_LEVEL[lvl])[player] = [0,0,0,0,0,0,0,0]; // (try, success)
  }
  (POKEMON_TRY_BY_LEVEL[lvl])[player][2*(pokestuff - 1)] += amount;
  if(success){
    (POKEMON_TRY_BY_LEVEL[lvl])[player][2*(pokestuff - 1) + 1]++;
  }

  //proba ref
  PROBABILITY_REF[pokestuff][lvl] = args.probability;
}

function playersBoxesHtmlInjection(){
  // proba ref (first line)
    var table_name = "boxes_table";
     $('#'+table_name).append(''
       + '<tr>'
         + '<th scope="row"><i>PROBABILITIES</i></th>'
         + '<td></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[1] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[2] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[3] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[4] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[5] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[6] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[7] + '%</i></td>'
         + '<td><i>ref: ' + BOXES_AVG_REF[8] + '%</i></td>'
       + '</tr>'
     );

  for(var user_id = 0; user_id < PLAYERS_LIST.length; user_id++){
    var username = PLAYERS_LIST[user_id];
    var boxes_data = BOXES_OPENING_STATS[username];
    if(boxes_data !== undefined){
      $('#'+table_name).append(''
        + '<tr>'
          + '<th scope="row">'+username+'</th>'
          + '<td>'+(boxes_data[0] !== 0 ? boxes_data[0] : '-')+'</td>'
          + '<td>'+(boxes_data[1] !== 0 ? (boxes_data[1]+' ('+Number.parseFloat(boxes_data[1]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[2] !== 0 ? (boxes_data[2]+' ('+Number.parseFloat(boxes_data[2]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[3] !== 0 ? (boxes_data[3]+' ('+Number.parseFloat(boxes_data[3]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[4] !== 0 ? (boxes_data[4]+' ('+Number.parseFloat(boxes_data[4]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[5] !== 0 ? (boxes_data[5]+' ('+Number.parseFloat(boxes_data[5]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[6] !== 0 ? (boxes_data[6]+' ('+Number.parseFloat(boxes_data[6]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[7] !== 0 ? (boxes_data[7]+' ('+Number.parseFloat(boxes_data[7]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
          + '<td>'+(boxes_data[8] !== 0 ? (boxes_data[8]+' ('+Number.parseFloat(boxes_data[8]*100.0/boxes_data[0]).toFixed(1) + '%)') : '-')+'</td>'
        + '</tr>'
      );
    }
  }
}

function playersLuckHtmlInjection(){
  // proba ref (first line)
  for(var lvl=1; lvl <= 10; lvl++){
    var table_name = "lvl_"+lvl+"_table";
     $('#'+table_name).append(''
       + '<tr>'
         + '<th scope="row"><i>PROBABILITIES</i></th>'
         + '<td></td>'
         + '<td><i>' + (PROBABILITY_REF[1][lvl] !== '-' ? 'ref: ' + Number.parseFloat(100*PROBABILITY_REF[1][lvl]).toFixed(2) + '%' : '') + '</i></td>'
         + '<td></td>'
         + '<td><i>' + (PROBABILITY_REF[2][lvl] !== '-' ? 'ref: ' + Number.parseFloat(100*PROBABILITY_REF[2][lvl]).toFixed(2) + '%' : '') + '</i></td>'
         + '<td></td>'
         + '<td><i>' + (PROBABILITY_REF[3][lvl] !== '-' ? 'ref: ' + Number.parseFloat(100*PROBABILITY_REF[3][lvl]).toFixed(2) + '%' : '') + '</i></td>'
         + '<td></td>'
         + '<td><i>' + (PROBABILITY_REF[4][lvl] !== '-' ? 'ref: ' + Number.parseFloat(100*PROBABILITY_REF[4][lvl]).toFixed(2) + '%' : '') + '</i></td>'
       + '</tr>'
     );
  }

  for(var user_id = 0; user_id < PLAYERS_LIST.length; user_id++){
    var username = PLAYERS_LIST[user_id];

    for(var lvl=1; lvl <= 10; lvl++){
      var table_name = "lvl_"+lvl+"_table";
      var luck_data = (POKEMON_TRY_BY_LEVEL[lvl])[username];
      if(luck_data !== undefined){
        $('#'+table_name).append(''
          + '<tr>'
            + '<th scope="row">'+username+'</th>'
            + '<td>'+(luck_data[0] !== 0 ? luck_data[0] : '-')+'</td>'
            + '<td>'+(luck_data[0] !== 0 ? (luck_data[1]+' ('+Number.parseFloat(luck_data[1]*100.0/luck_data[0]).toFixed(1) + '%)') : '-')+'</td>'
            + '<td>'+(luck_data[2] !== 0 ? luck_data[2] : '-')+'</td>'
            + '<td>'+(luck_data[2] !== 0 ? (luck_data[3]+' ('+Number.parseFloat(luck_data[3]*100.0/luck_data[2]).toFixed(1) + '%)') : '-')+'</td>'
            + '<td>'+(luck_data[4] !== 0 ? luck_data[4] : '-')+'</td>'
            + '<td>'+(luck_data[4] !== 0 ? (luck_data[5]+' ('+Number.parseFloat(luck_data[5]*100.0/luck_data[4]).toFixed(1) + '%)') : '-')+'</td>'
            + '<td>'+(luck_data[6] !== 0 ? luck_data[6] : '-')+'</td>'
            + '<td>'+(luck_data[6] !== 0 ? (luck_data[7]+' ('+Number.parseFloat(luck_data[7]*100.0/luck_data[6]).toFixed(1) + '%)') : '-')+'</td>'
          + '</tr>'
        );
      }
    }
  }
}

function pokemonHtmlInjection(){
  for(var i=1; i<152; i++){
    ALL_DENSITY += POKEMON_DATABASE[i-1].density;
  }

  // hide loading
  $("#loading_box").css("display", "none");
  $("#centent_box").css("display", "block");

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
