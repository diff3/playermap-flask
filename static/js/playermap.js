// Show info next to cursor
function divShow(e, id) {
  var div = document.getElementById(id);
  div.style.left = 50 + e.clientX + "px";;
  div.style.top = e.clientY + "px";;
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
      location = '<img src="/static/img/map/allia.gif" class="location" id="' + i + '" onmouseover="divShow(event, \'location_information\')" onmouseout="divHide(event,\'location_information\')" \>'

      $("#world").append(location);

      $("#" + i).css({
        'position': 'absolute',
        'left': position[i]['posx'],
        'top': position[i]['posy']
      })
    }

    // show info on mouse click
    $('#world').on('click', ".location", function() {
      ID = $(this).attr('id')
      s = "ID: " + position[ID]['id'] + "<br/>Name:" + position[ID]['name'] + "<br/>posx: " + position[ID]['position_x'] + "<br/>posy: " + position[ID]['position_y'];
      $('#mouse_click_info').html(s);
    });

    // show info next to mouse
    $('#world').on('mouseover', ".location", function() {
      ID = $(this).attr('id')
      s = position[ID]['id'] + "\n" + position[ID]['name'] + "\nposx: " + position[ID]['position_x'] + "\nposy: " + position[ID]['position_y'];
      $("#location_information").text(s)
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
