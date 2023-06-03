# Online player map for Alpha-core. 



The easiest way to start Playermap-flask, is to first start Alpha-core, Playermap-flask uses alpha-core dockers MariaDB to all its data.

in config sql host needs to be 127.0.0.1



I added a sql container so you don't need to use alpha-core. 

in config sql host needs to be sql

you can start this by: docker compose --profile sql up



If you want to develop, just start docker and edit files in app dir, and reload the webpage.

to start docker just run in terminal: docker-compose up

app dir will be mounted as '/opt/playermap' inside the docker container.

if you having trouble accessing alpha-core MariaDB, add 'hostname: sql' to Alpha-core's docker-compose, under 'sql' section.



All creatures in Alpha-core spawned





**All creatures in Alpha-core spawned**

![screen1](https://raw.githubusercontent.com/diff3/playermap-flask/main/app/wiki/screen1.png)

