#!/usr/bin/env bash
docker stop {name of container} || true && docker rm {name of container} || true

docker run \
  --name {name of container} \
  --mount type=bind,source={path to your static files dir},target=/var/www/ \
  --restart always \
  -p 8000:8000 \
  -itd \
  python:3.7-stretch

docker exec {name of container} git clone https://github.com/benyomin94/ginzburg.io /home/code/
docker exec {name of container} pip install -r /home/code/ginzburgio/requirements.txt