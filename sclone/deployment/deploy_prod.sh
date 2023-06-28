#!/bin/sh
current_dir=$(pwd)
echo $current_dir
echo $USER

ssh -T ubuntu@34.239.105.141 <<EOF
  cd project/Socialbook
  git pull
  cd sclone
  sudo docker-compose build
  sudo docker-compose up -d
  sudo service nginx restart
  exit
EOF