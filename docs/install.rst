Installation and configuration
==============================

Overview
--------
The supported approach for deploying SFM is Docker containers.

Each SFM service will provide images for the containers needed to run the service
(in the form of ``Dockerfile``s). These images will be published to `Docker Hub <https://hub.docker.com/>`_.
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

SFM *can* be deployed without Docker. The various ``Dockerfile``s should provide
reasonable guidance on how to accomplish this.

Dependencies
------------

`Docker Engine <https://www.docker.com/>`_ and `Docker Compose <https://docs.docker.com/compose/>`_

On OS X, just install the `Docker Toolbox <https://docs.docker.com/installation/mac/>`_.

Configuration
-------------

Passwords are kept in ``secrets.env``.  A template for this file (``example.secrets.env``) is provided.

Installation
------------

1. Either clone this repository::

    git clone git@github.com:gwu-libraries/sfm-docker.git

or just download ``docker-compose.yml`` and ``example.secrets.env``::

    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/master.docker-compose.yml > docker-compose.yml
    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/example.secrets.env > secrets.env

2. Put real secrets in ``secrets.env``.

3. Bring up the containers::

    docker-compose up -d

Helpful Docker commands
-----------------------

``docker ps``
    List running containers. Add ``-a`` to also list stopped containers.

``docker-compose kill``
    Stop the containers.

``docker-compose rm -v --force``
  Delete the containers and volumes.

``docker-compose logs``
    List the logs from all containers.

``docker logs <container name>``
    List the log from a single container.
