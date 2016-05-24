#!/bin/bash
echo "Waiting for db"
appdeps.py --wait-secs 30 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672
if [ "$?" = "1" ]; then
    echo "Problem with application dependencies."
    exit 1
fi

export DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings

echo "Syncing db"
/opt/sfm-ui/sfm/manage.py syncdb --noinput

echo "Migrating db"
/opt/sfm-ui/sfm/manage.py migrate --noinput

echo "Collecting static files"
/opt/sfm-ui/sfm/manage.py collectstatic --noinput

echo "Loading fixtures"
/opt/sfm-ui/sfm/manage.py loaddata /opt/sfm-setup/fixtures.json

echo "Creating social apps"
/opt/sfm-ui/sfm/manage.py addsocialapp twitter ${TWITTER_CONSUMER_KEY} ${TWITTER_CONSUMER_SECRET}
/opt/sfm-ui/sfm/manage.py addsocialapp weibo ${WEIBO_API_KEY} ${WEIBO_API_SECRET}

echo "Starting message consumer"
/opt/sfm-ui/sfm/manage.py startconsumer &

echo "Running server"
export SFM_RUN_SCHEDULER=True
source /etc/apache2/envvars
apachectl -DFOREGROUND
