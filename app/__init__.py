#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'entropy'

import configparser
from flask import Flask, render_template
from flask_socketio import SocketIO, emit  # noqa
import os
import sys
from time import sleep  # noqa
from threading import Thread, Event

path = os.path.dirname(__file__)
sys.path.append(path)
from database import World, Realm, Dbc # noqa


cfile = os.path.join(path, 'etc/config/config.conf')

config = configparser.ConfigParser()
config.read(cfile)

opac = dict(config.items('OPAC'))
webapp = dict(config.items('WEBAPP'))
expansion = dict(config.items(webapp['expansion']))


app = Flask(__name__)
app.config['SECRET_KEY'] = webapp['secret_key']
app.config['DEBUG'] = webapp['debug']

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

thread_players_online = Thread()
thread_players_online_stop_event = Event()


@app.route('/')
def index():
    return render_template('index.html',
                           title=opac['title'],
                           admin=opac['admin'],
                           map=expansion['mapfile'],
                           logo=expansion['logofile'],
                           expansion=webapp['expansion'])


@socketio.on('connect', namespace=webapp['namespace'])
def playermap_connect():
    global thread, thread_players_online
    socketio.emit('updated_players_location',
                  Realm().get_players_location(expansion),
                  namespace=webapp['namespace'])

    socketio.emit('players_online',
                  Realm().get_players_online(expansion),
                  namespace=webapp['namespace'])

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(players_locations)

    if not thread_players_online.is_alive():
        print("Starting Thread")
        thread_players_online = socketio.start_background_task(players_online)


@socketio.on('disconnect', namespace=webapp['namespace'])
def disconnect():
    print('Client disconnected')


def players_locations():
    while not thread_stop_event.isSet():
        socketio.emit('updated_players_location',
                      Realm().get_players_location(expansion),
                      namespace=webapp['namespace'])

        socketio.sleep(int(webapp['timer']))


def players_online():
    while not thread_players_online_stop_event.isSet():
        socketio.emit('players_online',
                      Realm().get_players_online(expansion),
                      namespace=webapp['namespace'])

        socketio.sleep(int(webapp['timer']))


@socketio.on('request_creatures_location', namespace=webapp['namespace'])
def creatures_location(message):
    thread_stop_event.set()
    socketio.emit('updated_creatures_location',
                  World().get_creatures_location(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_gameobjects_location', namespace=webapp['namespace'])
def gameobjects_location(message):
    thread_stop_event.set()
    socketio.emit('updated_gameobjects_location',
                  World().get_gameobjects_location(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_players_location', namespace=webapp['namespace'])
def players_location(message):
    global thread_stop_event, thread_players_online_stop_event

    # sync updates
    thread_stop_event.clear()
    thread_players_online_stop_event.set()
    thread_players_online_stop_event.clear()
    playermap_connect()


@socketio.on('request_quests_location', namespace=webapp['namespace'])
def quests_location(message):
    thread_stop_event.set()
    socketio.emit('updated_quests_location',
                  World().get_quests_location(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_taxis_location', namespace=webapp['namespace'])
def taxis_location(message):
    thread_stop_event.set()
    socketio.emit('updated_taxis_location',
                  Dbc().get_taxis_location(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_worldports_location', namespace=webapp['namespace'])
def get_worldports_location(message):
    thread_stop_event.set()
    socketio.emit('updated_worldports_location',
                  World().get_worldports_location(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_players_in_zone', namespace=webapp['namespace'])
def players_in_zone(message):
    thread_stop_event.set()
    socketio.emit('players_in_zone',
                  World().get_players_in_zone(expansion),
                  namespace=webapp['namespace'])


@socketio.on('request_expansion_change', namespace=webapp['namespace'])
def request_expansion_change(value):
    global thread_stop_event, thread_players_online_stop_event, expansion

    expansion = dict(config.items(value))

    # sync updates
    thread_stop_event.clear()
    thread_players_online_stop_event.set()
    thread_players_online_stop_event.clear()
    playermap_connect()

    socketio.emit('updated_expansion',
                  expansion, namespace=webapp['namespace'])


if __name__ == '__main__':
    socketio.run(app, host=webapp['host'], port=webapp['port'])
