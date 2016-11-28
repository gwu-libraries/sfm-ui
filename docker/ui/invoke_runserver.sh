#!/bin/bash

echo "Starting message consumer"
gosu sfm /opt/sfm-ui/sfm/manage.py startconsumer &

echo "Running server"
export SFM_RUN_SCHEDULER=True
gosu sfm /opt/sfm-ui/sfm/manage.py runserver 0.0.0.0:8080