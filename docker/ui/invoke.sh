#!/bin/bash

echo "Running server"
export SFM_RUN_SCHEDULER=True
# source /etc/apache2/envvars
# old, incompletely-shutdown httpd makes the apache start incorrectly
rm -rf /run/apache2/* /tmp/httpd*
echo "start apache on foreground"
apachectl -DFOREGROUND
