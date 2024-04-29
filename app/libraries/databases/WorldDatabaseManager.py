#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from libraries.utils.Logger import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from libraries.databases import WorldModels

import yaml

with open('etc/config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)


maps_static_data = config['maps_static_data']
host=config['database']['host']
user = config['database']['user']
password = config['database']['pass']
database = "alpha_world"
charset = config['database']['charset']

world_db_engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}?charset={charset}', pool_pre_ping=True)
SessionHolder = scoped_session(sessionmaker(bind=world_db_engine, autocommit=False, autoflush=True))


map_id = config['frontend']['map_id']

mapLeftPoint = maps_static_data[map_id]['mapLeftPoint']
mapTopPoint = maps_static_data[map_id]['mapTopPoint']
mapWidth = maps_static_data[map_id]['mapWidth']
mapHeight = maps_static_data[map_id]['mapHeight']
imageWidth = maps_static_data[map_id]['imageWidth']
imageHeight = maps_static_data[map_id]['imageHeight']



class WorldDatabaseManager:

    @staticmethod
    def SpawnGameObjects(is_ignored=0):
        world_db_session = SessionHolder()
        
        count = int(0)
        lst = dict()

        records = world_db_session.query(
            WorldModels.SpawnsGameobjects, WorldModels.GameobjectTemplate
        ).with_entities(
            WorldModels.SpawnsGameobjects.spawn_id,
            WorldModels.SpawnsGameobjects.spawn_map,
            WorldModels.SpawnsGameobjects.spawn_positionX,
            WorldModels.SpawnsGameobjects.spawn_positionY,
            WorldModels.SpawnsGameobjects.spawn_positionZ,
            WorldModels.SpawnsGameobjects.ignored,
            WorldModels.GameobjectTemplate.name,
            WorldModels.SpawnsGameobjects.spawn_entry,
            WorldModels.GameobjectTemplate.display_id
        ).filter(
            WorldModels.SpawnsGameobjects.ignored == is_ignored,
            WorldModels.GameobjectTemplate.entry == WorldModels.SpawnsGameobjects.spawn_entry
        ).all()

        length = len(records)

        for record in records:
            d = {
                'id': record.spawn_id,
                'x': record.spawn_positionX,
                'y': record.spawn_positionY,
                'z': record.spawn_positionZ,
                'map': record.spawn_map,
                'name': record.name,
                'entry': record.spawn_entry,
                'display_id': record.display_id,
                'class_name': 'objects'
            }

            lst[record.spawn_id] = d

            count += 1
            Logger.progress('SpawnGameObjects loading ...', count, length)

        world_db_session.close()

        return lst

    @staticmethod
    def SpawnCreatures(is_ignored=0):
        """
        Retrieves a dictionary of spawn creatures from the database for a given map_id and ignored flag.
        :param map_id: The ID of the map to retrieve the creatures from.
        :type map_id: int
        :param is_ignored: Flag to indicate if the creature should be ignored or not.
        :type is_ignored: bool
        :return: A dictionary of creatures and their spawn information.
        :rtype: dict
        """
        world_db_session = SessionHolder()

        count = int(0)
        lst = dict()

        records = world_db_session.query(
                WorldModels.SpawnsCreatures, WorldModels.CreatureTemplate 
               ).with_entities(
                WorldModels.SpawnsCreatures.spawn_id,
                WorldModels.SpawnsCreatures.position_x,
                WorldModels.SpawnsCreatures.position_y,
                WorldModels.SpawnsCreatures.position_z,
                WorldModels.SpawnsCreatures.orientation,
                WorldModels.CreatureTemplate.name,
                WorldModels.CreatureTemplate.display_id1,
                WorldModels.SpawnsCreatures.spawn_entry1, 
                WorldModels.SpawnsCreatures.map 
            ).filter(
                WorldModels.SpawnsCreatures.ignored == is_ignored,
                WorldModels.SpawnsCreatures.spawn_entry1 ==  WorldModels.CreatureTemplate.entry
            ).all()
       
        
        length = len(records)

        for record in records:
            
            d = {
                'id': record.spawn_id,
                'entry': record.spawn_entry1,
                'x': record.position_x,
                'y': record.position_y,
                'z': record.position_z,
                'orientation': record.orientation,
                'map': record.map,
                'name': record.name,
                'display_id': record.display_id1,
                'class_name': 'creature'
            }

            lst[record.spawn_id] = d
        
            count += 1
            Logger.progress('SpawnCreatures loading ...', count, length)

        world_db_session.close()

        return lst

    @staticmethod
    def WorldPorts():
        world_db_session = SessionHolder()

        count = int(0)
        lst = dict()

        records = world_db_session.query (
            WorldModels.Worldports
        ).all()

        length = len(records)
    
        for record in records:
            d = dict()
            
            for key in record.__dict__.keys():
                if key != '_sa_instance_state':
                    d[key] = getattr(record, key)
            
            d['id'] = record.entry
            d['class_name'] = 'worldport'

            lst[record.entry] = d
        
            count += 1
            Logger.progress('WorldPort loading ...', count, length)

        world_db_session.close()
        
        return lst 


    @staticmethod
    def get_quests_location(is_ignored):
        world_db_session = SessionHolder()

        count = int(0)
        lst = dict()

        """ records = world_db_session.query(
            WorldModels.CreatureTemplate.name,
            WorldModels.QuestTemplate.Title,
            WorldModels.QuestTemplate.Details,
            WorldModels.QuestTemplate.Objectives,
            WorldModels.QuestTemplate.PrevQuestId,
            WorldModels.QuestTemplate.NextQuestId,
            WorldModels.SpawnsCreatures.position_x,
            WorldModels.SpawnsCreatures.position_y,
            WorldModels.SpawnsCreatures.position_z,
            WorldModels.SpawnsCreatures.map,
            WorldModels.QuestTemplate.entry
        ).select_from(
            WorldModels.SpawnsCreatures,
            WorldModels.CreatureTemplate,
            WorldModels.QuestTemplate
        ).where(
            WorldModels.CreatureTemplate.entry == WorldModels.QuestTemplate.entry,
            WorldModels.CreatureTemplate.entry == WorldModels.SpawnsCreatures.spawn_entry1,
            WorldModels.QuestTemplate.ignored == is_ignored
        ).all() """
        
        records = world_db_session.query(
            WorldModels.CreatureTemplate.name,
            WorldModels.QuestTemplate.Title,
            WorldModels.QuestTemplate.Details,
            WorldModels.QuestTemplate.Objectives,
            WorldModels.QuestTemplate.PrevQuestId,
            WorldModels.QuestTemplate.NextQuestId,
            WorldModels.SpawnsCreatures.position_x,
            WorldModels.SpawnsCreatures.position_y,
            WorldModels.SpawnsCreatures.position_z,
            WorldModels.SpawnsCreatures.map,
            WorldModels.QuestTemplate.entry
        ).select_from(
            WorldModels.SpawnsCreatures,
            WorldModels.CreatureTemplate,
            WorldModels.QuestTemplate,
            WorldModels.t_creature_quest_starter
        ).where(
                WorldModels.CreatureTemplate.entry == WorldModels.SpawnsCreatures.spawn_entry1,
                WorldModels.t_creature_quest_starter.c.entry == WorldModels.CreatureTemplate.entry,
                WorldModels.t_creature_quest_starter.c.quest == WorldModels.QuestTemplate.entry,
                WorldModels.QuestTemplate.ignored == is_ignored    
        ).all()



        length = len(records)

        for record in records:
            d = {
                'id': record.entry,
                'name': record.name,
                'title': record.Title,
                'details': record.Details,
                'objectives': record.Objectives,
                'prev_quest_id': record.PrevQuestId,
                'next_quest_id': record.NextQuestId,
                'x': record.position_x,
                'y': record.position_y,
                'z': record.position_z,
                'map': record.map,
                'quest': record.entry,
                'class_name': 'quest'
            }

            lst[record.entry] = d

            count += 1
            Logger.progress('QuestStartLocation loading ...', count, length)

        world_db_session.close()
        
        return lst 


if __name__ == '__main__':
    pass
