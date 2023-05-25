# import os
from collections import defaultdict
from typing import Optional

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


DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="pwd"
DB_DBC_NAME="alpha_dbc"

dbc_db_engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DBC_NAME}?charset=utf8mb4',
                              pool_pre_ping=True)
SessionHolder = scoped_session(sessionmaker(bind=dbc_db_engine, autoflush=True))


# noinspection PyUnresolvedReferences
class DbcDatabaseManager:

    @staticmethod
    def get_all_taxi_nodes_by_mapid(map_id):
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
                DbcModels.TaxiNode.Name_enUS,
            ).filter_by(ContinentID=map_id).all()
        
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
                'class_name': 'taxi'
            }

            lst[record.ID] = d
        
            count += 1
            Logger.progress('TaxiNode loading ...', count, length)

        return lst