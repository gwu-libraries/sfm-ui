# Python 3.8.12:buster
FROM gwul/sfm-base@sha256:0b80a3d3562cdb4d631fbb55b9bd24889312838cbd27cd33e14cc0c18405f007
MAINTAINER Social Feed Manager <sfm@gwu.edu>

ARG build_version=release

# Install apache
RUN apt-get update && apt-get install -y \
    apache2=2.4* \
    apache2-dev=2.4*

ADD . /opt/sfm-ui/
WORKDIR /opt/sfm-ui
RUN python -m pip install -r requirements/common.txt -r requirements/${build_version}.txt

# Adds fixtures.
ADD docker/ui/fixtures.json /opt/sfm-setup/

# Add envvars. User and group for Apache is set in envvars.
ADD docker/ui/envvars /etc/apache2/

# Add WSGI
RUN python -m pip install mod_wsgi
ADD docker/ui/wsgi.load /etc/apache2/mods-available/wsgi.load
RUN a2enmod wsgi

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
STOPSIGNAL SIGWINCH

CMD ["/opt/sfm-setup/invoke.sh"]
