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

* Install `Docker for Mac <https://www.docker.com/products/docker#/mac>`_.
* If you are using Docker Toolbox, switch to Docker for Mac.

On Ubuntu:

* If you have difficulties with the ``apt`` install, try the ``pip`` install.
* The docker group is automatically created. `Adding your user to the docker
  group <https://docs.docker.com/engine/installation/linux/linux-postinstall/#manage-docker-as-a-non-root-user>`_
  avoids having to use sudo to run docker commands. Note that depending on how
  users/groups are set up, you may need to manually need to add your user to the
  group in ``/etc/group``.

While Docker is available on other platforms (e.g., `Windows <https://docs.docker.com/engine/installation/windows/>`_,
`Red Hat Enterprise Linux <https://docs.docker.com/engine/installation/linux/rhel/>`_), the SFM team does not have any experience running
SFM on those platforms.

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

``docker-compose build``    Build images for all of the containers specified in the docker-compose.yml file with the `build` field. Add ``--no-cache``
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

.. _docker-scaling:

------------------------
 Scaling up with Docker
------------------------

Most harvesters and exporters handle one request at a time; requests for exports and harvests queue up waiting
to be handled. If requests are taking too long to be processed you can scale up (i.e., create additional
instances of) the appropriate harvester or exporter.

To create multiple instances of a service, use `docker-compose scale <https://docs.docker.com/compose/reference/scale/>`_.

The harvester most likely to need scaling is the Twitter REST harvester since some harvests (e.g., broad Twitter
searches) may take a long time. To scale up the Twitter REST harvester to 3 instances use::

    docker-compose scale twitterrestharvester=3

To spread containers across multiple containers, use `Docker Swarm <https://docs.docker.com/swarm/overview/>`_.

`Using compose in production <https://docs.docker.com/compose/production/>`_ provides
some additional guidance.

.. _docker-stopping:

---------------------------------------------
 Stopping Docker from automatically starting
---------------------------------------------

Docker automatically starts when the server starts. To control this:

Ubuntu 14 (Upstart)
^^^^^^^^^^^^^^^^^^^
Stop Docker from automatically starting::

    echo manual | sudo tee /etc/init/docker.override

Allow Docker to automatically start::

    sudo rm /etc/init/docker.override

Manually start Docker::

    sudo service docker start

Ubuntu 16 (Systemd)
^^^^^^^^^^^^^^^^^^^
Stop Docker from automatically starting::

    sudo systemctl disable docker

Allow Docker to automatically start::

    sudo systemctl enable docker

Manually start Docker::

    sudo systemctl start docker
