#!/bin/sh

cd /opt/playermap-flask

/usr/local/bin/python -m pip install --upgrade pip
pip3 install -r requirements.txt

python3 main.py