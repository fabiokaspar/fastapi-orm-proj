#!/bin/bash

DIR="/usr/sbin/docker-compose"
if [[ ! -e $DIR ]]; then
  echo "Installing Docker..."
  sudo yum install -y docker
  sudo chkconfig docker on
  sudo service docker start
  sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/sbin/docker-compose
fi

./start.sh