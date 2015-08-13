Installation and configuration
==============================

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

    git clone git@github.com:gwu-libraries/sfm.git

or just download ``docker-compose.yml`` and ``example.secrets.env``::

    curl -L https://github.com/gwu-libraries/sfm/raw/master/docker-compose.yml > docker-compose.yml
    curl -L https://github.com/gwu-libraries/sfm/raw/master/example.secrets.env > secrets.env

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
