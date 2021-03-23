#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from time import sleep
from threading import Thread, Event

from database.queryHandler import Realm, World
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
        socketio.emit('newposition', World.get_creature_position(),
                      namespace='/playermap')
        socketio.sleep(5)


@socketio.on('connect', namespace='/playermap')
def playermap_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(player_position)


@socketio.on('disconnect', namespace='/playermap')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
