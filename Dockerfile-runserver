FROM gwul/sfm-base@sha256:e68cb98bdc9dc23bbed734f3e507a0ffb866b007dffea038b6af8d88a62150e6
MAINTAINER Social Feed Manager <sfm@gwu.edu>

ADD . /opt/sfm-ui/
WORKDIR /opt/sfm-ui
RUN pip install -r requirements/common.txt -r requirements/release.txt

# Adds fixtures.
ADD docker/ui/fixtures.json /opt/sfm-setup/

ADD docker/ui/invoke_runserver.sh /opt/sfm-setup/
RUN chmod +x /opt/sfm-setup/invoke_runserver.sh

ADD docker/ui/setup_ui.sh /opt/sfm-setup/
RUN chmod +x /opt/sfm-setup/setup_ui.sh

ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
ENV LOAD_FIXTURES=false
EXPOSE 8000

CMD ["/opt/sfm-setup/invoke_runserver.sh"]