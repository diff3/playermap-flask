#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# THIS CAN ZOON BE REMOVED


"""
Transform wow cords to web cords
"""

"""
map_0_offset_x=695
map_0_Offset_y=231
map_0_mod_x=0.032
map_0_mod_y=0.028
map_1_offset_x=145
map_1_offset_y=390
map_1_mod_x=0.03240
map_1_mod_y=0.030140

345x650

5080  ×  9576
"""

class Azeroth:
    def __init__(self, x, y):
        self.pos = {
            'x': 0,
            'y': 0
        }

        self.x = int(round(x))
        self.y = int(round(y))

    def maps(self, expansion, map):
        expansion['map_0_offset_x'] = 435
        expansion['map_0_offset_y'] = 151

        expansion['map_0_mod_x'] = 0.033
        expansion['map_0_mod_y'] = 0.028

        x = self.x
        y = self.y

        map = int(map)

        if map == 0:
            mapLeftPoint = 4267.765836313618
            mapTopPoint = 4657.975130879346 
            mapWidth = 10568.022008253096 
            mapHeight = 19980.94603271984 

            imageWidth = 345 
            imageHeight = 650

            mapx = (1 - (y - mapLeftPoint)) / mapWidth
            mapy = (1 - (x - mapTopPoint)) / mapHeight

            mapx *= imageWidth 
            mapy *= imageHeight

            mapx = round(mapx, 3)
            mapy = round(mapy, 3)

            self.pos['x'] = mapx
            self.pos['y'] = mapy

            # xpos = int(round(x * float(expansion['map_0_mod_x'])))
            # ypos = int(round(y * float(expansion['map_0_mod_y'])))

            # self.pos['x'] = float(expansion['map_0_offset_x']) - ypos
            # self.pos['y'] = float(expansion['map_0_offset_y']) - xpos
        elif map == 1:
            xpos = int(round(x * float(expansion['map_1_mod_x'])))
            ypos = int(round(y * float(expansion['map_1_mod_y'])))

            self.pos['x'] = float(expansion['map_1_offset_x']) - ypos
            self.pos['y'] = float(expansion['map_1_offset_y']) - xpos
        else:
            xpos = int(round(x * 0.032))
            ypos = int(round(y * 0.028))

            self.pos['x'] = 594 - ypos
            self.pos['y'] = 398 - xpos

        return self.pos



"""
--[[

MAP CO-ORDINATE CALCULATOR

If you update the maps (eg. different resolution, crop, etc.) you need to recalculate

1. Find two points on the map which are clearly identifiable in-game (eg. small islands).
   Preferably a fair distance from each other to reduce measurement or rounding errors.

    Eastern Kingdoms:

      I used:
        a. Brightwater Lake (the small island to the south)
        b. The entrance to the Sunken Temple.

    Kalimdor:

      I used:
        a. Darnassus, on the bridge facing the bank (or where it eventually is) at the bank end
        b. Outside Theramore, at the guard tower where the Sentry Point Guards are, on the road, next to the sign

2. Travel there in-game and find out their in-game coordinates (with the .gps command).

   Note that Y is east-west and X is north-south in the game.
   However in GIMP the X coordinate is given first and Y second, so you have to swap them around.
   So, in GIMP, if you mouse-over the spot to get the coordinates, you put them in as Y, X
   (Y being the first one as it is east/west, that is left/right)


--]]



function calc_coordinates (name, gameX1, gameY1, imageX1, imageY1,
                                 gameX2, gameY2, imageX2, imageY2,
                                 imageWidth, imageHeight)

  local gameDeltaX = math.abs (gameX2 - gameX1)
  local gameDeltaY = math.abs (gameY2 - gameY1)
  local imageDeltaX  = math.abs (imageX2 - imageX1)
  local imageDeltaY  = math.abs (imageY2 - imageY1)

  print ("**", name, "**")
  print ("Game Delta X =", gameDeltaX)
  print ("Game Delta Y =", gameDeltaY)
  print ()
  print ("Map  Delta X =", imageDeltaX)
  print ("Map  Delta Y =", imageDeltaY)
  print ()

  local Xratio = gameDeltaX / imageDeltaX
  local Yratio = gameDeltaY / imageDeltaY

  print ("X ratio =", Xratio)
  print ("Y ratio =", Yratio)

  print ()
  print (string.rep ("-", 40))
  print ("You need this stuff:")
  print ()

  -- left edge is how many pixel our reference point was from the left
  -- multiplied by the ratio factor, and adding in the reference point Y
  -- (either reference point will give the same result)

  local leftEdge = (imageY1 * Yratio) + gameY1
  local topEdge  = (imageX2 * Xratio) + gameX2
  print ("Left edge =", leftEdge, "(yards)")
  print ("Top  edge =", topEdge,  "(yards)")

  -- now calculate the width and height of the image in game units

  local mapWidth = imageWidth * Yratio
  local mapHeight = imageHeight * Xratio
  print ("Map width  =",  mapWidth, "(yards)")
  print ("Map height =", mapHeight, "(yards)")

  print ()
  print ("For PHP:")
  print ()

  print ("    //" .. string.rep ('-', 10) .. " " .. name .. " " .. string.rep ('-', 10))
  print ("    $mapLeftPoint = " .. leftEdge  .. ';  // game units (yards)')
  print ("    $mapTopPoint  = " .. topEdge   .. ';  //      "')
  print ("    $mapWidth     = " .. mapWidth  .. ';  //      "')
  print ("    $mapHeight    = " .. mapHeight .. ';  //      "')


end -- calc_coordinates

(name, gameX1, gameY1, imageX1, imageY1,
                                 gameX2, gameY2, imageX2, imageY2,
                                 imageWidth, imageHeight)

calc_coordinates ("Eastern Kingdoms",

                  -- Brightwater Lake (small island below larger one)
                  2484.981,   -- X (in-game) gameX1
                  24.705,     -- Y (in-game) gameY1
                  410,        -- map X (pixels) imageX1
                  803,        -- map Y (pixels) imageY1

                  -- Sunken Temple entrance (south)
                  -10473.484, -- X (in-game) gameX2
                  -3816.771,  -- Y (in-game) gameY2
                  2855,       -- map X (pixels) imageX1
                  1530,       -- map Y (pixels) imageY2

                  2000,       -- map width  (pixels)
                  3770)       -- map height (pixels)

print ()
print (string.rep ("*", 70))
print ()
calc_coordinates ("Kalimdor",

                  -- Darnassus on edge of bridge looking at bank
                  9945.852,     -- X (in-game)
                  2474.220,     -- Y (in-game)
                  278.4,        -- map X (pixels)
                  392.1,        -- map Y (pixels)

                  -- Theramore outside guard tower just up road (next to sign)
                  -3418.184,    -- X (in-game)
                  -4172.095,    -- Y (in-game)
                  2325.5,       -- map X (pixels)
                  1406.8,       -- map Y (pixels)

                  2000,         -- map width  (pixels)
                  3770)         -- map height (pixels)



"""