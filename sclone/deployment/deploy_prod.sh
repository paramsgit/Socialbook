#!/bin/sh
current_dir=$(pwd)
echo $current_dir
echo $USER


  cd project/Socialbook
  git pull
  cd sclone
  docker-compose build
  docker-compose up -d

  exit
