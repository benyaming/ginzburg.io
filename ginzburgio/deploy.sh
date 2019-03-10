#!/usr/bin/env bash
docker stop ginzburgio || true && docker rm ginzburgio || true

docker run \
  --name ginzburgio \
  --mount type=bind,source=/var/www/ginzburgio,target=/var/www/ \
  --restart always \
  -p 9000:8000 \
  -itd \
  python:3.7-stretch

docker exec ginzburgio git clone https://github.com/benyomin94/ginzburg.io /home/code/
docker exec ginzburgio pip install -r /home/code/ginzburgio/requirements.txt