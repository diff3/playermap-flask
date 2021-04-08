#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql.connector import connect, Error  # noqa


class Mysqld:
    def __init__(self, database):
        self.conn = connect(
            host="localhost",
            user="alpha-core",
            password="password",
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
