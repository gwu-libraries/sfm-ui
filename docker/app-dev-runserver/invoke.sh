#!/bin/bash
echo "Updating packages"
apt-get install -y < /opt/sfm-ui/requirements/requirements.apt

echo "Updating requirements"
pip install -r /opt/sfm-ui/requirements/master.txt --upgrade

echo "Waiting for db"
appdeps.py --wait-secs 30 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672
if [ "$?" = "1" ]; then
    echo "Problem with application dependencies."
    exit 1
fi

echo "Copying config"
cp /tmp/wsgi.py /opt/sfm-ui/sfm/sfm/

echo "Syncing db"
/opt/sfm-ui/sfm/manage.py syncdb --noinput

echo "Migrating db"
/opt/sfm-ui/sfm/manage.py migrate --noinput

echo "Collecting static files"
/opt/sfm-ui/sfm/manage.py collectstatic --noinput

echo "Loading fixtures"
/opt/sfm-ui/sfm/manage.py loaddata /opt/sfm-setup/fixtures.json

echo "Starting message consumer"
/opt/sfm-ui/sfm/manage.py startconsumer &

echo "Running server"
/opt/sfm-ui/sfm/manage.py runserver 0.0.0.0:80
