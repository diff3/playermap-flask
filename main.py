#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event

# from database.queryHandler import Realm, World, Dbc
import configparser
# from database.connection import ConnectDatabase

from database.mysqld import World, Realm, Dbc


__author__ = 'entropy'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


@app.route('/')
def index():
    return render_template('index.html', title="Online playermap")


def player_position():
    while not thread_stop_event.isSet():
        socketio.emit('newposition', Realm().get_player_position("alpha_realm"), namespace='/playermap')
        socketio.sleep(60)


@socketio.on('connect', namespace='/playermap')
def playermap_connect():
    socketio.emit('newposition', Realm().get_player_position("alpha_realm"), namespace='/playermap')
    global thread

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)


@socketio.on('disconnect', namespace='/playermap')
def test_disconnect():
    print('Client disconnected')


@socketio.on('get_player_position', namespace='/playermap')
def get_player_position(message):
    socketio.emit('newposition', Realm().get_player_position("alpha_realm"), namespace='/playermap')
    global thread

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)


@socketio.on('get_worldport', namespace='/playermap')
def get_worldport(message):
    thread_stop_event.set()
    socketio.emit('new_worldport', World().get_worldport("alpha_world"), namespace='/playermap')


@socketio.on('get_creature_position', namespace='/playermap')
def get_creature_position(message):
    thread_stop_event.set()
    socketio.emit('new_creature_position', World().get_creature_position("alpha_world"), namespace='/playermap')


@socketio.on('get_gameobjects', namespace='/playermap')
def get_gameobjects(message):
    thread_stop_event.set()
    socketio.emit('new_gameobjects', World().get_gameobjects("alpha_world"), namespace='/playermap')


@socketio.on('get_taxi_nodes', namespace='/playermap')
def get_taxi_nodes(message):
    thread_stop_event.set()
    socketio.emit('new_taxi_location', Dbc().get_taxi_nodes("alpha_dbc"), namespace='/playermap')


if __name__ == '__main__':
    socketio.run(app)
