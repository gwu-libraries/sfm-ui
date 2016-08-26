#!/bin/bash

echo "Starting message consumer"
/opt/sfm-ui/sfm/manage.py startconsumer &

echo "Running server"
export SFM_RUN_SCHEDULER=True
/opt/sfm-ui/sfm/manage.py runserver 0.0.0.0:80