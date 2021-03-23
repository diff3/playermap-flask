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
