function quests_location(position) {
  $("#world").empty();

  for (var i = 0; i < position.length; i++) {
    var locations = '<img src="/static/img/map/group-icon.gif" class="quest_info" id="' + i + '" onmouseover="divShow(event, \'' + position[i]['show'] + '\')" onmouseout="divHide(event,\'' + position[i]['show'] + '\')" \>';
    $("#world").append(locations);

    $("#" + i).css({
      'position': 'absolute',
      'left': position[i]['posx'],
      'top': position[i]['posy']
    });

    // save data to image tag
    $("#" + i).data("data-name", position[i]["name"]);
    $("#" + i).data("data-title", position[i]["title"]);
    $("#" + i).data("data-zone", position[i]["zone"]);
    $("#" + i).data("data-posx", position[i]["posx"]);
    $("#" + i).data("data-posy", position[i]["posy"]);
    $("#" + i).data("data-details", position[i]["details"]);
    $("#" + i).data("data-objectives", position[i]["objectives"]);
    $("#" + i).data("data-prevquestid", position[i]["prevquestid"]);
    $("#" + i).data("data-nextquestid", position[i]["nextquestid"]);
  }

  // show info next to cursor
  $('#world').on('mouseover', ".quest_info", function() {
    ID = $(this).attr('id');
    $("#quest_info_popup .row .title #name").text($("#" + ID).data("data-name"));
    $("#quest_info_popup .row #quest_title").text($("#" + ID).data("data-title"));
    $("#quest_info_popup .row #posx").text("posx: " + $("#" + ID).data("data-posx"));
    $("#quest_info_popup .row #posy").text("posy: " + $("#" + ID).data("data-posy"));
    $("#quest_info_popup .row #details").text($("#" + ID).data("data-details"));
    $("#quest_info_popup .row #objectives").text($("#" + ID).data("data-objectives"));
  });
}
