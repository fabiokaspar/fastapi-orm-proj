#!/bin/bash

DIR_VENV="./venv"
if [[ ! -e $DIR_VENV ]]; then
  echo "Creating virtual environment..."
  python -m venv venv
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
  docker-compose --env-file .env.production -f docker-compose.yml up
else
  echo "Modo dev"
  cp .env.development .env
  docker-compose up
fi