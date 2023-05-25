#!/bin/sh

/usr/local/bin/python -m pip install --upgrade pip

mkdir -p /opt/playermap-flask
cd /opt/playermap-flask
pip3 install -r requirements.txt
cp /opt/playermap-flask/etc/config/config.conf.docker /opt/playermap-flask/etc/config/config.conf
# /usr/bin/tmux new -d -s playermap "top"
# /usr/bin/tmux new -d -s playermap "cd /opt/playermap-flask/ && /usr/local/bin/python3 __init__.py"
python3 main.py

# /bin/sh
