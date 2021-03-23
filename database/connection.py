#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = configparser.ConfigParser()
config.read('config.conf')  # noqa
network = dict(config.items('NETWORK'))


class ConnectDatabase:
    def __init__(self, database=network['database']):
        self.engine = create_engine(
            'mysql+pymysql://{}:{}@{}:{}/{}'.format(
                network['user'],
                network['pass'],
                network['host'],
                network['port'],
                database)
        )

    def connect(self):
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        return self.session
