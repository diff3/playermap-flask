#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

__author__ = 'entropy'


def calculate_data_reduction_offset(magnification):
    if magnification >= 5:
        reduction_offset = 10 - (5 + magnification / 5) 
        reduction_offset = max(reduction_offset, 1)
    else:
        reduction_offset = 7

    return int(reduction_offset)

def recalculate(records, map_left_point, map_top_point, map_width, map_height, image_width, image_height, magnification, offset_x, offset_y):

    recalculated_records = records.copy()

    for key, record in records.items():
        left, top, mapx, mapy = recalculate_position(record, map_left_point, map_top_point, map_width, map_height, image_width, image_height, magnification, offset_x, offset_y)

        recalculated_records[key]['mapx'] = mapx
        recalculated_records[key]['mapy'] = mapy
        recalculated_records[key]['left'] = left
        recalculated_records[key]['top'] = top

    return recalculated_records

def recalculate_position(record, map_left_point, map_top_point, map_width, map_height, image_width, image_height, magnification, offset_x, offset_y):
    x = record['x']
    y = record['y']

    """mapx = (1 - (y - map_top_point)) / map_width
    mapy = (1 - (x - map_left_point)) / map_height

    mapx *= image_width
    mapy *= image_height
    
    left = (mapx * magnification) + offset_x
    top = (mapy * magnification) + offset_y """
    
    mapx = (1 - (y - map_left_point)) / map_width
    mapy = (1 - (x - map_top_point)) / map_height

    mapx *= image_width
    mapy *= image_height

    left = (mapx * magnification) + offset_x
    top = (mapy * magnification) + offset_y

    mapx = round(mapx, 3)
    mapy = round(mapy, 3)

    return left, top, mapx, mapy

def reduce_data(spawns_creatures_viewport, offset):
    spawns_creatures_reduced = {}
    for id in spawns_creatures_viewport:
        if id % offset == 0:
            spawns_creatures_reduced[id] = spawns_creatures_viewport[id]

    return spawns_creatures_reduced