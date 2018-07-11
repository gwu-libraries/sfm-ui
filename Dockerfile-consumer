FROM gwul/sfm-base@sha256:e68cb98bdc9dc23bbed734f3e507a0ffb866b007dffea038b6af8d88a62150e6
MAINTAINER Social Feed Manager <sfm@gwu.edu>

ADD . /opt/sfm-ui/
WORKDIR /opt/sfm-ui
RUN pip install -r requirements/common.txt -r requirements/release.txt

ADD docker/consumer/invoke_consumer.sh /opt/sfm-setup/
RUN chmod +x /opt/sfm-setup/invoke_consumer.sh

ENV DJANGO_SETTINGS_MODULE=sfm.settings.docker_settings
ENV LOAD_FIXTURES=false

CMD ["/opt/sfm-setup/invoke_consumer.sh"]