#!/bin/bash
echo "Waiting for db"
appdeps.py --wait-secs 30 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672
if [ "$?" = "1" ]; then
    echo "Problem with application dependencies."
    exit 1
fi

echo "Updating requirements"
pip install -r /opt/sfm-ui/requirements/requirements.txt --upgrade

export DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings

echo "Copying config"
cp /tmp/wsgi.py /opt/sfm-ui/sfm/sfm/

echo "Syncing db"
/opt/sfm-ui/sfm/manage.py syncdb --noinput

echo "Migrating db"
/opt/sfm-ui/sfm/manage.py migrate --noinput

echo "Running server"
#Not entirely sure why this is necessary, but it works.
/etc/init.d/apache2 start
#Make sure apache has started
/etc/init.d/apache2 status
while [ "$?" != "0" ];  do
    echo "Waiting for start"
    sleep 1
    /etc/init.d/apache2 status
done
echo "Stopping server"
/etc/init.d/apache2 graceful-stop
#Make sure apache has stopped
/etc/init.d/apache2 status
while [ "$?" = "0" ];  do
    echo "Waiting for stop"
    sleep 1
    /etc/init.d/apache2 status
done
echo "Starting server again"
apachectl -DFOREGROUND
