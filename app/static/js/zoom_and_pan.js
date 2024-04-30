// MAGNIFIER - written by X'Genesis Qhulut in September 2022

// global variables

// Note: 10% webp quality on small map, 91% on big map
var wheelTimeout;
var startDragX = 0;     // mouse-down location (start of drag)
var startDragY = 0;     //   "
var isDragging = false;   // are we dragging?
var magnification = 1   // initial magnification
const zoomFactor = 1.1  // amount to change when you zoom
const maxZoom = 40      // maximum magnification
const minZoom = 1     // minimum magnification
const spawnHighlightMaxDistance = 38  // if spawns fall within this number of pixels, show the highlighter
const mediumZoom = 8;
const largeZoom = 16;
var currentZoom = 'mediumZoom'

function hideHelp() {

  // hide all these things
  ;[
    'spawn-map-help-box',
    'spawn-map-highlighter',
    'map-arrow-right',
    'map-arrow-left',
  ].forEach(id => {
    var element = document.getElementById(id)
    if (element) {
      element.style.display = 'none';
    }
  }) // end of foreach


    // lower opacity of all these things
    ;[
      'shortcut-icon',
    ].forEach(id => {
      var element = document.getElementById(id)
      if (element) {
        element.style.opacity = '0.4';
      }
    }) // end of foreach


} // end of hideHelp

function onMouseDownMapContainer(event) {
  /**
  * Prevents the default behavior of the event and finds the image info of the current image.
  *
  * @param {Object} event - The event object.
  * @return {undefined}
  */

  event.preventDefault();
  const [currentImage, imageLeft, imageTop, offsetX, offsetY] = findImageInfo(event);

if (!currentImage || event.target.id.search("map-container active") > 0) {
  console.log("onMouseDownMapContainer: not active")
  return;
}

  hidePopup();
  startDragX = offsetX;
  startDragY = offsetY;
  isDragging = true;
  event.target.style.cursor = "grabbing";
}


function onMouseUpMapContainer(event) {
  /**
  * Handles the onMouseUp event on the map container.
  *
  * @param {Event} event - the mouseup event object
  * @return {void} This function does not return anything.
  */

  isDragging = false
  event.target.style.cursor = "auto"
}

function onMouseMoveMapContainer(event) {
  /**
  * Handles mouse move events on the map container.
  *
  * @param {event} event - The mouse move event.
  * @return {void}
  */

  event.preventDefault();

  if (!isDragging) {
    return;
  }

  const [currentImage, imageLeft, imageTop, offsetX, offsetY] = findImageInfo(event);

  if (!currentImage) {
    return;
  }
  
  hideHelp();

  const diffX = event.movementX;
  const diffY = event.movementY;

  currentImage.style.left = `${imageLeft + diffX}px`;
  currentImage.style.top = `${imageTop + diffY}px`;

  redrawSpawnPoints(currentImage); 
}

function onMouseWheelMapContainer(event) {
  event.preventDefault();
  clearTimeout(wheelTimeout);

  const [currentImage, imageLeft, imageTop, offsetX, offsetY] = findImageInfo(event)
  const isInfoPopupVisible = $('#info_popup').is(':visible');

  // If info_popup is visible, do not proceed with image movement
  if (!currentImage || event.target.id.search("map-container active") > 0) {
    console.log("onMouseWheelMapContainern: ot active")
      return;
    }

  // hide help box
  hideHelp();
  hidePopup();
  removeObjectsFromWorld()

  // how far through image is mouse assuming no magnification
  // (image may start offscreen)
  const mouseX = offsetX / magnification
  const mouseY = offsetY / magnification

  // how far cursor is through container
  const cursorX = offsetX + imageLeft
  const cursorY = offsetY + imageTop

  magnification *= event.deltaY > 0 ? 1 / zoomFactor : zoomFactor

  // constrain to 0.5 to 30 magnification
  magnification = Math.min(magnification, maxZoom)
  magnification = Math.max(magnification, minZoom)

  // adjust image size
  currentImage.style.width = (currentImage.dataset.width * magnification) + "px"
  currentImage.style.height = (currentImage.dataset.height * magnification) + "px"

  // move image so that the place under the cursor is still under it
  currentImage.style.left = - mouseX * magnification + cursorX + "px"
  currentImage.style.top = - mouseY * magnification + cursorY + "px"


  // load a medium def map if needed

  const baseName = currentImage.dataset.basename
  const extension = currentImage.dataset.extension

  wheelTimeout = setTimeout(function () {
    data = getImageData(`#${event.target.id}`)
    socket.emit('request_server_update', data);
  }, 500);
}

function getPosition(which) {
  return parseFloat(which.split("px")[0])
} // end of getPosition