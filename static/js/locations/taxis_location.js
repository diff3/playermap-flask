function taxis_location(position) {
  $("#world").empty();

  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/group-icon.gif" class="taxi_info" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';
    $("#world").append(locations);

    $("#" + i).css({
      'position': 'absolute',
      'left': position[i]['posx'],
      'top': position[i]['posy']
    });

    // save data to image tag
    $("#" + i).data("data-name", position[i]["name"]);
    $("#" + i).data("data-spawnid", position[i]["id"]);
    $("#" + i).data("data-posx", position[i]["position_x"]);
    $("#" + i).data("data-posy", position[i]["position_y"]);
  }

  // show info next to cursor
  $('#world').on('mouseover', ".taxi_info", function() {
    ID = $(this).attr('id');
    $("#taxi_info_popup .row .title #name").text($("#" + ID).data("data-name"));
    $("#taxi_info_popup .row #spawnid").text("id: " + $("#" + ID).data("data-spawnid"));
    $("#taxi_info_popup .row #posx").text("posx: " + $("#" + ID).data("data-posx"));
    $("#taxi_info_popup .row #posy").text("posy: " + $("#" + ID).data("data-posy"));
  });
}
