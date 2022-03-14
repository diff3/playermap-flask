$(document).ready(function() {
  console.log("ready");
  var socket = io.connect('http://' + document.domain + ':' + location.port + '/playermap');

  function inside(point, vs) {
    // ray-casting algorithm based on
    // https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html/pnpoly.html
    
    var x = point[0], y = point[1];
    
    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];
        
        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }
    
    return inside;
};

  $('#world').click(function(e) {
    var offset = $(this).offset();
    var posX = e.pageX - offset.left;
    var posY = e.pageY - offset.top;

    console.log("posX: " + posX  + " posY:" + posY);

    // map Dun morogh zone
    // posX: 663 posY:376
    // posX: 754 posY:372
    // posX: 762 posY:418
    // posX: 659 posY:450
    // posX: 700 posY:396
  
    var polygon = [ [ 663, 376 ], [ 754, 372 ], [ 762, 418 ], [718, 426], [ 659, 450 ] ];
    if (inside([ posX, posY ], polygon)) {
        console.log("Mouse inside, Dun Morogh");
        socket.emit('request_expansion_change', "dun_morogh");
    }
   });

   $('#world').click(function(e) {
    //	var offset = $(this).offset();
   // 	var posX = e.pageX - offset.left;
   // 	var posY = e.pageY - offset.top;
	var posX = e.pageX;
	var posY = e.pageY;

	var polygon = [ [ posX - 10, posY - 10], [posX + 10, posY - 10], [posX + 10, posY + 10], [posX - 10, posY + 10] ]; 
	   
	$('.quest_info').each(function(){
           x = $(this).offset().left;		
           y = $(this).offset().top;		

	   if (inside([x, y], polygon)) {
               console.log("Quest name: " + $(this).data("data-title"));
           }
	});
   }); 

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
    $('#expansion').val(expansion['name']);

    $("#world").css({
      "background-image": "url('"+expansion['logofile']+"'), url('"+expansion['mapfile']+"')"
    });
  });
});
