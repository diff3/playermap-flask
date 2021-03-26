#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaxiNode(Base):
    __tablename__ = 'TaxiNodes'

    ID = Column(INTEGER(11), primary_key=True, server_default=text("'0'"))
    ContinentID = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    X = Column(Float, nullable=False, server_default=text("'0'"))
    Y = Column(Float, nullable=False, server_default=text("'0'"))
    Z = Column(Float, nullable=False, server_default=text("'0'"))
    Name_enUS = Column(Text)
    Name_enGB = Column(Text)
    Name_koKR = Column(Text)
    Name_frFR = Column(Text)
    Name_deDE = Column(Text)
    Name_enCN = Column(Text)
    Name_zhCN = Column(Text)
    Name_enTW = Column(Text)
    Name_Mask = Column(INTEGER(10), nullable=False, server_default=text("'0'"))


class AreaTrigger(Base):
    __tablename__ = 'AreaTrigger'

    ID = Column(INTEGER(11), primary_key=True, server_default=text("'0'"))
    ContinentID = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    X = Column(Float, nullable=False, server_default=text("'0'"))
    Y = Column(Float, nullable=False, server_default=text("'0'"))
    Z = Column(Float, nullable=False, server_default=text("'0'"))
    Radius = Column(Float, nullable=False, server_default=text("'0'"))

class AreaTable(Base):
    __tablename__ = 'AreaTable'

    ID = Column(INTEGER(11), primary_key=True, server_default=text("'0'"))
    AreaNumber = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    ContinentID = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    ParentAreaNum = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    AreaBit = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    Flags = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    SoundProviderPref = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    SoundProviderPrefUnderwater = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    MIDIAmbience = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    MIDIAmbienceUnderwater = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    ZoneMusic = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    IntroSound = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    IntroPriority = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    AreaName_enUS = Column(Text)
    AreaName_enGB = Column(Text)
    AreaName_koKR = Column(Text)
    AreaName_frFR = Column(Text)
    AreaName_deDE = Column(Text)
    AreaName_enCN = Column(Text)
    AreaName_zhCN = Column(Text)
    AreaName_enTW = Column(Text)
    AreaName_Mask = Column(INTEGER(10), nullable=False, server_default=text("'0'"))
    
