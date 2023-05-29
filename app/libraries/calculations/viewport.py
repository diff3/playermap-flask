#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import json

__author__ = 'entropy'

def recalculate_objects_limited_by_viewport(original_dict, max_x, max_y, offset):
    min_x = min_y = 0

    min_x -= offset
    max_x += offset
    min_y -= offset
    max_y += offset 

    filtered_dict = {}

    for key, value in original_dict.items():
        if min_x <= value['left'] <= max_x and min_y <= value['top'] <= max_y:
            filtered_dict[key] = value

    return filtered_dict