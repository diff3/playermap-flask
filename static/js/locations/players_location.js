function players_location(position) {
  $("#world").empty();

  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/' + position[i]["faction"] + '.gif" class="player_info icon" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>'
    $("#world").append(locations);

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
