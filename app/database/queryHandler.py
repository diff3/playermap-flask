#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import Azeroth
from database import Mysqld

allience = [1, 3, 4, 7]


class Dbc:
    def __init__(self):
        pass

    def get_taxis_location(self, expansion):
        results = Mysqld("alpha_dbc").query(
            """SELECT * FROM TaxiNodes
            WHERE ContinentID = '0' OR ContinentID = '1'""")

        lst = list()

        for record in results:
            pos = Azeroth(record[2], record[3]).maps(expansion, record[1])

            lst.append({
                'id': record[0],
                'position_x': record[2],
                'position_y': record[3],
                'map': record[1],
                'name': record[5],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "taxi_info_popup"
            })

        return lst


class Realm:
    def __init__(self):
        pass

    def get_players_location(self, expansion):
        results = Mysqld("alpha_realm").query(
            """SELECT * FROM characters
            WHERE map = '0' AND online='1'
            OR map = '1' AND online = '1'""")

        lst = list()

        for record in results:
            zone = Mysqld("alpha_world").query(
                """SELECT name FROM area_template
                WHERE entry = '{}' """.format(record[27]))

            # guild = Mysqld("alpha_realm").guery()

            pos = Azeroth(record[17], record[18]).maps(expansion, record[20])

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
                # 'guild': guild,
                'faction': faction,
                'zone': zone,
                'show': 'player_info_popup'
            })

        return lst

    def get_players_online(self, expansion):
        results = Mysqld("alpha_realm").query(
            """SELECT count(guid) FROM characters
            WHERE online='1'""")

        return results[0][0]

    def get_players_in_zone(self, expansion):
        results = Mysqld("alpha_realm").query(
            """SELECT * FROM characters
            WHERE map = '0'
            AND online='1'
            AND zone = '1'""")

        """
        SELECT
        c.name, a.AreaName_enUS
        FROM
        alpha_realm.characters as c, alpha_dbc.AreaTable as a
        WHERE
        map='0' AND
        c.zone = a.ID AND
        a.ParentAreaNum='1048576'
        OR map ='0' AND
        c.zone = a.ID AND
        a.AreaNumber = '1048576';
        """

        lst = list()

        for record in results:
            print(record)
            # zone = Mysqld("alpha_dbc").query(
            #    """SELECT name FROM area_template
            #    WHERE entry = '{}' """.format(record[27]))

            # guild = Mysqld("alpha_realm").guery()

            pos = Azeroth(record[17], record[18]).maps(expansion, record[20])

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
                # 'guild': guild,
                'faction': faction,
                # 'zone': zone,
                'show': 'player_information'
            })

        return lst


class World:
    def __init__(self):
        pass

    def get_creatures_location(self, expansion):
        results = Mysqld("alpha_world").query(
            """SELECT
                sc.spawn_id, ct.name, sc.position_x, sc.position_y,
                sc.position_z, sc.orientation, sc.map, ct.display_id1
               FROM
                spawns_creatures as sc, creature_template as ct
               WHERE
                sc.map = '0' AND sc.ignored= '0' AND sc.spawn_entry1 = ct.entry
               OR
                sc.map = '0' AND sc.ignored = '0' AND
                sc.spawn_entry1 = ct.entry""")

        lst = list()

        for record in results:
            pos = Azeroth(record[2], record[3]).maps(expansion, record[6])

            lst.append({
                'id': record[0],
                'name': record[1],
                'position_x': record[2],
                'position_y': record[3],
                'position_z': record[4],
                'orientation': record[5],
                'map': record[6],
                'posx': pos['x'],
                'posy': pos['y'],
                'image': record[7],
                'show': "creature_info_popup"
            })

        return lst

    def get_worldports_location(self, expansion):
        results = Mysqld("alpha_world").query(
            """SELECT * FROM worldports
            WHERE map = '0' OR map = '1'""")

        lst = list()

        for record in results:
            pos = Azeroth(record[1], record[2]).maps(expansion, record[5])

            lst.append({
                'id': record[0],
                'name': record[6],
                'position_x': record[1],
                'position_y': record[2],
                'map': record[5],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "worldport_info_popup"
            })

        return lst

    def get_gameobjects_location(self, expansion):
        results = Mysqld("alpha_world").query(
            """SELECT sg.spawn_entry, gt.name, sg.spawn_map, sg.spawn_positionX,
            sg.spawn_positionY, sg.spawn_positionZ, sg.spawn_orientation
            FROM spawns_gameobjects sg
            JOIN gameobject_template gt ON gt.entry = sg.spawn_id
            WHERE sg.spawn_map = '0' AND sg.ignored='0'
            OR sg.spawn_map = '1' AND sg.ignored='0'""")

        lst = list()

        for record in results:
            pos = Azeroth(record[3], record[4]).maps(expansion, record[2])

            lst.append({
                'id': record[0],
                'name': record[1],
                'map': record[2],
                'position_x': record[3],
                'position_y': record[4],
                'position_z': record[5],
                'orientation': record[6],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "gameobject_info_popup"
            })

        return lst

    def get_quests_location(self, expansion):
        results = Mysqld("alpha_world").query(
            """SELECT
            ct.name,
            qt.Title,
            qt.Details,
            qt.Objectives,
            qt.PrevQuestId,
            qt.NextQuestId,
            sc.position_x,
            sc.position_y,
            sc.position_z,
            sc.map
            FROM
            alpha_world.spawns_creatures as sc,
            alpha_world.creature_questrelation as cq,
            alpha_world.creature_template as ct,
            alpha_world.quest_template as qt
            WHERE
            cq.entry = ct.entry AND
            cq.quest = qt.entry AND
            ct.entry = sc.spawn_entry1 AND
            sc.map = '0' AND
            sc.position_x < -4500 AND
            sc.position_x > -6400 AND
            sc.position_y > -2480 AND
            sc.position_y < 700 AND
            qt.ignored = '0'"""
        )

        lst = list()

        for record in results:
            pos = Azeroth(record[6], record[7]).maps(expansion, record[9])

            lst.append({
                # 'id': record[0],
                'name': record[0],
                'title': record[1],
                'details': record[2],
                'objectives': record[3],
                'prevquestid': record[4],
                'nextquestid': record[5],
                'map': record[9],
                'position_x': record[6],
                'position_y': record[7],
                'position_z': record[8],
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "quest_info_popup"
            })

        return lst
