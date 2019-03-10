#!/usr/bin/env bash
docker exec ginzburgio /bin/bash -c "
export PRODUCTION=true
export HOST_NAME=ginzburg.io
export SECRET_KEY=\"fgmv1ln5qg-o2ckv%2k860u_h=rx3=8%-&-27dsoyk)rj1+b%^\"
export ADMIN_NAME=benyomin
export ADMIN_MAIL=benyomin.94@gmail.com
export ADMIN_PASS=123465
bash
cd /home/code/ginzburgio
./manage.py makemigrations
./manage.py migrate
./manage.py test
./manage.py collectstatic --noinput
./create_admin.py | ./manage.py shell
gunicorn -c /home/code/ginzburgio/config/gunicorn_conf.py config.wsgi:application
"
