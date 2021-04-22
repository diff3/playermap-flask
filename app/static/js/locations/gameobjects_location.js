function gameobjects_location(position) {
  $("#world").empty();
  
  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/group-icon.gif" class="gameobject_info" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';
    $("#world").append(locations);

    $("#" + i).css({
      'position': 'absolute',
      'left': position[i]['posx'],
      'top': position[i]['posy']
    });

    // save data to image tag
    $("#" + i).data("data-name", position[i]["name"]);
    $("#" + i).data("data-id", position[i]["id"]);
    $("#" + i).data("data-posx", position[i]["position_x"]);
    $("#" + i).data("data-posy", position[i]["position_y"]);
    $("#" + i).data("data-posz", position[i]["position_z"]);
    $("#" + i).data("data-orientation", position[i]["orientation"]);
  }

  $('#world').on('mouseover', ".gameobject_info", function() {
    ID = $(this).attr('id');
    $("#gameobject_info_popup .row .title #name").text($("#" + ID).data("data-name"));
    $("#gameobject_info_popup .row #spawnid").text("id: " + $("#" + ID).data("data-id"));
    $("#gameobject_info_popup .row #posx").text("posx: " + $("#" + ID).data("data-posx"));
    $("#gameobject_info_popup .row #posy").text("posy: " + $("#" + ID).data("data-posy"));
    $("#gameobject_info_popup .row #posz").text("posz: " + $("#" + ID).data("data-posz"));
    $("#gameobject_info_popup .row #orientation").text("orientation: " + $("#" + ID).data("data-orientation"));
  });
}
