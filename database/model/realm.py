from sqlalchemy import Column, Float, ForeignKey, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, MEDIUMINT, SMALLINT, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()


class Characters(Base):
    __tablename__ = 'characters'

    guid = Column(INTEGER(11), primary_key=True, autoincrement=True)
    account_id = Column('account', ForeignKey('accounts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, server_default=text("0"), comment='Account Identifier')
    name = Column(String(12), nullable=False, index=True, server_default=text("''"))
    race = Column(TINYINT(3), nullable=False, server_default=text("0"))
    class_ = Column('class', TINYINT(3), nullable=False, server_default=text("0"))
    gender = Column(TINYINT(3), nullable=False, server_default=text("0"))
    level = Column(TINYINT(3), nullable=False, server_default=text("0"))
    xp = Column(INTEGER(10), nullable=False, server_default=text("0"))
    money = Column(INTEGER(10), nullable=False, server_default=text("0"))
    skin = Column(TINYINT(3), nullable=False, server_default=text("0"))
    face = Column(TINYINT(3), nullable=False, server_default=text("0"))
    hairstyle = Column(TINYINT(3), nullable=False, server_default=text("0"))
    haircolour = Column(TINYINT(3), nullable=False, server_default=text("0"))
    facialhair = Column(TINYINT(3), nullable=False, server_default=text("0"))
    bankslots = Column(TINYINT(3), nullable=False, server_default=text("0"))
    talentpoints = Column(TINYINT(3), nullable=False, server_default=text("0"))
    skillpoints = Column(TINYINT(3), nullable=False, server_default=text("0"))
    position_x = Column(Float, nullable=False, server_default=text("0"))
    position_y = Column(Float, nullable=False, server_default=text("0"))
    position_z = Column(Float, nullable=False, server_default=text("0"))
    map = Column(INTEGER(11), nullable=False, server_default=text("0"), comment='Map Identifier')
    orientation = Column(Float, nullable=False, server_default=text("0"))
    taximask = Column(LONGTEXT)
    online = Column(TINYINT(3), nullable=False, index=True, server_default=text("0"))
    totaltime = Column(INTEGER(11), nullable=False, server_default=text("0"))
    leveltime = Column(INTEGER(11), nullable=False, server_default=text("0"))
    extra_flags = Column(INTEGER(11), nullable=False, server_default=text("0"))
    zone = Column(INTEGER(11), nullable=False, server_default=text("0"))
    taxi_path = Column(Text)
    drunk = Column(SMALLINT(5), nullable=False, server_default=text("0"))
    health = Column(INTEGER(10), nullable=False, server_default=text("0"))
    power1 = Column(INTEGER(10), nullable=False, server_default=text("0"))
    power2 = Column(INTEGER(10), nullable=False, server_default=text("0"))
    power3 = Column(INTEGER(10), nullable=False, server_default=text("0"))
    power4 = Column(INTEGER(10), nullable=False, server_default=text("0"))
    power5 = Column(INTEGER(10), nullable=False, server_default=text("0"))
