#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

__author__ = 'entropy'

import configparser
import json
import logging
import numpy as np
import os
import sys

from libraries.databases.WorldDatabaseManager import WorldDatabaseManager
from libraries.databases.RealmDatabaseManager import RealmDatabaseManager
from libraries.databases.DbcDatabaseManager import DbcDatabaseManager
# from libraries.databases.queryHandler import World, Realm, Dbc

import libraries.calculations.viewport as viewport

import threading
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from libraries.calculations import position

import uuid
import secrets

client_ids = list()

def generate_unique_client_id():
    while True:
        random_number = secrets.randbits(128)
        unique_id = uuid.UUID(int=random_number)
        unique_id_str = str(unique_id)

        if unique_id_str not in client_ids:
            client_ids.append(unique_id_str)
            return unique_id_str


logger = logging.getLogger('socketio')
logging.disable(logging.CRITICAL) 

# Flytta till konfig
mapLeftPoint = 4267.765836313618
mapTopPoint = 4657.975130879346
mapWidth = 10568.022008253096
mapHeight = 19980.94603271984

imageWidth = 345
imageHeight = 650

spawnsCratures = list()
gameObjectsLocations = list()
taxiLocations = list()
worldPorts = list()
guestsLocation = list()

client_counter = 0 


path = os.path.dirname(__file__)
sys.path.append(path)

cfile = os.path.join(path, 'etc/config/config.conf')

config = configparser.ConfigParser()
config.read(cfile)

opac = dict(config.items('OPAC'))
webapp = dict(config.items('WEBAPP'))
expansion = dict(config.items(webapp['expansion']))


app = Flask(__name__)
app.config['STATIC_FOLDER'] = '/static'
app.config['SECRET_KEY'] = webapp['secret_key']
app.config['DEBUG'] = webapp['debug']
app.clients = {}

socketio = SocketIO(app, logger=True, engineio_logger=True)
scheduler = None

@app.route('/')
def index():
    return render_template('index.html',
                           title=opac['title'],
                           admin=opac['admin'],
                           map=expansion['mapfile'],
                           logo=expansion['logofile'],
                           expansion=webapp['expansion'])

def players_online_thread():
    print("Updating players online")
    
    global scheduler, client_ids
    
    processed_clients = set() 
    print("processed clients: ", processed_clients)
    
    for client_id in client_ids:
        if client_id not in processed_clients:
            playersOnline = RealmDatabaseManager.players_online()
            socketio.emit('players_online', playersOnline, room=client_id, namespace=webapp['namespace'])
            processed_clients.add(client_id) 
    
    print("processed clients: ", processed_clients)
    scheduler = threading.Timer(60.0, players_online_thread)
    scheduler.start()


@socketio.on('connect', namespace=webapp['namespace'])
def handle_connect():
    print("Client connected")
    client_id = generate_unique_client_id()
    socketio.emit('connected', client_id, namespace=webapp['namespace'])

    client_ids.append(client_id)
    join_room(client_id)

    players_online_thread()

@socketio.on('disconnect_event', namespace=webapp['namespace'])
def handle_disconnect(clientId):
    if clientId in client_ids:
        client_ids.remove(clientId)
        leave_room(clientId)
        print(f"Client {clientId} disconnected")

@socketio.on('request_players_location', namespace=webapp['namespace'])
def players_location(message):
    pass


