#!/bin/bash

if [ "$ENV_MODE" == "production" ]; then
  cd /app
fi

DIR_VENV="./venv"
if [[ ! -e $DIR_VENV ]]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  echo "Activating virtual environment..."
  source venv/bin/activate
  echo "Installing dependencies..."
  pip install -r requirements.txt
else
  echo "Activating virtual environment..."
  source venv/bin/activate
fi

if [ "$ENV_MODE" == "production" ]; then
  echo "Modo produção"
  echo "Conectando ao RDS..."
  cp .env.production .env
  python3 main.py
else
  echo "Modo dev"
  cp .env.development .env
  docker-compose up
fi