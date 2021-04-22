$(document).ready(function() {
  console.log("ready");

  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');

  // creatures
  $('#get_creatures_button').on('click', function() {
    socket.emit('request_creatures_location', 'update');
  });

  socket.on('updated_creatures_location', function(data) {
    creatures_location(data);
  });

  // gameobject
  $('#get_gameobjects_button').on('click', function() {
    socket.emit('request_gameobjects_location', 'update');
  });

  socket.on('updated_gameobjects_location', function(data) {
    gameobjects_location(data);
  });

  // online
  socket.on('players_online', function(online) {
    $("#players_online").text(online + " online");
  });

  // player
  $('#get_players_button').on('click', function() {
    socket.emit('request_players_location', 'update');
  });

  socket.on('updated_players_location', function(data) {
    players_location(data);
  });

  // quest
  $('#get_quests_button').on('click', function() {
    socket.emit('request_quests_location', 'update');
  })

  socket.on('updated_quests_location', function(data) {
    quests_location(data);
  });

  // taxi
  $('#get_taxis_button').on('click', function() {
    socket.emit('request_taxis_location', 'update');
  });

  socket.on('updated_taxis_location', function(data) {
    taxis_location(data);
  });

  // worldport
  $('#get_worldports_button').on('click', function() {
    socket.emit('request_worldports_location', 'update');
  });

  socket.on('updated_worldports_location', function(data) {
    worldports_location(data);
  });

  // expansion
  $('#expansion').change(function(){
     socket.emit('request_expansion_change', $(this).val());
  });

  socket.on('updated_expansion', function(expansion) {
    $("#world").css({
      "background-image": "url('"+expansion['logofile']+"'), url('"+expansion['mapfile']+"')"
    });
  });
});
