#!/bin/sh

/usr/local/bin/python -m pip install --upgrade pip

mkdir -p /
cd /opt/playermap-flask
pip3 install -r requirements.txt
cp /opt/playermap-flask/etc/config/config.conf.docker /opt/playermap-flask/etc/config/config.conf
python3 __init__.py
