const svgTemplate = `
  <svg width="7px" height="7px" class="spawn_point">
    <circle cx="4" cy="4" r="4" fill="lightgreen" stroke="black"></circle>
  </svg>
`;

function spawnSVGElements(positionData) {
  $("#world_objects").empty();

  for (const positionId in positionData) {
    const { left, top, mapx, mapy, id, class_name, name, x, y, z} = positionData[positionId];

    const svgElement = $(svgTemplate);
    svgElement.attr('id', id);
    svgElement.attr('data-classname', class_name);
    svgElement.attr('data-left', mapx);
    svgElement.attr('data-top', mapy);
    svgElement.attr('data-x', x);
    svgElement.attr('data-y', y);
    svgElement.attr('data-z', z);
    svgElement.attr('data-name', name);
    svgElement.addClass(class_name);
    svgElement.addClass('popups');
    svgElement.css({ left: `${left}px`, top: `${top}px`, position: 'absolute', cursor: 'auto' });
      
    $("#world_objects").append(svgElement);
  }
}
