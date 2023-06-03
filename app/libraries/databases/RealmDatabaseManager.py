# import hashlib
# import os
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from libraries.databases import RealmModels
from libraries.utils import Logger

with open('etc/config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


maps_static_data = config['maps_static_data']
host=config['database']['host']
user = config['database']['user']
password = config['database']['pass']
database = "alpha_realm"
charset = config['database']['charset']

realm_db_engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}', pool_pre_ping=True)
SessionHolder = scoped_session(sessionmaker(bind=realm_db_engine, autocommit=False, autoflush=True))


map_id = config['frontend']['map_id']

mapLeftPoint = maps_static_data[map_id]['mapLeftPoint']
mapTopPoint = maps_static_data[map_id]['mapTopPoint']
mapWidth = maps_static_data[map_id]['mapWidth']
mapHeight = maps_static_data[map_id]['mapHeight']
imageWidth = maps_static_data[map_id]['imageWidth']
imageHeight = maps_static_data[map_id]['imageHeight']


class RealmDatabaseManager(object):
    # Realm.
    
    @staticmethod
    def players_online():
        realm_db_session = SessionHolder()
        
        results = realm_db_session.query(
                RealmModels.Character
            ).filter(
                RealmModels.Character.online == '1'
            ).all()
            
        realm_db_session.close()

        return len(results)

    def get_player_location(map_id):
        realm_db_session = SessionHolder()

        results = realm_db_engine.query(RealmModels.Character
            ).filter(
                RealmModels.Character.map.in_(map_id), 
                RealmModels.Character.online == '1'
            ).all()

        for character in results:
            print(character.name, character.map, character.online)
            
        realm_db_session.close()