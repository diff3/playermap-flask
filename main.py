#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event

from database.queryHandler import Realm, World, Dbc
import configparser

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
        # socketio.emit('newposition', Dbc().get_taxi_nodes(), namespace='/playermap') # noqa
        # socketio.emit('newposition', Dbc().get_area_triggers(), namespace='/playermap') # noqa
        # socketio.emit('newposition', World().get_creature_position(), namespace='/playermap') # noqa
        socketio.emit('newposition', World().get_worldport(), namespace='/playermap') # noqa
        # socketio.emit('newposition', World().get_gameobjects(), namespace='/playermap') # noqa
        # socketio.emit('newposition', Realm().get_player_position(), namespace='/playermap') # noqa

        socketio.sleep(60)


@socketio.on('connect', namespace='/playermap')
def playermap_connect():
    global thread
    print('Client connected')

    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)


@socketio.on('disconnect', namespace='/playermap')
def test_disconnect():
    print('Client disconnected')


@socketio.on('message_from_browser', namespace='/playermap')
def message_from_browser(message):
    emit('message_from_server', "Hello from server", broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
