#!/usr/bin/env bash -c
docker exec ginzburgio /bin/bash "
export PRODUCTION=true
export HOST_NAME=ginzburg.io
export SECRET_KEY=fgmv1ln5qg-o2ckv%2k860u_h=rx3=8%-&-27dsoyk)rj1+b%^
bash
cd /home/code/ginzburgio
manage.py test
manage.py collectstatic
gunicorn -c /home/code/ginzburgio/config/gunicorn_conf.py config.wsgi:app
"