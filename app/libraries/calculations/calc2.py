mapLeftPoint = 4267.765836313618
mapTopPoint = 4657.975130879346
mapWidth = 10568.022008253096
mapHeight = 19980.94603271984

magnification = 1
imageWidth = 345
imageHeight = 650
offset_x = 300
offset_y = 0
x = -8840.56
y = 489.7



def calculate_webb_position(x, y, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y):
    mapx = (1 - (y - mapLeftPoint)) / mapWidth
    mapy = (1 - (x - mapTopPoint)) / mapHeight

    mapx *= imageWidth
    mapy *= imageHeight
    
    left = (mapx * magnification) + offset_x
    top = (mapy * magnification) + offset_y 

    return left, top, mapx, mapy

def calculate_ingame_position(mapx, mapy, magnification, offset_x, offset_y):
    # den räknar på ursprongs positionen, inte på den förändrade positionen
    mapy = (top - offset_y) / magnification
    mapx = (left - offset_x) / magnification
    
    print(f"mapx: {mapx}, mapy: {mapy}")
    
    mapx /= imageWidth 
    mapy /= imageHeight 
    print(f"mapx: {mapx}, mapy: {mapy}")

    x = 1 + mapTopPoint - (mapHeight * mapy) 
    y = 1 + mapLeftPoint - (mapWidth * mapx)
    print(f"x: {x}, y: {y}")
    print(f"mapTopPoint: {mapTopPoint}, mapLeftPoint: {mapLeftPoint}")
    print(f"mapWidth: {mapWidth}, mapHeight: {mapHeight}")
    
    return x, y



left, top, mapx, mapy = calculate_webb_position(x, y, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

print("Webbposition")
print(f"left: {left}, top: {top}, mapx: {mapx}, mapy: {mapy}")
print()

top=439
left=430

x, y = calculate_ingame_position(left, top, magnification, offset_x, offset_y)
print("Ingameposition")
print(f"x: {x}, y: {y}")