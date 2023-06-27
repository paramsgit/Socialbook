#!/bin/sh
current_dir=$(whoami)
echo $current_dir
echo $USER

ssh -T ubuntu@34.239.105.141 <<EOF
  cd project/Socialbook
  git pull
  source sclone/env/bin/activate
  pip install -r requirements.txt
  python manage.py makemigrations
  python manage.py migrate  --run-syncdb
  deactivate
  sudo docker-compose build
  sudo docker-compose up -d
  sudo service nginx restart
  exit
EOF