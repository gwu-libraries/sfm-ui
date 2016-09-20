FROM gwul/sfm-base@sha256:74fbacb81df7bb26f3efb67074b4b3fc2447bfd876d7197f932d08386cc068d0
MAINTAINER Justin Littman <justinlittman@gwu.edu>

# Install apache
RUN apt-get update && apt-get install -y \
    apache2=2.4.10-10+deb8u* \
    libapache2-mod-wsgi=4.3.0-1

ADD . /opt/sfm-ui/
WORKDIR /opt/sfm-ui
RUN pip install -r requirements/common.txt -r requirements/release.txt

#This is used to automatically create the admin user.
RUN pip install django-finalware==0.1.0

# Adds fixtures.
ADD docker/ui/fixtures.json /opt/sfm-setup/

# Enable sfm site
ADD docker/ui/apache.conf /etc/apache2/sites-available/sfm.conf
RUN a2ensite sfm.conf

# Disable pre-existing default site
RUN a2dissite 000-default

ADD docker/ui/invoke.sh /opt/sfm-setup/
RUN chmod +x /opt/sfm-setup/invoke.sh

ADD docker/ui/setup_ui.sh /opt/sfm-setup/
RUN chmod +x /opt/sfm-setup/setup_ui.sh

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/apache2/access.log
RUN ln -sf /dev/stderr /var/log/apache2/error.log

ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
ENV LOAD_FIXTURES=false
EXPOSE 80

CMD sh /opt/sfm-setup/setup_reqs.sh \
    && appdeps.py --wait-secs 30 --port-wait db:5432 --file /opt/sfm-ui --port-wait mq:5672 \
    && sh /opt/sfm-setup/setup_ui.sh \
    && sh /opt/sfm-setup/invoke.sh
