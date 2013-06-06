#!/bin/bash
cd "$(dirname "$0")"
set -e
NUM_WORKERS=3
DEPLOY_MODE=$1
source ./load_env.sh

LOG_FILE=$LOG_DIR/$PROJ_NAME.log
source $VENV_DIR/bin/activate
source $GLOBALS_DIR/$DEPLOY_MODE.sh

gunicorn_django -w $NUM_WORKERS \
--user=$USER --log-level=$LOG_LEVEL \
--log-file=$LOG_FILE