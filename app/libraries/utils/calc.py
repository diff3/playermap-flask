def calc_coordinates(name, gameX1, gameY1, imageX1, imageY1, gameX2, gameY2, imageX2, imageY2, imageWidth, imageHeight):
    gameDeltaX = abs(gameX2 - gameX1)
    gameDeltaY = abs(gameY2 - gameY1)
    imageDeltaX = abs(imageX2 - imageX1)
    imageDeltaY = abs(imageY2 - imageY1)

    print(name)
    print(f"Game Delta Y = {gameDeltaY}")
    print(f"Game Delta X = {gameDeltaX}")
    print()
    print(f"Map Delta Y = {imageDeltaY}")
    print(f"Map Delta X = {imageDeltaX}")
    Xratio = gameDeltaX / imageDeltaX
    Yratio = gameDeltaY / imageDeltaY

    print()
    print(f"X ratio = {Xratio}")
    print(f"Y ratio = {Yratio}")

    print()
    print("You need this stuff:")
    print()

    leftEdge = (imageY1 * Yratio) + gameY1
    topEdge = (imageX2 * Xratio) + gameX2
    print(f"Left edge = {leftEdge} (yards)")
    print(f"Top  edge = {topEdge} (yards)")

    mapWidth = imageWidth * Yratio
    mapHeight = imageHeight * Xratio
    print()
    print(f"Map width  = {mapWidth} (yards)")
    print(f"Map height = {mapHeight} (yards)")

    print(f"    {name}")
    print(f"    mapLeftPoint = {leftEdge} (yards)")
    print(f"    mapTopPoint  = {topEdge} ")
    print(f"    mapWidth     = {mapWidth} ")
    print(f"    mapHeight    = {mapHeight} ")


calc_coordinates("Eastern Kingdoms",
                    #- Brightwater Lake (small island below larger one)
                  2484.981,   #- X (in-game)
                  24.705,     #- Y (in-game)
                  410,        #- map X (pixels)
                  803,        #- map Y (pixels)

                  #- Sunken Temple entrance (south)
                  -10473.484, #- X (in-game)
                  -3816.771,  #- Y (in-game)
                  2855,       #- map X (pixels)
                  1530,       #- map Y (pixels)

                  2000,       #- map width  (pixels)
                  3770)       #- map height (pixels)

calc_coordinates("Kalimdor",
                 #- Darnassus on edge of bridge looking at bank
                  9945.852,     #- X (in-game)
                  2474.220,     #- Y (in-game)
                  278.4,        #- map X (pixels)
                  392.1,        #- map Y (pixels)

                  #- Theramore outside guard tower just up road (next to sign)
                  -3418.184,    #- X (in-game)
                  -4172.095,    #- Y (in-game)
                  2325.5,       #- map X (pixels)
                  1406.8,       #- map Y (pixels)

                  2000,         #- map width  (pixels)
                  3770)         #- map height (pixels)