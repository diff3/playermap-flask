// MAGNIFIER - written by X'Genesis Qhulut in September 2022

// global variables

// Note: 10% webp quality on small map, 91% on big map
var wheelTimeout;
var startDragX = 0;     // mouse-down location (start of drag)
var startDragY = 0;     //   "
var dragging = false;   // are we dragging?
var magnification = 1   // initial magnification
const zoomFactor = 1.1  // amount to change when you zoom
const maxZoom = 40      // maximum magnification
const minZoom = 1     // minimum magnification
const spawnHighlightMaxDistance = 38  // if spawns fall within this number of pixels, show the highlighter
const mediumZoom = 8;
const largeZoom = 16;
var currentZoom = 'mediumZoom'

function hideHelp ()
{

  // hide all these things
 ;[
  'spawn-map-help-box',
  'spawn-map-highlighter',
  'map-arrow-right',
  'map-arrow-left',
  ].forEach(id =>
    {
    var element = document.getElementById (id)
    if (element)
      {
      element.style.display = 'none';
      }
   }) // end of foreach


  // lower opacity of all these things
  ;[
  'shortcut-icon',
  ].forEach(id =>
    {
    var element = document.getElementById (id)
    if (element)
      {
      element.style.opacity = '0.4';
      }
   }) // end of foreach


} // end of hideHelp


// mouse down (start of drag) - remember starting point
function onMouseDownMapContainer (event)
  {
  event.preventDefault();
  var [ currentImage, imageLeft, imageTop, offsetX, offsetY ] = findImageInfo (event)
  
  if (!currentImage)
    return

  startDragX  = offsetX
  startDragY  = offsetY
  dragging = true
  event.target.style.cursor = "grabbing"
  } // end of onMouseDownMapContainer


// redraw spawn points based on their original position multiplied by the magnification factor
function redrawSpawnPoints (currentImage)
  {
    if (currentImage == null) {
      return
    }


    const spawnPoints = document.getElementsByClassName("spawn_point")
    const offsetX = currentImage.offsetLeft
    const offsetY = currentImage.offsetTop

    // console.log("offsetX: ", offsetX, "offsetY: ", offsetY)

  for (var i = 0; i < spawnPoints.length; i++)
    {
    spawnPoints[i].style.left = ((spawnPoints[i].dataset.left * magnification) + offsetX) + "px";
    spawnPoints[i].style.top  = ((spawnPoints[i].dataset.top * magnification)  + offsetY) + "px";
    } // end of for

  } // end of redrawSpawnPoints

  // mouse up (end of drag)
function onMouseUpMapContainer (event)
{
  
dragging = false
event.target.style.cursor = "unset"

var element = event.target;
element = element.parentNode;

const currentImage = element.querySelector("img")
var screenWidth = $(window).width();
var screenHeight = $(window).height();

data = {
  'id': saved_button,
  'magnification': magnification,
  'offsetLeft':  currentImage.style.left,
  'offsetTop':  currentImage.style.top,
  'offsetHeight': currentImage.style.height,
  'offsetWidth': currentImage.style.width,
  'max_x': screenWidth,
  'max_y': screenHeight
}
socket.emit('request_server_update', data);

$('#info_popup').hide();
$(document).off("click", '#info_popup');
$('#info_popup').attr('data-click_url', "no");

// redrawSpawnPoints (currentImage) 
} // end of onMouseUpMapContainer

function findImageInfo (event)
  {
  var element = event.target;
  while (true)
    {
    if (!element)
      return [ false, false, false, false, false ]

    if (element.classList && element.classList.contains ("map-container"))
      break

    element = element.parentNode;
    } // end of while we haven't found the map container

  const currentImage = element.querySelector("img")

  // where does the image start? (it may be offscreen)
//  var imageLeft = getPosition (currentImage.style.left)
  var imageLeft = currentImage.offsetLeft;
  var imageTop  = currentImage.offsetTop;

  var offsetX = event.offsetX;
  var offsetY = event.offsetY;

  // if mouse over a spawn point, find where the spawn point is
  if (event.target.nodeName == 'circle')
    {
    offsetX = getPosition (event.target.parentNode.style.left) - imageLeft
    offsetY = getPosition (event.target.parentNode.style.top)  - imageTop
    } // end of if over a spawn point
  else if (event.target.nodeName == 'svg')
    {
    offsetX = getPosition (event.target.style.left) - imageLeft
    offsetY = getPosition (event.target.style.top)  - imageTop
    } // end of if over a SVG point
  else if (event.target.nodeName == 'DIV')
    {
    return [ false, false, false, false, false ]
    } // end of if over a DIV point

  return [ currentImage, imageLeft, imageTop, offsetX, offsetY ]

  }   // end of findImage

