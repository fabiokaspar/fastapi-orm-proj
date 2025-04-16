#!/bin/bash

if [ "$ENV_MODE" == "production" ]; then
  cd /app/fastapi-orm-proj
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
  cp .env.production .env
  echo "Iniciando FastAPI com Uvicorn..."
  exec uvicorn main:app --host 0.0.0.0 --port 8000
else
  echo "Modo dev"
  cp .env.development .env
  docker-compose up
fi