#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import json

__author__ = 'entropy'



# open recalculated_spawns.json file to a dict

# with open('recalculated_spawns.json') as file:
    # Load the JSON data into a dictionary
  #  original_dict = json.load(file)

'''
original_dict = {
    1: {'id': 1, 'entry': 2843, 'x': -14467.8, 'y': 468.374, 'z': 15.1064, 'orientation': 0.139626, 'name': 'Jutak', 'display_id': 4481, 'class_name': 'creature', 'mapx': 124.066, 'mapy': 622.213, 'left': 424.06628056832847, 'top': 622.2129730350538},
    3: {'id': 3, 'entry': 2499, 'x': -14355.9, 'y': 433.399, 'z': 7.55289, 'orientation': 1.79769, 'name': 'Markel Smythe', 'display_id': 242, 'class_name': 'creature', 'mapx': 125.208, 'mapy': 618.573, 'left': 425.2080623502529, 'top': 618.5727550052922}
    # Add more entries if necessary
}
'''

def recalculate_objects_limited_by_viewport(original_dict, max_x, max_y):

    min_x = -750  # Adjust as per your requirements
    max_x += 750  # Adjust as per your requirements
    min_y = -750  # Adjust as per your requirements
    max_y += 750  # Adjust as per your requirements

    filtered_dict = {}

    for key, value in original_dict.items():
        if min_x <= value['left'] <= max_x and min_y <= value['top'] <= max_y:
            filtered_dict[key] = value

    return filtered_dict
#    print(filtered_dict)
