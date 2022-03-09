function creatures_location(position) {
  $("#world").empty();

  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/group-icon.gif" class="creature_info" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';
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
    $("#" + i).data("data-image", position[i]["image"]);
  }

  // show info next to cursor
  $('#world').on('mouseover', ".creature_info", function() {
    ID = $(this).attr('id');
    $("#creature_info_popup .row .title #name").text($("#" + ID).data("data-name"));
    $("#creature_info_popup .row #spawnid").text("spawnid: " + $("#" + ID).data("data-id"));
    $("#creature_info_popup .row #display_id1").text("display_id1: " + $("#" + ID).data("data-image"));
    $("#creature_info_popup .row #posx").text("posx: " + $("#" + ID).data("data-posx"));
    $("#creature_info_popup .row #posy").text("posy: " + $("#" + ID).data("data-posy"));
    $("#creature_info_popup .row #posz").text("posz: " + $("#" + ID).data("data-posz"));
    $("#creature_info_popup .row #orientation").text("orientation: " + $("#" + ID).data("data-orientation"));

    var path = "/static/img/alpha/creature-display-" + $("#" + ID).data("data-image") + ".jpg";
    var image = $("<img class='image' src='" + path + "' />");
    $("#creature_info_popup #image").html(image);
  });
}
