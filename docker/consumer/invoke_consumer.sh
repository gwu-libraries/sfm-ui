#!/bin/bash
set -e

sh /opt/sfm-setup/setup_reqs.sh
appdeps.py --wait-secs 90 --port-wait ${SFM_POSTGRES_HOST}:${SFM_POSTGRES_PORT} --file /opt/sfm-ui --port-wait ${SFM_RABBITMQ_HOST}:${SFM_RABBITMQ_PORT} --port-wait ui:8080 --file-wait /sfm-collection-set-data/collection_set

echo "Running consumer"
exec gosu sfm /opt/sfm-ui/sfm/manage.py startconsumer
