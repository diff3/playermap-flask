#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.calculations import Azeroth_053
from database.mysqld import Mysqld

allience = [1, 3, 4, 7]


class Dbc:
    def __init__(self):
        pass

    def get_taxi_nodes(self, database):
        results = Mysqld(database).query(
            """SELECT * FROM TaxiNodes
            WHERE ContinentID = '0' OR ContinentID = '1'""")

        lst = list()

        for record in results:
            pos = Azeroth_053(record[2], record[3]).maps(record[1])

            lst.append({
                'id': record[0],
                'position_x': record[2],
                'position_y': record[3],
                'map': record[1],
                'name': record[5],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "information"

            })

        return lst


class Realm:
    def __init__(self):
        pass

    def get_player_position(self, database):
        results = Mysqld(database).query(
            """SELECT * FROM characters
            WHERE map = '0' AND online='1'
            OR map = '1' AND online = '1'""")

        lst = list()

        for record in results:
            zone = Mysqld("alpha_world").query(
                """SELECT name FROM area_template
                WHERE entry = '" + str(record[27]) + "'""")

            pos = Azeroth_053(record[17], record[18]).maps(record[20])

            if record[3] in allience:
                faction = "alliance"
            else:
                faction = "horde"

            lst.append({
                'name': record[2],
                'position_x': record[17],
                'position_y': record[18],
                'race': record[3],
                'class': record[4],
                'level': record[6],
                'gender': record[5],
                'map': record[20],
                'posx': pos['x'],
                'posy': pos['y'],
                'faction': faction,
                'zone': zone,
                'show': 'player_information'
            })

        return lst

    def get_player_online(self, database):
        results = Mysqld(database).query(
            """SELECT count(guid) FROM characters
            WHERE map = '0' AND online='1'
            OR map = '1' AND online = '1'""")

        print("HÄR %s" % results[0][0])

        return results[0][0]


class World:
    def __init__(self):
        pass

    def get_creature_position(self, database):
        results = Mysqld(database).query(
            """SELECT * FROM spawns_creatures
            WHERE map = '0' AND ignored= '0'
            OR map = '1' AND ignored = '0'""")

        lst = list()

        for record in results:
            pos = Azeroth_053(record[8], record[9]).maps(record[5])

            lst.append({
                'id': record[0],
                'position_x': record[8],
                'position_y': record[9],
                'position_z': record[10],
                'orientation': record[11],
                'map': record[5],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "information"
            })

        return lst

    def get_worldport(self, database):
        results = Mysqld(database).query(
            """SELECT * FROM worldports
            WHERE map = '0' OR map = '1'""")

        lst = list()

        for record in results:
            pos = Azeroth_053(record[1], record[2]).maps(record[5])

            lst.append({
                'id': record[0],
                'name': record[6],
                'position_x': record[1],
                'position_y': record[2],
                'map': record[5],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "information"
            })

        return lst

    def get_gameobjects(self, database):
        results = Mysqld(database).query(
            """SELECT sg.spawn_entry, gt.name, sg.spawn_map, sg.spawn_positionX,
            sg.spawn_positionY, sg.spawn_positionZ, sg.spawn_orientation
            FROM spawns_gameobjects sg
            JOIN gameobject_template gt ON gt.entry = sg.spawn_id
            WHERE sg.spawn_map = '0' AND sg.ignored='0'
            OR sg.spawn_map = '1' AND sg.ignored='0'""")

        lst = list()

        for record in results:
            pos = Azeroth_053(record[3], record[4]).maps(record[2])

            lst.append({
                'id': record[0],
                'name': record[1],
                'map': record[2],
                'position_x': record[3],
                'position_y': record[4],
                'position_z': record[5],
                'spawn_orientation': record[6],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "information"
            })

        return lst
