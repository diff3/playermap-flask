#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from database.queryHandler import World, Realm, Dbc
from flask import Flask, render_template
from flask_socketio import SocketIO, emit  # noqa
from time import sleep  # noqa
from threading import Thread, Event


__author__ = 'entropy'

config = configparser.ConfigParser()
config.read('config.conf')

opac = dict(config.items('OPAC'))
webapp = dict(config.items('WEBAPP'))


app = Flask(__name__)
app.config['SECRET_KEY'] = webapp['secret_key']
app.config['DEBUG'] = webapp['debug']

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

thread_player_online = Thread()
thread_player_online_stop_event = Event()


@app.route('/')
def index():
    return render_template('index.html',
                           title=opac['title'],
                           admin=opac['admin'])


def player_position():
    while not thread_stop_event.isSet():
        socketio.emit('newposition',
                      Realm().get_player_position("alpha_realm"),
                      namespace=webapp['namespace'])

        socketio.sleep(int(webapp['timer']))


def player_online():
    while not thread_player_online_stop_event.isSet():
        socketio.emit('player_online',
                      Realm().get_player_online("alpha_realm"),
                      namespace=webapp['namespace'])

        socketio.sleep(int(webapp['timer']))


@socketio.on('connect', namespace=webapp['namespace'])
def playermap_connect():
    socketio.emit('newposition',
                  Realm().get_player_position("alpha_realm"),
                  namespace=webapp['namespace'])

    socketio.emit('player_online',
                  Realm().get_player_online("alpha_realm"),
                  namespace=webapp['namespace'])

    global thread, thread_player_online

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)

    if not thread_player_online.is_alive():
        print("Starting Thread")
        thread_player_online = socketio.start_background_task(player_online)


@socketio.on('disconnect', namespace=webapp['namespace'])
def test_disconnect():
    print('Client disconnected')


@socketio.on('get_player_position', namespace=webapp['namespace'])
def get_player_position(message):
    socketio.emit('newposition',
                  Realm().get_player_position("alpha_realm"),
                  namespace=webapp['namespace'])

    socketio.emit('player_online',
                  Realm().get_player_online("alpha_realm"),
                  namespace=webapp['namespace'])

    global thread, thread_player_online

    thread_player_online_stop_event.set()

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)

    if not thread_player_online.is_alive():
        print("Starting Thread")
        thread_player_online = socketio.start_background_task(player_online)


@socketio.on('get_worldport', namespace=webapp['namespace'])
def get_worldport(message):
    thread_stop_event.set()
    socketio.emit('new_worldport',
                  World().get_worldport("alpha_world"),
                  namespace=webapp['namespace'])


@socketio.on('get_creature_position', namespace=webapp['namespace'])
def get_creature_position(message):
    thread_stop_event.set()
    socketio.emit('new_creature_position',
                  World().get_creature_position("alpha_world"),
                  namespace=webapp['namespace'])


@socketio.on('get_gameobjects', namespace=webapp['namespace'])
def get_gameobjects(message):
    thread_stop_event.set()
    socketio.emit('new_gameobjects',
                  World().get_gameobjects("alpha_world"),
                  namespace=webapp['namespace'])


@socketio.on('get_taxi_nodes', namespace=webapp['namespace'])
def get_taxi_nodes(message):
    thread_stop_event.set()
    socketio.emit('new_taxi_location',
                  Dbc().get_taxi_nodes("alpha_dbc"),
                  namespace=webapp['namespace'])


if __name__ == '__main__':
    socketio.run(app, host=webapp['host'], port=webapp['port'])
