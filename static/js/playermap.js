// Show info next to cursor

// it's marks on page width, no mather where on page it is

function divShow(e, id) {
  var div = document.getElementById(id);

  var height = e.pageY - $(div).height() - 10;
  var width = e.pageX + $(div).width() + 10;

  var offsetY = 0;
  var offsetX = 0;

  if (0 > height) {
    offsetY = Number($(div).height() + 30);
  }

  if ($(window).width() < width) {
    offsetX = Number($(div).width() + 10);
  }

  div.style.left = e.pageX - offsetX + "px";
  div.style.top = height + offsetY + "px";

  $("#" + id).show();
}

// hide it
function divHide(e, id) {
  var div = document.getElementById(id);
  $("#" + id).hide();
}
var position;

$(document).ready(function() {


  console.log("ready");


  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');

  socket.on('new_worldport', function(position) {
    console.log("Worldport update")
    var i, locations;

    $("#world").html("");
    for (i = 0; i < position.length; i++) {
      locations = '<img src="/static/img/map/group-icon.gif" class="worldport_location" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';

      $("#world").append(locations);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      });

      $('#world').on('mouseover', ".worldport_location", function() {
        ID = $(this).attr('id');

        $("#cname").text(position[ID]['name']);
        $("#spawnid").text("id: " + position[ID]['id']);
        $("#cposx").text("posx: " + position[ID]['position_x']);
        $("#cposy").text("posy: " + position[ID]['position_y']);
      });
    }
  });

  socket.on('new_creature_position', function(position) {
    console.log("new creature position update")
    var i, locations;

    $("#world").html("");
    for (i = 0; i < position.length; i++) {
      locations = '<img src="/static/img/map/group-icon.gif" class="new_creature_position" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';

      $("#world").append(locations);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      });

      $('#world').on('mouseover', ".new_creature_position", function() {
        ID = $(this).attr('id');

        $("#cname").text(position[ID]['name']);
        $("#spawnid").text("spawn id: " + position[ID]['id']);
        $("#cposx").text("posx: " + position[ID]['position_x']);
        $("#cposy").text("posy: " + position[ID]['position_y']);
        $("#cposz").text("posz: " + position[ID]['position_z']);
        $("#orientation").text("o: " + position[ID]['orientation']);
        $("#cimage").html("<img id='cimg' src='/static/img/alpha/creature-display-" + position[ID]['display_id'] + ".jpg' />")
      });
    }
  });

  socket.on('new_taxi_location', function(position) {
    console.log("new taxi position update")
    var i, locations;

    $("#world").html("");
    for (i = 0; i < position.length; i++) {
      locations = '<img src="/static/img/map/group-icon.gif" class="new_taxi_location" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';

      $("#world").append(locations);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      });

      $('#world').on('mouseover', ".new_taxi_location", function() {
        ID = $(this).attr('id');

        $("#cname").text(position[ID]['name']);
        $("#spawnid").text("id: " + position[ID]['id']);
        $("#cposx").text("posx: " + position[ID]['position_x']);
        $("#cposy").text("posy: " + position[ID]['position_y']);
      });
    }
  });

  socket.on('new_gameobjects', function(position) {
    console.log("new gameobjects update")
    var i, locations;

    $("#world").html("");
    for (i = 0; i < position.length; i++) {
      locations = '<img src="/static/img/map/group-icon.gif" class="new_gameobjects_position" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';

      $("#world").append(locations);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      });

      $('#world').on('mouseover', ".new_gameobjects_position", function() {
        ID = $(this).attr('id');
        $("#cname").text(position[ID]['name']);
        $("#spawnid").text("id: " + position[ID]['id']);
        $("#cposx").text("posx: " + position[ID]['position_x']);
        $("#cposy").text("posy: " + position[ID]['position_y']);
        $("#cposz").text("posz: " + position[ID]['position_z']);
      });
    }
  });

  socket.on('player_online', function(online) {
    $("#player_online").text(online + " online")
  });

  //receive details from server
  socket.on('newposition', function(position) {
    var locations;
    var i;
    $("#world").html("");

    for (i = 0; i < position.length; i++) {
      if (position[i]['show'] == 'player_information') {
        locations = '<img src="/static/img/map/' + position[i]["faction"] + '.gif" class="player_location" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>'
      } else {
        locations = '<img src="/static/img/map/group-icon.gif" class="player_location" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>'
      }

      $("#world").append(locations);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      });

      $("#" + i).data("data-name", position[i]["name"])
      $("#" + i).data("data-level", position[i]["level"])
      $("#" + i).data("data-zone", position[i]["zone"])
      $("#" + i).data("data-race", position[i]["race"])
      $("#" + i).data("data-class", position[i]["class"])
      $("#" + i).data("data-faction", position[i]["faction"])
      $("#" + i).data("data-gender", position[i]["gender"])
    }

    // show info next to mouse, player
    $('#world').on('mouseover', ".player_location", function(event) {
      ID = $(this).attr('id');

      $("#name").text($("#" + ID).data("data-name"));
      $("#level").text("Level " + $("#" + ID).data("data-level"));
      // $("#guild").text(position[ID]['guild']));
      $("#faction").html("<img class='left_padding' src='/static/img/map/" + $("#" + ID).data("data-faction") + "icon.gif' />");
      $("#race").html("<img class='left_padding' src='/static/img/c_icons/" + $("#" + ID).data("data-race") + "-" + $("#" + ID).data("data-gender") + ".gif' />");
      $("#class").html("<img class='left_padding' src='/static/img/c_icons/" + $("#" + ID).data("data-class") + ".gif' />");
      $("#zone").html($("#" + ID).data("data-zone"));
    });
  });

  $('#get_worldport').on('click', function() {
    socket.emit('get_worldport', 'update');
    console.log("Sending: worldport update");
    $("#world").html("");
    $("orientation").html("");
    $("cimage").html("");
    $("#cposz").text("");
    position = null;
  });

  $('#get_creature_position').on('click', function() {
    socket.emit('get_creature_position', 'update');
    console.log("Sending: creatures update");
    $("#world").html("");
    $("orientation").html("");
    $("cimage").html("");
    $("#cposz").text("");
    position = null;
  });

  $('#get_player_position').on('click', function() {
    socket.emit('get_player_position', 'update');
    console.log("Sending: player updates");
    $("#world").html("");
    $("orientation").html("");
    $("cimage").html("");
    $("#cposz").text("");
    position = null;
  });

  $('#get_gameobjects').on('click', function() {
    socket.emit('get_gameobjects', 'update');
    console.log("Sending: game objects update");
    $("#world").html("");
    $("orientation").html("");
    $("#cposz").text("");
    $("cimage").html("");
    position = null;
  });

  $('#get_taxi_nodes').on('click', function() {
    socket.emit('get_taxi_nodes', 'update');
    console.log("Sending: taxiNode update");
    $("#world").html("");
    $("#cposz").text("");
    $("orientation").html("");
    $("cimage").html("");
    position = null;
  });
});
