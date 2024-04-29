#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

__author__ = 'entropy'

import logging
import libraries.calculations.viewport as viewport
import os
import secrets
import sys
import threading
import uuid
import yaml

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from libraries.calculations import position
from libraries.databases.WorldDatabaseManager import WorldDatabaseManager
from libraries.databases.RealmDatabaseManager import RealmDatabaseManager
from libraries.databases.DbcDatabaseManager import DbcDatabaseManager

client_ids = list()

def generate_unique_client_id():
    while True:
        random_number = secrets.randbits(128)
        unique_id = uuid.UUID(int=random_number)
        unique_id_str = str(unique_id)

        if unique_id_str not in client_ids:
            client_ids.append(unique_id_str)
            return unique_id_str


# logger = logging.getLogger('socketio')
# logging.getLogger('engineio').setLevel(logging.NONE)

spawnsCratures = list()
gameObjectsLocations = list()
taxiLocations = list()
worldPorts = list()
guestsLocation = list()

client_counter = 0 

path = os.path.dirname(__file__)
sys.path.append(path)

with open('etc/config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

frontend = config['frontend']
app_conf = config['app']
game_version = config['app']['game_version']
maps_static_data = config['maps_static_data']
viewport_offset = config['viewport']['offset']
version = config[game_version]

def staticMapData(map_id):
    mapLeftPoint = maps_static_data[map_id]['mapLeftPoint']
    mapTopPoint = maps_static_data[map_id]['mapTopPoint']
    mapWidth = maps_static_data[map_id]['mapWidth']
    mapHeight = maps_static_data[map_id]['mapHeight']
    imageWidth = maps_static_data[map_id]['imageWidth']
    imageHeight = maps_static_data[map_id]['imageHeight']

    return mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight

def filterDictionary(original_dict, filters):

    print("hello")

    filtered_dict = original_dict.copy()

    for filter_item in filters:
        filter_key = filter_item[0]
        filter_value = filter_item[1]

        print(f"filter_key: {filter_key}, filter_value: {filter_value}")

        tmp = {}
        for key, value in filtered_dict.items():
            if str(filter_key) in str(value) and str(value[filter_key]) == str(filter_value):
                tmp[key] = value

        filtered_dict = tmp

    print(filtered_dict)
    return filtered_dict



app = Flask(__name__)
app.config['STATIC_FOLDER'] = app_conf['static_folder']
app.config['SECRET_KEY'] = app_conf['secret_key']
app.config['DEBUG'] = False
app.clients = {}

socketio = SocketIO(app, logger=app_conf['logger'], engineio_logger=app_conf['engineio_logger'])
scheduler = None

@app.route('/')
def index():
    return render_template('index.html',
                           title=frontend['title'],
                           admin=frontend['admin'],
                           map=version['mapfile'],
                           logo=version['logofile'],
                           expansion=app_conf['game_version'])

def players_online_thread():
    print("Updating players online")
    
    global scheduler, client_ids
    
    processed_clients = set() 
    print("processed clients: ", processed_clients)
    
    for client_id in client_ids:
        if client_id not in processed_clients:
            playersOnline = RealmDatabaseManager.players_online()
            socketio.emit('players_online', playersOnline, room=client_id, namespace=app_conf['namespace'])
            processed_clients.add(client_id) 
    
    print("processed clients: ", processed_clients)
    scheduler = threading.Timer(app_conf['timer'], players_online_thread)
    scheduler.start()


@socketio.on('connect', namespace=app_conf['namespace'])
def handle_connect():
    global client_ids
    print("Client connected")
    client_id = generate_unique_client_id()
    socketio.emit('connected', client_id, namespace=app_conf['namespace'])

    client_ids.append(client_id)
    join_room(client_id)

    players_online_thread()

@socketio.on('disconnect_event', namespace=app_conf['namespace'])
def handle_disconnect(clientId):
    global client_ids

    while clientId in client_ids: client_ids.remove(clientId)
    leave_room(clientId)

    print(f"Client {clientId} is disconnected")

@socketio.on('request_players_location', namespace=app_conf['namespace'])
def players_location(message):
    pass


@socketio.on('mouse_enter_info', namespace=app_conf['namespace'])
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

    emit('show_info_popups', {'requested_data': requested_data}, namespace=app_conf['namespace'])


@socketio.on('request_server_update', namespace=app_conf['namespace'])
def request_server_update(data):
    """
    Handles a 'request_server_update' event from a socketio client. 
    Recalculates the positions of various objects on a map using 
    the supplied data. Returns a dictionary of updated positions 
    based on the request type. 

    Args:
        data (dict): A dictionary of data supplied by the client.

    Returns:
         data (dict): A dictionary of updated positions.

    Raises:
        None.
    """

    map_id = int(data['filters'][0][1])

    mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight = staticMapData(map_id)

    spawns_reduced = dict()
    spawns_viewport = dict()
    
    magnification = data['magnification']

    max_x = data['max_x']
    max_y = data['max_y']

    offset_x = data['offsetLeft']
    offset_y = data['offsetTop']

    if type(offset_x) == str:
        offset_x = float(offset_x[:-2])
        offset_y = float(offset_y[:-2])

    print(data)


    if not 'filters' in data:
        filters = [
            ['map', 0],
        ]
    else:
        filters = data['filters']

    match data['id']:
        case 'get_taxis_button':
            filtered_spawns = filterDictionary(taxiLocations, filters)
            numSpawns = len(taxiLocations)

            if len(filtered_spawns) == 0:
                return
            recalculated_spawns = position.recalculate(filtered_spawns, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            filtered_spawns = filterDictionary(recalculated_spawns, filters)
            spawns = filtered_spawns 
        case 'get_creatures_button':
            filtered_spawns = filterDictionary(spawnsCratures, filters)
            numSpawns = len(spawnsCratures)

            if len(filtered_spawns) == 0:
                return


            recalculated_spawns = position.recalculate(filtered_spawns, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)
            spawns_viewport = viewport.recalculate_objects_limited_by_viewport(recalculated_spawns, max_x, max_y, viewport_offset)
            offset = position.calculate_offset_for_items(3000, len(spawns_viewport))

            for id in spawns_viewport:
                if id % offset == 0:
                    spawns_reduced[id] = spawns_viewport[id]

            spawns = spawns_reduced
        case 'get_gameobjects_button':
            filtered_spawns = filterDictionary(gameObjectsLocations, filters)
            numSpawns = len(filtered_spawns)
            spawns_viewport = viewport.recalculate_objects_limited_by_viewport(recalculated_spawns, max_x, max_y, viewport_offset)
            offset = position.calculate_offset_for_items(3000, len(spawns_viewport))

            for id in spawns_viewport:
                if id % offset == 0:
                    spawns_reduced[id] = spawns_viewport[id]

            spawns = spawns_reduced 
        case 'get_worldports_button':
            filtered_spawns = filterDictionary(worldPorts, filters)
            numSpawns = len(worldPorts)

            if len(filtered_spawns) == 0:
                return
            recalculated_spawns = position.recalculate(filtered_spawns, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            spawns = recalculated_spawns
        case 'get_quests_button':
            filtered_spawns = filterDictionary(guestsLocation, filters)
            numSpawns = len(guestsLocation)
            recalculated_spawns = position.recalculate(filtered_spawns, mapLeftPoint, mapTopPoint, mapWidth, mapHeight, imageWidth, imageHeight, magnification, offset_x, offset_y)

            spawns = recalculated_spawns
            pass
        case _:   
            pass

    spawnData = {
        "spawned": len(spawns),
        "numSpawns": numSpawns
    }

    emit('receaving_update_from_server', {'spawnSVGElements': spawns, 'spawnData': spawnData}, namespace=app_conf['namespace'])

if __name__ == '__main__':
    spawnsCratures = WorldDatabaseManager.SpawnCreatures(is_ignored=0)
    gameObjectsLocations = WorldDatabaseManager.SpawnGameObjects(is_ignored=0)
    taxiLocations = DbcDatabaseManager.get_all_taxi_nodes_by_mapid()
    worldPorts = WorldDatabaseManager.WorldPorts()
    guestsLocation = WorldDatabaseManager.get_quests_location(0)

    socketio.run(app, host=app_conf['host'], port=app_conf['port'], debug=True)
