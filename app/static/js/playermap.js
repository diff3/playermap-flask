var socket;
var saved_button
var popup = $('#info_popup');
var draggable = 'false'
var filterList = [];
var clientID;

window.addEventListener('beforeunload', function () {
  console.log("Disconnecting from server");
  socket.emit('disconnect_event', clientId);
});

$(document).ready(function () {
  switchActiveMap();
  socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');
  console.log("Page Loaded, with no errors");

  socket.on('connected', function (data) {
    console.log("Connected to server");
    clientId = data
  });

  socket.on('receaving_update_from_server', function (data) {
    spawnData = data['spawnData'];
    elements = data['spawnSVGElements'];
    $("#spawned").text(spawnData['spawned']);
    $("#numSpawns").text("/" + spawnData['numSpawns'] + " spawned ");
    spawnSVGElements(elements);
  });

  // online
  socket.on('players_online', function (online) {
    $("#player_online").text(online + " online");
  });

  // player
  $('#get_players_button').on('click', function () {
    socket.emit('request_players_location', 'update');
  });

  socket.on('updated_players_location', function (data) {
    players_location(data);
  });

  /* MOUSE EVENTS */

  $(document).on('mouseenter', ".popups", function (event) {
    data = {
      'id': $(this).attr('id'),
      'class_name': $(this).attr('data-classname'),
      'popup': 'mouseover',
      'mouseX': event.pageX,
      'mouseY': event.pageY
    }

    socket.emit('mouse_enter_info', data);
  });

  $(document).on('mouseleave', ".popups", function (event) {
    hidePopup()
  });

  /* POPUP EVENTS */

  socket.on('show_info_popups', function (data) {
    mouseX = data['requested_data']['mouseX']
    mouseY = data['requested_data']['mouseY']

    $("#info_popup #title").text(data['requested_data']['name']);
    $("#info_popup #subTitle").html(data['requested_data']['subTitle']);
    notes = data['requested_data']['notes'];
    
    // replace quest tags
    if (data['requested_data']['url'].indexOf("action=show_quest") !== -1)
    {
      notes = replaceQuestTags(notes);
    }
    $("#info_popup #notes").html(notes);

    var offsetX = 10; // Adjust the horizontal offset
    var offsetY = 10; // Adjust the vertical offset

    // Calculate the maximum allowed positions
    var maxLeft = $(window).width() - $("#info_popup").outerWidth() - offsetX;
    var maxTop = $(window).height() - $("#info_popup").outerHeight() - offsetY;

    // Adjust the position if it exceeds the maximum allowed positions
    var left = Math.min(mouseX + offsetX, maxLeft);
    var top = Math.min(mouseY + offsetY, maxTop);

    // Check if the popup is too close to the right side of the screen
    if (left > maxLeft - offsetX) {
      left = mouseX - offsetX - popup.outerWidth();
    }

    // Check if the popup is too close to the bottom of the screen
    if (top > maxTop - offsetY) {
      top = mouseY - offsetY - popup.outerHeight();
    }

    $("#info_popup").css({
      top: top + "px",
      left: left + 'px'
    });

    $('#info_popup').attr('data-click_url', data['requested_data']['url']);
    $('#info_popup').show();
  });

  $(document).on('click', ".popups", function (event) {
    var x = parseFloat($(this).attr('data-x'));
    var y = parseFloat($(this).attr('data-y'));
    var z = parseFloat($(this).attr('data-z'));
    var title = $(this).attr('data-name');
    var class_name = $(this).attr('data-classname');
    var url = $("#info_popup").attr('data-click_url');
    var textToCopy = ""
    const mapId = $("#map").val();
    
    if (event.metaKey && event.shiftKey) {
      textToCopy = title;
    }
    else if (event.altKey && event.metaKey) {
      if ($(this).attr('data-display_id')) {
        var display_id = $(this).attr('data-display_id');
        textToCopy = display_id;
      } 
      else {
        console.log("No display id found")
      }
    }
    else if (event.altKey) {
      textToCopy = `.port ${x} ${y} ${z} ${mapId}`;;
    }
    else if (event.metaKey && class_name == "worldport") {
      textToCopy = `.tel ${title.toLowerCase()}`;
    } else if (event.shiftKey && url != "no" && url != undefined) {
      window.open(url, '_blank');
    } else if (event.shiftKey && class_name == "taxi") {
      url = "https://db.thealphaproject.eu/?action=show_table&table=TaxiNodes&database=alpha_dbc";
      window.open(url, '_blank');
    }

    if (textToCopy.length > 0) {
      copyToClipboard(textToCopy);
    }
  });

  $(document).on("click", function (event) {
    // button.addEventListener("click", function(event) {
      event.preventDefault();
      activeID = getActiveDivId()
      data = getImageData(`#${activeID}`);


    if (event.altKey) {
      var offsetX = event.offsetX;
      var offsetY = event.offsetY;

      console.log("offsetX: ", offsetX, " offsetY: ", offsetY);

      const currentImage = document.querySelector(`#${activeID}`);

      // console.log("data: ", data);      


      const mapWidth = currentImage.dataset.mapwidth
      const mapHeight = currentImage.dataset.mapheight
      const mapLeft = currentImage.dataset.mapleft
      const mapTop = currentImage.dataset.maptop

      const mapId = $("#map").val();

      const imageWidth = currentImage.dataset.width
      const imageHeight = currentImage.dataset.height
      console.log("mapWidth: ", mapWidth + " mapHeight: " + mapHeight + " mapLeft: " + mapLeft + " mapTop: " + mapTop + " imageWidth: " + imageWidth + " imageHeight: " + imageHeight); ;

      // how far through image is mouse assuming no magnification
      // (image may start offscreen)
      const mouseX = offsetX / magnification
      const mouseY = offsetY / magnification

      // distance through map we are (from 0 to 1)
      const xOffset = mouseX / imageWidth
      const yOffset = mouseY / imageHeight

      const x = mapLeft - mapWidth * xOffset
      const y = mapTop - mapHeight * yOffset

      copyToClipboard(".port " + y + " " + x + " " + 300 + " " + mapId);
    }
  });

  /* SEARCH BAR FUNCTIONS */

  $("#add-button").click(function () {
    var selectedFilter = $("#filters").val();
    var query = $("#query-input").val();

    if (selectedFilter || query) {
      filterList.push([selectedFilter, query]);
      $("#filter-items").append("<span class='filter-item' data-filter='" + selectedFilter + "' data-query='" + query + "'>- " + selectedFilter + ": " + query + "</span>");
      $("#query-input").val("");
    }
  });

  $("#filter-items").on("click", ".filter-item", function () {
    var selectedFilter = $(this).data("filter");
    var query = $(this).data("query");

    filterList = filterList.filter(function (filter) {

      return !(filter[0] === selectedFilter && filter[1] === query);
    });

    $(this).remove();
  });

  $("#search-button").click(function () {
    var active_id = getActiveDivId(".map-container");
    console.log("active_id: ", active_id);
    data = getImageData(`#${active_id}`)

    console.log(data);
    socket.emit('request_server_update', data);
  });

  $("#clear-button").click(function () {
    filterList = [];
    $("#filter-items").empty();
    removeObjectsFromWorld();
    $("#spawned").text("");
    $("#numSpawns").empty();
  });

  // Get references to the necessary elements
  const toggleButton = document.getElementById('toggle-advanced');
  const advancedContainer = document.getElementById('advanced-features');

  // Add a click event listener to the toggle button
  toggleButton.addEventListener('click', () => {
    // Toggle the visibility of the advanced container by adding/removing the 'hidden' class
    if ($("#toggle-advanced").text() == '[ + ]') {
      $("#toggle-advanced").text('[ - ]');
    } else {
      $("#toggle-advanced").text('[ + ]');
    }
    advancedContainer.classList.toggle('hidden');
  });

  $("#map").on("change", function(event) {
    switchActiveMap();



    // Rest of your code handling the select change event
  });
});
