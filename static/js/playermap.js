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
  console.log("ready")

  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');

  // var position

  //receive details from server
  socket.on('newposition', function(position) {
    var i, location;

    for (i = 0; i < position.length; i++)
    {
      if (position[i]['show'] == 'player_information') {
        location = '<img src="/static/img/map/' + position[i]["faction"] + '.gif" class="player_location" id="' + i + '" onmouseover="divShow(event, \''+position[i]['show']+'\')" onmouseout="divHide(event,\''+position[i]['show']+'\')" \>'
      }
      else {
        location = '<img src="/static/img/map/group-icon.gif" class="location" id="' + i + '" onmouseover="divShow(event, \''+position[i]['show']+'\')" onmouseout="divHide(event,\''+position[i]['show']+'\')" \>'
      }


      $("#world").append(location);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      })
    }

    // show info on mouse click
    $('#world').on('click', ".player_location", function() {
      ID = $(this).attr('id')
      s = "ID: " + position[ID]['id'] + "<br/>Name:" + position[ID]['name'] + "<br/>posx: " + position[ID]['position_x'] + "<br/>posy: " + position[ID]['position_y'];
      $('#mouse_click_info').html(s);
    });

    // show info next to mouse, player
    $('#world').on('mouseover', ".player_location", function() {
      ID = $(this).attr('id')

      $("#name").text(position[ID]['name']);
      $("#level").text("Level " + position[ID]['level']);
      $("#guild").text("Glory of Potatos");
      $("#name").text(position[ID]['name']);
      $("#faction").html("<img src='/static/img/map/"+position[ID]['faction']+"icon.gif' />");
      $("#race").html("<img src='/static/img/c_icons/"+position[ID]['race']+"-"+position[ID]['gender']+".gif' />");
      $("#class").html("<img src='/static/img/c_icons/"+position[ID]['class']+".gif' />");
      $("#zone").text(position[ID]['zone']);
    });

    // show info next to mouse, creatures
    $('#world').on('mouseover', ".location", function() {
      ID = $(this).attr('id')

      $("#cname").text(position[ID]['name']);
      $("#spawnid").text("spawn id: " + position[ID]['id']);
      $("#cposx").text("posx: " + position[ID]['position_x']);
      $("#cposy").text("posx: " + position[ID]['position_y']);
      $("#cposz").text("posz: " + position[ID]['position_z']);
      $("#orientation").text("o: " + position[ID]['orientation']);
      $("#cimage").html("<img id='cimg' src='/static/img/alpha/creature-display-" + position[ID]['display_id'] + ".jpg' />")
    });
  });
  //$("#world").html(location);

  $('#submit_to_server').on('click', function() {
    socket.emit('message_from_browser', 'Hello from browser');
    console.log("Sending: Hello from browser");
  });

  socket.on('message_from_server', function(msg) {
    console.log("Got this: " + msg);
    $("#mouse_click_info").html(msg)
  });
});
