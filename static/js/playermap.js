// Show info next to cursor
function divShow(e, id) {
  var div = document.getElementById(id);
  div.style.left = 10 + e.clientX + "px";;
  div.style.top = -101 + e.clientY + "px";;
  $("#" + id).show();
}

// hide it
function divHide(e, id) {
  var div = document.getElementById(id);
  $("#" + id).hide();
}

$(document).ready(function() {
  console.log("ready");


  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');
  var position = ""

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
        $("#orientation").text("orientation: " + position[ID]['position_o']);
      });
    }
  });

  //receive details from server
  socket.on('newposition', function(position) {
    var locations;
    var i;
    $("#world").html("");
    for (i = 0; i < position.length; i++) {
      console.log("update" + position[i])
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

    }


    // show info on mouse click
    $('#world').on('click', ".player_location", function() {
      ID = $(this).attr('id')
      s = "ID: " + position[ID]['id'] + "<br/>Name:" + position[ID]['name'] + "<br/>posx: " + position[ID]['position_x'] + "<br/>posy: " + position[ID]['position_y'];
      $('#mouse_click_info').html(s);
    });

    // show info next to mouse, player
    $('#world').on('mouseover', ".player_location", function() {
      ID = $(this).attr('id');

      $("#name").text(position[ID]['name']);
      $("#level").text("Level " + position[ID]['level']);
      $("#guild").text("Glory of Potatos");
      $("#name").text(position[ID]['name']);
      $("#faction").html("<img src='/static/img/map/" + position[ID]['faction'] + "icon.gif' />");
      $("#race").html("<img src='/static/img/c_icons/" + position[ID]['race'] + "-" + position[ID]['gender'] + ".gif' />");
      $("#class").html("<img src='/static/img/c_icons/" + position[ID]['class'] + ".gif' />");
      $("#zone").text(position[ID]['zone']);
    });
  });

  $('#get_worldport').on('click', function() {
    socket.emit('get_worldport', 'update');
    console.log("Sending: worldport update");
    $("#world").html("");
  });

  $('#get_creature_position').on('click', function() {
    socket.emit('get_creature_position', 'update');
    console.log("Sending: creatures update");
    $("#world").html("");
  });

  $('#get_player_position').on('click', function() {
    socket.emit('get_player_position', 'update');
    console.log("Sending: player updates");
    $("#world").html("");
  });

  $('#get_gameobjects').on('click', function() {
    socket.emit('get_gameobjects', 'update');
    console.log("Sending: game objects update");
    $("#world").html("");
  });

  $('#get_taxi_nodes').on('click', function() {
    socket.emit('get_taxi_nodes', 'update');
    console.log("Sending: taxiNode update");
    $("#world").html("");
  });
});
