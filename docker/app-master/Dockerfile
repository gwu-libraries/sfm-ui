FROM ubuntu:14.04
MAINTAINER Rajat Vij <rajatvij@email.gwu.edu>

RUN apt-get update && apt-get install -y \
    build-essential \
    gettext \
    python-dev \
    zlib1g-dev \
    libpq-dev \
    python-pip \
    apache2 \
    libapache2-mod-wsgi \
    wget \
    zip
# Not sure why the git install needs its own line,
# but it seems to be ignored if added into the list above
RUN apt-get install -y git
#Upgrade pip
RUN pip install --upgrade pip
WORKDIR /tmp
RUN wget --no-check-certificate https://github.com/gwu-libraries/sfm-ui/archive/master.zip
RUN unzip master.zip
RUN mv sfm-ui-master /opt/sfm-ui
#This installs requirements.txt.
RUN pip install -r /opt/sfm-ui/requirements/requirements.txt --upgrade
#This is used to automatically create the admin user.
RUN pip install django-finalware==0.1.0
#Install appdeps to allow checking for application dependencies
RUN pip install appdeps
#This will be copied over into the app by invoke.sh.
ADD wsgi.py /opt/sfm-ui/sfm/sfm/
#Adds fixtures.
ADD fixtures.json /opt/sfm-setup/
#Enable sfm site
ADD apache.conf /etc/apache2/sites-available/sfm.conf
RUN a2ensite sfm.conf
#Disable pre-existing default site
RUN a2dissite 000-default
#Data volume
RUN mkdir /var/sfm && chmod ugo+w /var/sfm
VOLUME /var/sfm
ADD invoke.sh /opt/
RUN chmod +x /opt/invoke.sh
WORKDIR /opt/sfm-ui
CMD ["/opt/invoke.sh"]
ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
EXPOSE 80