function onMouseMoveMapContainer (event)
  {
  event.preventDefault();

  if (!dragging)
    return;

  hideHelp ()

  // if button is now up they must have released it outside the container
  if (event.buttons == 0)
    {
    onMouseUpMapContainer (event)
    return
    }

  const [ currentImage, imageLeft, imageTop, offsetX, offsetY ] = findImageInfo (event)
  if (!currentImage)
    return

  // difference between where we started and where we are now
  const diffX = startDragX - offsetX;
  const diffY = startDragY - offsetY;

  // move it by the difference between where we started and where we are now
  currentImage.style.left = (imageLeft - diffX) + "px"
  currentImage.style.top  = (imageTop  - diffY) + "px"

  redrawSpawnPoints (currentImage)

  } // end of onMouseMoveMapContainer

function onMouseWheelMapContainer (event)
{
  $("#world_objects").empty();
  $('#info_popup').hide();
  clearTimeout(wheelTimeout);
  event.preventDefault();

  
  const [ currentImage, imageLeft, imageTop, offsetX, offsetY ] = findImageInfo (event)

  if (!currentImage)
    return

  // hide help box
  hideHelp ()

  // how far through image is mouse assuming no magnification
  // (image may start offscreen)
  const mouseX = offsetX / magnification
  const mouseY = offsetY / magnification

  // how far cursor is through container
  const cursorX = offsetX + imageLeft
  const cursorY = offsetY + imageTop

  magnification *= event.deltaY > 0 ? 1/zoomFactor : zoomFactor

  // constrain to 0.5 to 30 magnification
  magnification = Math.min (magnification, maxZoom)
  magnification = Math.max (magnification, minZoom)

  // adjust image size
  currentImage.style.width  = (currentImage.dataset.width  * magnification) + "px"
  currentImage.style.height = (currentImage.dataset.height * magnification) + "px"

  // move image so that the place under the cursor is still under it
  currentImage.style.left = - mouseX * magnification +  cursorX + "px"
  currentImage.style.top  = - mouseY * magnification +  cursorY + "px"


 // load a medium def map if needed

  const baseName = currentImage.dataset.basename
  const extension = currentImage.dataset.extension

  // adjust map image file name depending on amount of magnification
  // we downgrade when zooming out because the browser struggles to resize very large files down very small

  /*
  if (magnification < mediumZoom && currentZoom != 'small')
    {
//    console.log (`switching to small map`)
    currentImage.src = baseName + extension
    currentZoom = 'small'
    }
  else
*/

  if (magnification >= mediumZoom && magnification < largeZoom && currentZoom != 'medium')
    {
//    console.log ('switching to medium map')
    currentImage.src = baseName + '_big' + extension
    currentZoom = 'medium'
    }
  else if (magnification >= largeZoom && currentZoom != 'large')
    {
//    console.log ('switching to large map')
    currentImage.src = baseName + '_bigger' + extension
    currentZoom = 'large'
    }


    wheelTimeout = setTimeout(function() {
//  console.log (`magnification = ${magnification}, file name = ${currentImage.src}`)
   // redrawSpawnPoints (currentImage)
   var screenWidth = $(window).width();
   var screenHeight = $(window).height();

   data = {
    'id': saved_button,
    'magnification': magnification,
    'offsetLeft':  currentImage.style.left,
    'offsetTop':  currentImage.style.top,
    'offsetHeight': currentImage.style.height,
    'offsetWidth': currentImage.style.width,
    'max_x': screenWidth,
    'max_y': screenHeight
  }

  socket.emit('request_server_update', data);

   // redrawSpawnPoints (currentImage) 
  }, 500); // Adjust the timeout duration as needed
} // end of onMouseWheelMapContainer

function getPosition (which)
  {
  return parseFloat (which.split ("px") [0])
  } // end of getPosition