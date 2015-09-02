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
WORKDIR /tmp
RUN wget --no-check-certificate https://github.com/gwu-libraries/sfm-ui/archive/t13-initial-collection-list.zip
RUN unzip t13-initial-collection-list.zip
RUN mv sfm-ui-t13-initial-collection-list /opt/sfm-ui
#This installs the requirements.txt.
RUN pip install -r /opt/sfm-ui/requirements/requirements.txt
#This is used to automatically create the admin user.
RUN pip install django-finalware==0.0.2
ADD common.py /tmp/
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
#Install appdeps to allow checking for application dependencies
WORKDIR /opt/sfm-ui
RUN wget -L --no-check-certificate https://github.com/gwu-libraries/appdeps/raw/master/appdeps.py
CMD ["/opt/invoke.sh"]
EXPOSE 80
