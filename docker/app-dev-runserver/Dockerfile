FROM ubuntu@sha256:0844055d30c0cad5ac58097597a94640b0102f47d6fa972c94b7c129d87a44b7
#Ubuntu 14.04
MAINTAINER Rajat Vij <rajatvij@email.gwu.edu>

#This pre-fetches the most recent requirements.apt.
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-ui/master/requirements/requirements.apt /opt/sfm-setup/
RUN apt-get update
RUN cat /opt/sfm-setup/requirements.apt | tr "\n" " " | xargs apt-get install -y
RUN pip install pip==7.1.2
#This pre-fetches the most recent requirements.txt.
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-ui/master/requirements/common.txt /opt/sfm-setup/
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-ui/master/requirements/requirements.txt /opt/sfm-setup/
RUN pip install -r /opt/sfm-setup/requirements.txt
#Install appdeps to allow checking for application dependencies
RUN pip install appdeps
#This is used to automatically create the admin user.
RUN pip install django-finalware==0.1.0
#This will be copied over into the app by invoke.sh.
ADD wsgi.py /tmp/
#Adds fixtures.
ADD fixtures.json /opt/sfm-setup/
ADD invoke.sh /opt/
RUN chmod +x /opt/invoke.sh
WORKDIR /opt/sfm-ui
ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
CMD ["/opt/invoke.sh"]
EXPOSE 80