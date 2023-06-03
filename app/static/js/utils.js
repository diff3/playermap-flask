function copyToClipboard(text) {
    /** 
    * Copies the given text to the user's clipboard.
    * @param {string} text 
    */

    navigator.clipboard.writeText(text)
        .then(() => console.log("Copied to clipboard:", text))
        .catch(error => console.error("Error:", error));
}

function getImageData(elementId) {
    /**
    * Retrieves data for a specified image element 
    * and returns it as an object.
    *
    * @param {string} elementId
    * @return {object}
    */
    const currentImage = document.querySelector(elementId);
    const id = $("#id").val();
    const map = $("#map").val();
    const filterList = [["map", map]];
    const screenWidth = $(window).width();
    const screenHeight = $(window).height();

    // Calculate image offsets and dimensions
    const { offsetLeft, offsetTop, offsetHeight, offsetWidth } = currentImage;

    // Create data object using standardized variable names
    const data = {
        id,
        magnification,
        offsetLeft: offsetLeft,
        offsetTop: offsetTop,
        offsetHeight: offsetHeight,
        offsetWidth: offsetWidth,
        max_x: screenWidth,
        max_y: screenHeight,
        filters: filterList,
    };

    return data;
}

function redrawSpawnPoints(image) {
    /**
   * Redraws the spawn points on the given image by adjusting their position
   * based on the magnification factor and the image's offset.
   *
   * @param {Image} image - the image containing the spawn points to be redrawn
   * @return {void}
   */

    if (!image) return;

    const spawnPoints = document.getElementsByClassName("spawn_point");
    const offsetX = image.offsetLeft;
    const offsetY = image.offsetTop;

    for (var i = 0; i < spawnPoints.length; i++) {
        point = spawnPoints[i];
        point.style.left = `${(parseFloat(point.dataset.left) * magnification) + offsetX}px`;
        point.style.top = `${(parseFloat(point.dataset.top) * magnification) + offsetY}px`;
    }
}

function findImageInfo(event) {
    /**
    * Finds and returns information about an image based on a mouse event.
    *
    * @param {MouseEvent} event - The mouse event containing information about the image.
    * @return {Array} An array containing information about the current image, including its element, 
    *   offset from the left of the screen, offset from the top of the screen, and offset from the mouse 
    *   cursor.
    */

    var element = event.target;

    while (element) {
        if (element.classList && element.classList.contains("map-container")) {
            break;
        }

        element = element.parentNode;
    }

    if (!element) {
        return [false, false, false, false, false];
    }

    const currentImage = element.querySelector("img");
    const imageLeft = currentImage.offsetLeft;
    const imageTop = currentImage.offsetTop;
    var offsetX = event.offsetX;
    var offsetY = event.offsetY;

    if (event.target.nodeName == "svg") {
        offsetX = getPosition(event.target.style.left) - imageLeft;
        offsetY = getPosition(event.target.style.top) - imageTop;
    } else if (event.target.nodeName == "div") {
        return [false, false, false, false, false];
    }

    return [currentImage, imageLeft, imageTop, offsetX, offsetY];
}

function hidePopup() {
    /**
    * Hides the info popup by selecting the element with id 'info_popup' and hiding it. 
    * Removes the click event listener for that popup, sets its 'data-click_url' attribute to "no".
    *
    * @return {void} 
    */

    const popup = $('#info_popup');
    popup.hide();
    popup.attr('data-click_url', "no");
    $(document).off("click", '#info_popup');
}

function getActiveDivId() {
    /**
    * Returns the ID of the active image in the div with the given class name.
    *
    * @param {string} className - The class name of the map container div.
    * @return {string} The ID of the active image.
    */

    const activeImageId = $(".map-container.active img").attr("id");
    return activeImageId;
}

function removeObjectsFromWorld() {
    $(".world_objects").empty();
}

function addObjectsToWorld(data) {
    $(".map-container.active .world_objects").append(data);
}


function switchActiveMap() {
    var selectedValue = $('select#map').val();

    var imageElement = $(".map-container.active img");
    var imageOffset = imageElement.offset();
    var imageTop = imageOffset.top;
    var imageLeft = imageOffset.left;

    if (selectedValue == 1) {
      $("#map-container-Eastern_Kingdoms").addClass("hidden");
      $("#map-container-Eastern_Kingdoms").removeClass("active");
      $("#map-container-Kalimdor").removeClass("hidden");
      $("#map-container-Kalimdor").addClass("active");
    } 
    else {
      $("#map-container-Eastern_Kingdoms").addClass("active");
      $("#map-container-Eastern_Kingdoms").removeClass("hidden");
      $("#map-container-Kalimdor").addClass("hidden"); 
      $("#map-container-Kalimdor").removeClass("active");
    }

    imageElement.data("top", imageTop);
  imageElement.data("left", imageLeft);

}