#!/bin/sh
current_dir=$(pwd)
echo $current_dir
echo $USER


  cd project/Socialbook
  git pull
  cd sclone
  sudo docker-compose build
  sudo docker-compose up -d

  exit
