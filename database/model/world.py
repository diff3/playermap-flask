#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SpawnsCreatures(Base):
    __tablename__ = 'spawns_creatures'

    spawn_id = Column(INTEGER(10), primary_key=True, comment=u'Global Unique Identifier')
    spawn_entry1 = Column(ForeignKey(u'creature_template.entry', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True, server_default=text("'0'"), comment=u'Creature Template Id')
    spawn_entry2 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment=u'Creature Template Id')
    spawn_entry3 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment=u'Creature Template Id')
    spawn_entry4 = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"), comment=u'Creature Template Id')
    map = Column(SMALLINT(5), nullable=False, index=True, server_default=text("'0'"), comment=u'Map Identifier')
    display_id = Column(MEDIUMINT(8), nullable=False, server_default=text("'0'"))
    equipment_id = Column(MEDIUMINT(9), nullable=False, server_default=text("'0'"))
    position_x = Column(Float, nullable=False, server_default=text("'0'"))
    position_y = Column(Float, nullable=False, server_default=text("'0'"))
    position_z = Column(Float, nullable=False, server_default=text("'0'"))
    orientation = Column(Float, nullable=False, server_default=text("'0'"))
    spawntimesecsmin = Column(INTEGER(10), nullable=False, server_default=text("'120'"))
    spawntimesecsmax = Column(INTEGER(10), nullable=False, server_default=text("'120'"))
    wander_distance = Column(Float, nullable=False, server_default=text("'5'"))
    health_percent = Column(Float, nullable=False, server_default=text("'100'"))
    mana_percent = Column(Float, nullable=False, server_default=text("'100'"))
    movement_type = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spawn_flags = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    visibility_mod = Column(Float, server_default=text("'0'"))
    ignored = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class Worldports(Base):
    __tablename__ = 'worldports'

    entry = Column(INTEGER(11), autoincrement=True, primary_key=True)
    x = Column(Float, nullable=False, server_default=text("'0'"))
    y = Column(Float, nullable=False, server_default=text("'0'"))
    z = Column(Float, nullable=False, server_default=text("'0'"))
    o = Column(Float, nullable=False, server_default=text("'0'"))
    map = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    name = Column(String(255), nullable=False, server_default=text("''"))


class SpawnsGameobjects(Base):
    __tablename__ = 'spawns_gameobjects'

    spawn_id = Column(INTEGER(10), primary_key=True, comment='Global Unique Identifier')
    spawn_entry = Column(ForeignKey('gameobject_template.entry', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("'0'"), comment='Gameobject Identifier')
    spawn_map = Column(SMALLINT(5), nullable=False, index=True, server_default=text("'0'"), comment='Map Identifier')
    spawn_positionX = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_positionY = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_positionZ = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_orientation = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_rotation0 = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_rotation1 = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_rotation2 = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_rotation3 = Column(Float, nullable=False, server_default=text("'0'"))
    spawn_spawntimemin = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    spawn_spawntimemax = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    spawn_animprogress = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spawn_state = Column(TINYINT(3), nullable=False, server_default=text("'0'"))
    spawn_flags = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    spawn_visibility_mod = Column(Float, nullable=True, server_default=text("'0'"))
    ignored = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
