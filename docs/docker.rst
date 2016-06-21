========
 Docker
========

This page contains information about Docker that is useful for installation,
administration, and development.

.. _docker-installing:

-------------------
 Installing Docker
-------------------

`Docker Engine <https://www.docker.com/>`_ and `Docker Compose <https://docs.docker.com/compose/>`_

On OS X:

* Install the `Docker Toolbox <https://docs.docker.com/installation/mac/>`_.
* Be aware that Docker is not running natively on OS X, but rather in a
  VirtualBox VM.

On Ubuntu:

* If you have difficulties with the ``apt`` install, try the ``pip`` install.
* The docker group is automatically created. `Adding your user to the docker
  group <https://docs.docker.com/v1.8/installation/ubuntulinux/#create-a-docker-group>`_
  avoids having to use sudo to run docker commands. Note that depending on how
  users/groups are set up, you may need to manually need to add your user to the
  group in ``/etc/group``.

.. _docker-helpful:

------------------
 Helpful commands
------------------

``docker-compose up -d``
    Bring up all of the containers specified in the docker-compose.yml file. If a container has not yet been pulled,
    it will be pulled. If a container has not yet been built it will be built. If a container has been stopped ("killed")
    it will be re-started. Otherwise, a new container will be created and started ("run").

``docker-compose pull``
    Pull the latest images for all of the containers specified in the docker-compose.yml file with the `image` field.

``docker-compose build``
    Build images for all of the containers specified in the docker-compose.yml file with the `build` field. Add ``--no-cache``
    to re-build the entire image (which you might want to do if the image isn't building as expected).

``docker ps``
    List running containers. Add ``-a`` to also list stopped containers.

``docker-compose kill``
    Stop all containers.

``docker kill <container name>``
    Stop a single container.

``docker-compose rm -v --force``
    Delete the containers and volumes.

``docker rm -v <container name>``
    Delete a single container and volume.

``docker rm $(docker ps -a -q) -v``
    Delete all containers.

``docker-compose logs``
    List the logs from all containers. Add ``-f`` to follow the logs.

``docker logs <container name>``
    List the log from a single container. Add ``-f`` to follow the logs.

``docker-compose -f <docker-compose.yml filename> <command>``
    Use a different docker-compose.yml file instead of the default.

``docker exec -it <container name> /bin/bash``
    Shell into a container.

``docker rmi <image name>``
    Delete an image.

``docker rmi $(docker images -q)``
    Delete all images

``docker-compose scale <service name>=<number of instances>``
    Create multiple instances of a service.


------------------------
 Scaling up with Docker
------------------------
To create multiple instances of a service, use `docker-compose scale <https://docs.docker.com/compose/reference/scale/>`_.
This can be used to created multiple instances of a harvester when the queue for
that harvester is too long.

To spread containers across multiple containers, use `Docker Swarm <https://docs.docker.com/swarm/overview/>`_.

`Using compose in production <https://docs.docker.com/compose/production/>`_ provides
some additional guidance.