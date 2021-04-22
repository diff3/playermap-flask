#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform wow cords to web cords
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
        x = self.x
        y = self.y

        map = int(map)

        if map == 0:
            xpos = int(round(x * float(expansion['map_0_mod_x'])))
            ypos = int(round(y * float(expansion['map_0_mod_y'])))

            self.pos['x'] = float(expansion['map_0_offset_x']) - ypos
            self.pos['y'] = float(expansion['map_0_offset_y']) - xpos
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
