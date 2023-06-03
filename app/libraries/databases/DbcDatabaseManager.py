# import os
# from collections import defaultdict
# from typing import Optional
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from libraries.databases import DbcModels
from libraries.utils.Logger import Logger

# from game.world.managers.objects.locks.LockHolder import LockHolder
# from utils.ConfigManager import *
# from utils.constants.SpellCodes import SpellImplicitTargets


# DB_USER = os.getenv('MYSQL_USERNAME', config.Database.Connection.username)
# DB_PASSWORD = os.getenv('MYSQL_PASSWORD', config.Database.Connection.password)
# DB_HOST = os.getenv('MYSQL_HOST', config.Database.Connection.host)
# DB_DBC_NAME = config.Database.DBNames.dbc_db



with open('etc/config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


maps_static_data = config['maps_static_data']
host=config['database']['host']
user = config['database']['user']
password = config['database']['pass']
database = "alpha_dbc"
charset = config['database']['charset']

dbc_db_engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}',
                              pool_pre_ping=True)
SessionHolder = scoped_session(sessionmaker(bind=dbc_db_engine, autoflush=True))


# noinspection PyUnresolvedReferences
class DbcDatabaseManager:

    @staticmethod
    def get_all_taxi_nodes_by_mapid():
        dbc_db_session = SessionHolder()
        
        count = int(0)
        lst = dict()

        records = dbc_db_session.query(DbcModels.TaxiNode
            ).with_entities(
                DbcModels.TaxiNode.ID,
                DbcModels.TaxiNode.ContinentID,
                DbcModels.TaxiNode.X,
                DbcModels.TaxiNode.Y,
                DbcModels.TaxiNode.Z,
                DbcModels.TaxiNode.Name_enUS
            ).all()
        
        dbc_db_session.close()

        length = len(records)

        for record in records:
            d = {
                'id': record.ID,
                'map': record.ContinentID,
                'x': record.X,
                'y': record.Y,
                'z': record.Z,
                'name': record.Name_enUS,
                'map': record.ContinentID,
                'class_name': 'taxi'
            }

            lst[record.ID] = d
        
            count += 1
            Logger.progress('TaxiNode loading ...', count, length)

        return lst