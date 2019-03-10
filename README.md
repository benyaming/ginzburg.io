# ginzburg.io

Simple blog written on django

## Deployment

### Prerequisites
- create a directory for static files, for exemple /var/www/mycoolsite
- set up your web server. Example for nginx:
```
server {
  listen 443 ssl;
  # may be more settings here
  location /static/ {
    root {your_static_folder_path};
  }

  location /media/ {
    root {your_static_folder_path};
  }

  location / {
    proxy_pass http://127.0.0.1:8000/;
    proxy_set_header Host $host;
  }
}
```
- install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)


### Installing

1) [Download](https://github.com/benyomin94/ginzburg.io/blob/master/ginzburgio/deploy.sh) deployment script
2) Edit it with your params. Here is my example:
```
docker run \
  --name ginzburgio \
  --mount type=bind,source=/var/www/ginzburgio,target=/var/www/ \
  --restart always \
  -p 9000:8000 \
  -itd \
  python:3.7-stretch

docker exec ginzburgio git clone https://github.com/benyomin94/ginzburg.io /home/code/
docker exec ginzburgio pip install -r /home/code/ginzburgio/requirements.txt
```
3) run `chmod +x deploy.sh` and run the script



### Runing 

1) [Download](https://github.com/benyomin94/ginzburg.io/blob/master/ginzburgio/start.sh) start script
2) Edit it with your params. Here is my example:
```
#!/usr/bin/env bash
docker exec ginzburgio /bin/bash -c "
export PRODUCTION=true
export HOST_NAME=ginzburg.io
export SECRET_KEY=\"fgmv1lx3=8%-&-27dsoyk)rj1+b%^\"
export ADMIN_NAME=benyomin
export ADMIN_MAIL=benyomin@ginzburg.io
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
```
3) run `chmod +x start.sh` and run the script
