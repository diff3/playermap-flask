#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from database.model.realm import Characters
from database.model.world import SpawnsCreatures
from sqlalchemy import create_engine,  or_
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('/Users/mape0148/projekt/alpha-core/playermap-flask/config.conf')  # noqa
network = dict(config.items('NETWORK'))

engine = create_engine(
    'mysql+pymysql://{}:{}@{}:{}/{}'.format(
        network['user'],
        network['pass'],
        network['host'],
        network['port'],
        'alpha_world')
)


Session = sessionmaker(bind=engine)
session = Session()


class Realm:
    def __init__():
        pass

    def get_player_position():
        records = session.query(Characters).filter(Characters.map).all()
        session.commit()

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
    def __init__():
        pass

    def get_creature_position():
        records = session.query(SpawnsCreatures).filter(or_(
            SpawnsCreatures.map == '0', SpawnsCreatures.map == '1')).limit(1000).all()
        # .limit(1000)

        session.commit()

        lst = list()

        for record in records:
            lst.append({
                'position_x': record.position_x,
                'position_y': record.position_y,
                'map': record.map,
            })

        return lst
