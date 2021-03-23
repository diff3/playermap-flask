#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from database.model.realm import Characters
from database.model.world import SpawnsCreatures
from database.connection import ConnectDatabase
from sqlalchemy import or_


class Realm:
    def __init__(self):
        Realm.session = ConnectDatabase("alpha_realm").connect()

    def get_player_position(self):
        records = Realm.session.query(Characters).all()
        Realm.session.commit()

        lst = list()

        for record in records:
            lst.append({
                # 'name': record.name,
                'position_x': record.position_x,
                'position_y': record.position_y,
                # 'race': record.race,
                # 'class': record.class, # noqa
                # 'level': record.level,
                'map': record.map,
                # 'zone': record.zone,
            })

        return lst


class World:
    def __init__(self):
        World.session = ConnectDatabase("alpha_world").connect()

    def get_creature_position(self):
        records = World.session.query(SpawnsCreatures).filter(or_(
            SpawnsCreatures.map == '0', SpawnsCreatures.map == '1')).limit(1000).all()
        # .limit(1000)

        World.session.commit()

        lst = list()

        for record in records:
            lst.append({
                'position_x': record.position_x,
                'position_y': record.position_y,
                'map': record.map,
            })

        return lst
