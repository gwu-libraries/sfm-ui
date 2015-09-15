FROM ubuntu:14.04
MAINTAINER Rajat Vij <rajatvij@email.gwu.edu>

LABEL Description="This image is used to start the sfm-ui executable" Vendor="GWU Libraries" Branch="t13-initial-collection-list"
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
#This pre-fetches the most recent requirements.txt.
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-ui/t14-add_seed-seed_sets/requirements/requirements.txt /opt/sfm-setup/
RUN pip install -r /opt/sfm-setup/requirements.txt
#This is used to automatically create the admin user.
RUN pip install django-finalware==0.1.0
#This will be copied over into the app by invoke.sh.
ADD wsgi.py /tmp/
#Enable sfm site
ADD apache.conf /etc/apache2/sites-available/sfm.conf
RUN a2ensite sfm.conf
#Disable pre-existing default site
RUN a2dissite 000-default
#Data volume
ADD invoke.sh /opt/
RUN chmod +x /opt/invoke.sh
#Install appdeps to allow checking for application dependencies
WORKDIR /opt/sfm-ui
RUN pip install appdeps
CMD ["/opt/invoke.sh"]
EXPOSE 80
