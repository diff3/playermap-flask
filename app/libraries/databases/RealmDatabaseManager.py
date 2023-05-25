import hashlib
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from libraries.databases import RealmModels
from libraries.utils import Logger


host="localhost"
user="root"
password="pwd"
database="alpha_realm"

realm_db_engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4', pool_pre_ping=True)
SessionHolder = scoped_session(sessionmaker(bind=realm_db_engine, autocommit=False, autoflush=True))

mapLeftPoint = 4267.765836313618
mapTopPoint = 4657.975130879346
mapWidth = 10568.022008253096
mapHeight = 19980.94603271984

imageWidth = 345
imageHeight = 650




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

    """
    guid = Column(INTEGER(11), primary_key=True, autoincrement=True)
    account_id = Column('account', ForeignKey('accounts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Account Identifier')
    realm_id = Column(TINYINT(3), nullable=False, server_default=text("1"))
    name = Column(String(12), nullable=False, index=True, server_default=text("''"))
    race = Column(TINYINT(3), nullable=False, server_default=text("0"))
    class_ = Column('class', TINYINT(3), nullable=False, server_default=text("0"))
    gender = Column(TINYINT(3), nullable=False, server_default=text("0"))
    level = Column(TINYINT(3), nullable=False, server_default=text("0"))
    position_x = Column(Float, nullable=False, server_default=text("0"))
    position_y = Column(Float, nullable=False, server_default=text("0"))
    position_z = Column(Float, nullable=False, server_default=text("0"))
    map = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Map Identifier')
    online = Column(TINYINT(3), nullable=False, index=True, server_default=text("0"))
    """
        
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