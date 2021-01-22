#!/bin/bash
set -e

sh /opt/sfm-setup/setup_reqs.sh
appdeps.py --wait-secs 60 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672  --file-wait /sfm-collection-set-data/collection_set
sh /opt/sfm-setup/setup_ui.sh

echo "Running server"
export SFM_RUN_SCHEDULER=True
source /etc/apache2/envvars
mkdir -p $APACHE_RUN_DIR
# old, incompletely-shutdown httpd makes the apache start incorrectly
rm -rf /run/apache2/* /tmp/httpd*

echo "start apache"
exec apache2 -DFOREGROUND