@socketio.on('mouse_enter_info', namespace=webapp['namespace'])
def request_popup_information(data):
    
    match data['class_name']:
        case 'worldport':
            ID = int(data['id'])

            requested_data = {
                'mouseX': data['mouseX'],
                'mouseY': data['mouseY'],
                'subTitle': f"ID: {ID}, x: {worldPorts[ID]['x']}, y: {worldPorts[ID]['y']} ",
                'data': worldPorts[int(data['id'])],
                'name': worldPorts[int(data['id'])]['name'], 
                'notes': f"Shift + Click for info",
                'url': f"https://db.thealphaproject.eu/index.php?action=show_port&id={data['id']}&sort_order=name&pos=1&max=1618"
            }

        case 'objects':
            ID = int(data['id'])

            requested_data = {
                'mouseX': data['mouseX'],
                'mouseY': data['mouseY'],
                'subTitle': f"ID: {ID}, x: {gameObjectsLocations[ID]['x']}, y: {gameObjectsLocations[ID]['y']} ",
                'data': gameObjectsLocations[int(data['id'])],
                'name': gameObjectsLocations[int(data['id'])]['name'], 
                'notes': f"Shift + Click for info",
                'url': f"https://db.thealphaproject.eu/index.php?action=show_go&id={gameObjectsLocations[ID]['entry']}"
            }

        case 'creature':
            ID = int(data['id'])
            path = f"/static/img/creatures/{spawnsCratures[ID]['display_id']}.webp"
            image = f"<img class='image' src='{path}' /><br/>Shift + Click for info"

            requested_data = {
                'mouseX': data['mouseX'],
                'mouseY': data['mouseY'], 
                'subTitle': f"""ID: {ID}, x: {spawnsCratures[ID]['x']}, y: {spawnsCratures[ID]['y']}
                <br/>o: {spawnsCratures[ID]['orientation']} """,
                'data': spawnsCratures[int(data['id'])],
                'name': spawnsCratures[int(data['id'])]['name'], 
                'notes': image,
                'url': f"https://db.thealphaproject.eu/index.php?action=show_creature&id={spawnsCratures[ID]['entry']}"
            }

           # print(requested_data['url'])

        case 'taxi':
            ID = int(data['id'])

            requested_data = {
                'mouseX': data['mouseX'],
                'mouseY': data['mouseY'], 
                'subTitle': f"ID: {ID}, x: {taxiLocations[ID]['x']}, y: {taxiLocations[ID]['y']} ",
                'data': taxiLocations[int(data['id'])],
                'name': taxiLocations[int(data['id'])]['name'], 
                'notes': "",
                'url': "no"
            }

        case 'quest':
            ID = int(data['id'])

            requested_data = {
                'mouseX': data['mouseX'],
                'mouseY': data['mouseY'], 
                'name': guestsLocation[int(data['id'])]['title'],
                'subTitle': f"npc: {guestsLocation[int(data['id'])]['name']}",
                'data': guestsLocation[int(data['id'])],
                'notes': f"{guestsLocation[int(data['id'])]['details']} <br/>Shift + Click for info",
                'url': f"https://db.thealphaproject.eu/?action=show_quest&id={ID}&sort_order=Title&pos=1&max=1189"
            } 

    emit('show_info_popups', {'requested_data': requested_data}, namespace=webapp['namespace'])


@socketio.on('request_server_update', namespace=webapp['namespace'])
def request_server_update(data):
    spawns_reduced = dict()
    spawns_in_viewport = dict()
    
    magnification = data['magnification']
    offset = position.calculate_data_reduction_offset(magnification)

    max_x = data['max_x']
    max_y = data['max_y']

    offset_x = data['offsetLeft']
    offset_y = data['offsetTop']

    if type(offset_x) == str:
        offset_x = float(offset_x[:-2])
        offset_y = float(offset_y[:-2])

    match data['id']:
        case 'get_taxis_button':
            recalculated_spawns = position.recalculate(taxiLocations, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            spawns = recalculated_spawns 
        case 'get_creatures_button':
            recalculated_spawns = position.recalculate(spawnsCratures, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            # with open('recalculated_spawns.json', 'w') as file:
                # json.dump(recalculated_spawns, file, indent=4)

            for id in recalculated_spawns:
                if id % offset == 0:
                    spawns_reduced[id] = recalculated_spawns[id]

            spawns = viewport.recalculate_objects_limited_by_viewport(spawns_reduced, max_x, max_y)
            # spawns = spawns_reduced
        case 'get_gameobjects_button':
            recalculated_spawns = position.recalculate(gameObjectsLocations, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            for id in recalculated_spawns:
                if id % offset == 0:
                    spawns_reduced[id] = recalculated_spawns[id]

            spawns = spawns_reduced 
        case 'get_worldports_button':
            recalculated_spawns = position.recalculate(worldPorts, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            spawns = recalculated_spawns
        case 'get_quests_button':
            recalculated_spawns = position.recalculate(guestsLocation, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            spawns = recalculated_spawns
            pass
        case _:   
            pass
        
    emit('receaving_update_from_server', {'spawnSVGElements': spawns}, namespace=webapp['namespace'])

if __name__ == '__main__':
    spawnsCratures = WorldDatabaseManager.SpawnCreatures(0, 0)
    gameObjectsLocations = WorldDatabaseManager.SpawnGameObjects(0, 0)
    taxiLocations = DbcDatabaseManager.get_all_taxi_nodes_by_mapid(0)
    worldPorts = WorldDatabaseManager.WorldPorts(0)
    guestsLocation = WorldDatabaseManager.get_quests_location(0, 0)

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)