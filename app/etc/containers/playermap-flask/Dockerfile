FROM python:3.11-alpine

COPY app/requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /opt/playermap-flask

CMD [ "python3", "main.py" ]
