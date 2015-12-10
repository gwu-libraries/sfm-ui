FROM ubuntu:14.04
MAINTAINER Rajat Vij <rajatvij@email.gwu.edu>

ENV sfm_ui_version 0.2.0
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
#Upgrade pip
RUN pip install --upgrade pip
WORKDIR /tmp
RUN wget --no-check-certificate https://github.com/gwu-libraries/sfm-ui/archive/${sfm_ui_version}.zip
RUN unzip ${sfm_ui_version}.zip
RUN mv sfm-ui-${sfm_ui_version} /opt/sfm-ui
#This installs requirements.txt.
RUN pip install -r /opt/sfm-ui/requirements/requirements.txt --upgrade
#This is used to automatically create the admin user.
RUN pip install django-finalware==0.1.0
#Install appdeps to allow checking for application dependencies
RUN pip install appdeps
#This will be copied over into the app by invoke.sh.
ADD wsgi.py /opt/sfm-ui/sfm/sfm/
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
