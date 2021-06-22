#!/bin/bash
set -e

sh /opt/sfm-setup/setup_reqs.sh
appdeps.py --wait-secs 60 --port-wait ${SFM_POSTGRES_HOST}:${SFM_POSTGRES_PORT} --file /opt/sfm-ui --port-wait ${SFM_RABBITMQ_HOST}:${SFM_RABBITMQ_PORT} --file-wait /sfm-collection-set-data/collection_set
sh /opt/sfm-setup/setup_ui.sh

echo "Running server"
export SFM_RUN_SCHEDULER=True
exec gosu sfm /opt/sfm-ui/sfm/manage.py runserver 0.0.0.0:8080
