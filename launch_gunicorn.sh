#!/bin/bash
cd "$(dirname "$0")"
set -e
NUM_WORKERS=3
USER=xande
GROUP=xande
source ./.src
source ./venv/bin/activate
if [ "$1" == "" ]; then
  gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug
else
  gunicorn_django -w $NUM_WORKERS \
    --user=$USER --group=$GROUP --log-level=debug \
    --log-file=$1
fi

