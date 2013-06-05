#!/bin/bash
cd "$(dirname "$0")"
set -e
NUM_WORKERS=3
USER=ubuntu
source ./.src
source /home/ubuntu/venv/caiubem/bin/activate
if [ "$1" == "" ]; then
  gunicorn_django -w $NUM_WORKERS \
    --user=$USER --log-level=debug
else
  gunicorn_django -w $NUM_WORKERS \
    --user=$USER --log-level=debug \
    --log-file=$1
fi

