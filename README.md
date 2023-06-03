# Online player map for Alpha-core.

The easiest way to start Playermap-flask, is to first start Alpha-core, Playermap-flask uses alpha-core dockers MariaDB to all its data.

If you want to develop, just start docker and edit files in app dir, and reload the webpage.

to start docker just run in terminal:
docker-compose up

app dir will be mounted as '/opt/playermap' inside the docker container.

if you having trouble accessing alpha-core MariaDB, add 'hostname: sql' to Alpha-core's docker-compose, under 'sql' section.


docker compose --profile sql up

**All creatures in Alpha-core spawned**

![screen1](https://raw.githubusercontent.com/diff3/playermap-flask/main/app/wiki/screen1.png)
