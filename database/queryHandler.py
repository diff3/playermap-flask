#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Not used at the moment
"""

from database.model.realm import Characters
from database.model.world import *  # noqa
from database.model.dbc import TaxiNode, AreaTrigger, AreaTable # noqa
from database.connection import ConnectDatabase
from sqlalchemy import or_
from calculations import Azeroth

allience = [1, 3, 4, 7]


class Realm:
    def __init__(self):
        Realm.session = ConnectDatabase("alpha_realm").connect()

    def get_player_position(self):
        records = Realm.session.query(Characters).all()
        Realm.session.commit()

        lst = list()

        for record in records:
            pos = Azeroth(
                record.position_x, record.position_y).maps(record.map)

            if record.race in allience:
                faction = "alliance"
            else:
                faction = "horde"

            zone = Dbc().get_zone_name(record.zone)

            lst.append({
                'name': record.name,
                'position_x': record.position_x,
                'position_y': record.position_y,
                'race': record.race,
                'class': record.class_,
                'level': record.level,
                'gender': record.gender,
                'map': record.map,
                'posx': pos['x'],
                'posy': pos['y'],
                'faction': faction,
                'zone': zone,
                'show': 'player_information'
            })

        return lst


class World:
    def __init__(self, session):
        # World.session = ConnectDatabase("alpha_world").connect()
        World.session = session

    def get_creature_position(self):
        records = World.session.query(SpawnsCreatures) \
            .filter(or_(
                SpawnsCreatures.map == '0',
                SpawnsCreatures.map == '1',
                SpawnsCreatures.ignored == 0)).all()
            # .limit(1000).all()

        World.session.commit()

        lst = list()

        for record in records:
            pos = Azeroth(
                record.position_x, record.position_y).maps(record.map)

            name, display_id1 = self.get_creature_name(record.spawn_entry1)

            # todo get spawn namn from DBC database
            # dbc.CreatureDisplayInfo.ID == world.creature_template.display_id1
            # world.spawns_creature.spawn_entry1 == world.creature_template.entry

            lst.append({
                'id': record.spawn_id,
                'display_id': display_id1,
                'name': name,
                'position_x': record.position_x,
                'position_y': record.position_y,
                'position_z': record.position_z,
                'orientation': record.orientation,
                'map': record.map,
                'posx': pos['x'],
                'posy': pos['y'],
                'show': "information"
            })

        return lst

    def get_worldport(self):
        records = World.session.query(Worldports).filter(or_(
            Worldports.map == '0',
            Worldports.map == '1')).all()

        World.session.commit()

        lst = list()

        for record in records:
            pos = Azeroth(record.x, record.y).maps(record.map)

            lst.append({
                'id': record.entry,
                'name': record.name,
                'position_x': record.x,
                'position_y': record.y,
                'map': record.map,
                'posx': pos['x'],
                'posy': pos['y']
            })

        return lst

    def get_gameobjects(self):
        """ records = World.session.query(SpawnsGameobjects).filter(or_(
            SpawnsGameobjects.spawn_map == '0',
            SpawnsGameobjects.spawn_map == '1')).all() """

        records = World.session.query(SpawnsGameobjects).all()

        World.session.commit()

        lst = list()

        for record in records:
            pos = Azeroth(
                record.spawn_positionX, record.spawn_positionY).maps(
                    record.spawn_map)

            # todo get spawn name from DBC
            lst.append({
                'id': record.spawn_id,
                'position_x': record.spawn_positionX,
                'position_y': record.spawn_positionY,
                'map': record.spawn_map,
                'posx': pos['x'],
                'posy': pos['y']
            })

        return lst

    def get_creature_name(self, id):
        records = World.session.query(CreatureTemplate) \
            .filter(CreatureTemplate.entry == id) \
            .all()

        World.session.commit()

        name = str()
        display_id1 = int()

        for record in records:
            name = record.name
            display_id1 = record.display_id1

        return name, display_id1


class Dbc:
    def __init__(self):
        Dbc.session = ConnectDatabase("alpha_dbc").connect()

    def get_taxi_nodes(self):
        records = Dbc.session.query(TaxiNode).all()

        Dbc.session.commit()

        lst = list()

        for record in records:
            pos = Azeroth(record.X, record.Y).maps(record.ContinentID)

            lst.append({
                'id': record.ID,
                'position_x': record.X,
                'position_y': record.Y,
                'map': record.ContinentID,
                'name': record.Name_enUS,
                'posx': pos['x'],
                'posy': pos['y']
            })

        return lst

    def get_zone_name(self, id):
        records = Dbc.session.query(AreaTable) \
            .filter(AreaTable.ID == id) \
            .all()

        Dbc.session.commit()

        zone = str()

        for record in records:
            print(record.AreaName_enUS)
            zone = record.AreaName_enUS

        return zone
