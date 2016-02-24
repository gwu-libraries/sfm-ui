FROM ubuntu@sha256:0844055d30c0cad5ac58097597a94640b0102f47d6fa972c94b7c129d87a44b7
#Ubuntu 14.04
MAINTAINER Rajat Vij <rajatvij@email.gwu.edu>

ENV sfm_ui_version 0.4.0
#This pre-fetches the most recent requirements.apt.
ADD https://raw.githubusercontent.com/gwu-libraries/sfm-ui/${sfm_ui_version}/requirements/requirements.apt /tmp/
RUN apt-get update && apt-get install -y \
    zip=3.0-8
RUN cat /tmp/requirements.apt | tr "\n" " " | xargs apt-get install -y
#Upgrade pip
RUN pip install pip==7.1.2
WORKDIR /tmp
ADD https://github.com/gwu-libraries/sfm-ui/archive/${sfm_ui_version}.zip /tmp/
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
#Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/apache2/access.log
RUN ln -sf /dev/stderr /var/log/apache2/error.log
WORKDIR /opt/sfm-ui
CMD ["/opt/invoke.sh"]
ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
EXPOSE 80
