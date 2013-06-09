#!/bin/bash
set -e
NUM_WORKERS=3

LOG_FILE=logs/production.log
source activate_venv
source load_local_env.sh

gunicorn_django -w $NUM_WORKERS \
--user=$USER --log-level=$LOG_LEVEL \
--log-file=$LOG_FILE
