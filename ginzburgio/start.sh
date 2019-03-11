#!/usr/bin/env bash
docker exec {name of container} /bin/bash -c "
export PRODUCTION=true
export HOST_NAME={your host name or ip adress}
export SECRET_KEY=\"{secret key for csrf}\"
export ADMIN_NAME={username of site admin}
export ADMIN_MAIL={email of site admin}
export ADMIN_PASS={password of site admin}
bash
cd /home/code/ginzburgio
./manage.py makemigrations
./manage.py migrate
./manage.py test
./manage.py collectstatic --noinput
python create_admin.py | ./manage.py shell
gunicorn -c /home/code/ginzburgio/config/gunicorn_conf.py config.wsgi:application
"
