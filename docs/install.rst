================================
 Installation and configuration
================================

----------
 Overview
----------
The supported approach for deploying SFM is Docker containers.

Each SFM service will provide images for the containers needed to run the service
(in the form of ``Dockerfile`` s). These images will be published to `Docker Hub <https://hub.docker.com/>`_.
GWU created images will be part of the `GWUL organization <https://hub.docker.com/u/gwul>`_
and be prefixed with *sfm-*.

`sfm-docker <https://github.com/gwu-libraries/sfm-docker>`_ provides the necessary
``docker-compose.yml`` files to compose the services into a complete instance of SFM.

For a container, there may be multiple flavors of the container. In particular,
there may be the following:

* *development*:  The code for the service is outside the container and linked into
  the container as a shared volume. This supports development with a running instance
  of the service.
* *master*:  The container contains the master branch of the code at the time the
  image is built.
* *release*:  The container contains a release of the code. There will be a
  separate image for each release.

For more information, see :doc:`docker`.

SFM *can* be deployed without Docker. The various ``Dockerfile``s should provide
reasonable guidance on how to accomplish this.

--------------
 Dependencies
--------------
See :ref:`docker-installing`.


---------------
 Configuration
---------------

* Passwords are kept in ``secrets.env``.  A template for this file (``example.secrets.env``) is provided.
* Debug mode for sfm-ui is controlled by the ``DEBUG`` environment variable in ``docker-compose.yml``.
  If setting ``DEBUG`` to false, the ``SFM_HOST`` environment variable must be provided with the host.
  See the `Django documentation <https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts>`_
  for ``ALLOWED_HOSTS``.
* The default timezone is Eastern Standard Time (EST). To select a different timezone, change ``TZ=EST`` in
  ``docker-compose.yml``.
* Email is configured by providing the ``SFM_HOST``, ``SFM_SMTP_HOST``, ``SFM_EMAIL_USER``, and ``SFM_EMAIL_PASSWORD``
  environment variables.  ``SFM_HOST`` is used to determine the host name when constructing links contained in the emails.
* Application credentials for social media APIs are configured by providing the ``TWITTER_CONSUMER_KEY``,
  ``TWITTER_CONSUMER_SECRET``, ``WEIBO_API_KEY``, and/or ``WEIBO_API_SECRET``. For more information, see :doc:`credentials`.
* The `data volume strategy <https://docs.docker.com/engine/userguide/dockervolumes/#creating-and-mounting-a-data-volume-container>`_
  is used to manage the volumes that store SFM's data. By default, normal Docker volumes are used; to use
  a host volume instead, add the host directory to the ``volumes`` field.  This will allow you to access the
  data outside of Docker.  For example::

    sfmdata:
        image: ubuntu:14.04
        command: /bin/true
        volumes:
             - /myhost/data:/sfm-data


--------------
 Installation
--------------

1. Either clone this repository::

    git clone git@github.com:gwu-libraries/sfm-docker.git

or just download ``docker-compose.yml`` and ``example.secrets.env``::

    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/master.docker-compose.yml > docker-compose.yml
    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/example.secrets.env > secrets.env

2. Put real secrets in ``secrets.env``.

3. Bring up the containers::

    docker-compose up -d
