// Show info next to cursor

function divShow(event, id) {
  var div = document.getElementById(id);

  var height = event.pageY - $(div).height() - 10;
  var width = event.pageX + $(div).width() + 10;

  var offsetY = 0;
  var offsetX = 0;

  if (0 > height) {
    offsetY = Number($(div).height() + 30);
  }

  if ($(window).width() < width) {
    offsetX = Number($(div).width() + 10);
  }

  div.style.left = event.pageX - offsetX + "px";
  div.style.top = height + offsetY + "px";

  $("#" + id).show();
}

// hide it
function divHide(event, id) {
  var div = document.getElementById(id);
  $("#" + id).hide();
}
