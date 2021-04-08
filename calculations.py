#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Transform wow cords to web cords
"""


class Azeroth_053:
    def __init__(self, x, y):
        self.pos = {
            'x': 0,
            'y': 0
        }

        self.x = int(round(x))
        self.y = int(round(y))

    def maps(self, map):
        x = self.x
        y = self.y

        map = int(map)

        xpos = int(round(x * 0.032))
        ypos = int(round(y * 0.028))

        if map == 0:
            self.pos['x'] = 695 - ypos
            self.pos['y'] = 231 - xpos
        elif map == 1:
            xpos = int(round(x * 0.03240))
            ypos = int(round(y * 0.030140))

            self.pos['x'] = 145 - ypos
            self.pos['y'] = 390 - xpos
        else:
            self.pos['x'] = 594 - ypos
            self.pos['y'] = 398 - xpos

        return self.pos
