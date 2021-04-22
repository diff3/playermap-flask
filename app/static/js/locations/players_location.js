function player_pos(positions) {
  var pos_x, pos_y, size_x, size_y;
  var xmin, xmax, ymin, ymax;

  var xmin = -17000;
  var xmax = 17000;

  var ymin = -17000;
  var ymax = 17000;

  position = $("#world").position();

  pos_x = position.left;
  pos_y = position.top;

  console.log("pos_x: " + pos_x)
  console.log("pos_y: " + pos_y)

  size_x = $("#world").width();
  size_y = $("#world").height();

  console.log("size_x: " +  size_x);
  console.log("size_y: " +  size_y);

  var player_x = positions['position_x'];
  var player_y = positions['position_y'];

  console.log("player_x: " + player_x);
  console.log("player_y: " + player_y);

  var player_xx = (player_x - xmin) / (xmax - xmin);
  var player_yy = (player_y - ymin) / (ymax - ymin);

  console.log("player_xx: " + player_xx);
  console.log("plauer_yy: " + player_yy);

  // posx = size_x * player_xx + 393;
  // posy = size_y * player_yy + 25;

   posx = (pos_x + size_x) * player_xx;
   posy = (pos_y + size_y) * player_yy;

  console.log("posx: " + posx);
  console.log("posy: " + posy);

  // return posy, posx - (posx * 2);
  return posx, posy;
}

function players_location(position) {
  $("#world").empty();

  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/' + position[i]["faction"] + '.gif" class="player_info icon" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>'
    var locations2 = '<img src="/static/img/map/group-icon.gif" class="player_info icon" id="a' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>'

    $("#world").append(locations);
    $("#world").append(locations2);

    // more to utils?
    $("#" + i).css({
      'position': 'absolute',
      'left': position[i]['posx'],
      'top': position[i]['posy']
    });

    // save data to image tag
    $("#" + i).data("data-name", position[i]["name"]);
    $("#" + i).data("data-level", position[i]["level"]);
    $("#" + i).data("data-zone", position[i]["zone"]);
    $("#" + i).data("data-race", position[i]["race"]);
    $("#" + i).data("data-class", position[i]["class"]);
    $("#" + i).data("data-faction", position[i]["faction"]);
    $("#" + i).data("data-gender", position[i]["gender"]);
  }

  // show info next to cursor
  $('#world').on('mouseover', ".player_info", function(event) {
    ID = $(this).attr('id');

    $("#player_info_popup .row .title #name").text($("#" + ID).data("data-name"));
    $("#player_info_popup .row #level").text("Level " + $("#" + ID).data("data-level"));
    // $("#player_info_popup .row #guild").text(position[ID]['guild']));
    $("#player_info_popup .row #faction").html("<img class='left_padding' src='/static/img/map/" + $("#" + ID).data("data-faction") + "icon.gif' />");
    $("#player_info_popup .row #race").html("<img class='left_padding' src='/static/img/c_icons/" + $("#" + ID).data("data-race") + "-" + $("#" + ID).data("data-gender") + ".gif' />");
    $("#player_info_popup .row #class").html("<img class='left_padding' src='/static/img/c_icons/" + $("#" + ID).data("data-class") + ".gif' />");
    $("#player_info_popup .row #zone").html($("#" + ID).data("data-zone"));
  });
}
