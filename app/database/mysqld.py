#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from mysql.connector import connect, Error  # noqa
import os

__author__ = 'entropy'

path = os.path.dirname(__file__)
parent = os.path.join(path, os.pardir)
apath = os.path.abspath(parent)
cfile = os.path.join(apath, 'etc/config/config.conf')

config = configparser.ConfigParser()
config.read(cfile)

db = dict(config.items('DATABASE'))


class Mysqld:
    def __init__(self, database=db['database']):
        self.conn = connect(
            host=db['host'],
            user=db['user'],
            password=db['pass'],
            database=database
        )
        self.cursor = self.conn.cursor(buffered=True)

    def insert(self, SQL, tpl=None, database='alpha_realm'):
        self.cursor.execute(SQL, tpl)
        id = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()

        return id

    def delete(self, SQL, tpl=None, database='alpha_realm'):
        self.cursor.execute(SQL, tpl)
        id = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()

        return id

    def query(self, SQL, tpl=None):
        result = None

        self.cursor.execute(SQL, tpl)
        result = self.cursor.fetchall()

        self.conn.close()

        return result
