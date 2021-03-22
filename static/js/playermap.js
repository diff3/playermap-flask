function _pos() {
  this.x = 0;
  this.y = 0;
}

function get_player_position(x, y, m) {
  pos = new _pos()

  x = Math.round(x);
  y = Math.round(y);

  switch (m) {
    case 0:
      xpos = Math.round(x * 0.032);
      ypos = Math.round(y * 0.028);

      pos.x = 695 - ypos;
      pos.y = 231 - xpos;
      break;
    case 1:
      xpos = Math.round(x * 0.03240);
      ypos = Math.round(y * 0.030140);

      pos.x = 145 - ypos;
      pos.y = 390 - xpos;
      break;
    default:
      pos.x = 194 - ypos;
      pos.y = 398 - xpos;

  }
  return pos
}

$(document).ready(function() {
  console.log("ready")

  //connect to the socket server.
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');

  //receive details from server
  socket.on('newposition', function(position) {

    var i;
    test = ""
    for (i = 0; i < position.length; i++) {
      /*
      console.log("name: " + position[i]['name']);
      console.log("posx: " + position[i]['position_x']);
      console.log("posy: " + position[i]['position_y']);
      console.log("race: " + position[i]['race']);
      console.log("class: " + position[i]['class']);
      console.log("level: " + position[i]['level']);
      console.log("map: " + position[i]['map']);
      console.log("zone: " + position[i]['zone']);
      console.log();
      */

      map = parseInt(position[i]['map'])
      pos = get_player_position(position[i]['position_x'], position[i]['position_y'], map);

      test += '<img src="/static/img/map/allia.gif" id="pointsOldworld" style="position: absolute; border: 0px; left: ' + pos.x + 'px; top: ' + pos.y + 'px;" \>';
    }
    $("#world").html(test);

  });
});
