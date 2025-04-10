# start.sh

#!/bin/bash

if [ "$ENV_MODE" == "PRODUCTION" ]; then
  echo "Modo produção"
  docker-compose --env-file .env.production -f docker-compose.yml up
else
  echo "Modo dev"
  cp .env.development .env
  docker-compose up
fi