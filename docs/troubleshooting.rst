=================
 Troubleshooting
=================

--------------
 General tips
--------------

* Upgrade to the latest version of Docker and Docker-Compose.
* Make sure expected containers are running with ``docker ps``.
* Check the logs with ``docker-compose logs`` and ``docker logs <container name>``.


-------------------
 Specific problems
-------------------

Bind error
^^^^^^^^^^
If when bringing up the containers you receive something like::

    ERROR: driver failed programming external connectivity on endpoint docker_sfmuiapp_1 (98caab29b4ba3c2b08f70fdebad847980d80a29a2c871164257e454bc582a060): Bind for 0.0.0.0:8080 failed: port is already allocated

it means another application is already using a port configured for SFM. Either shut down the other application
or choose a different port for SFM. (Chances are the other application is Apache.)

Bad Request (400)
^^^^^^^^^^^^^^^^^
If you receive a Bad Request (400) when trying to access SFM, your ``SFM_HOST`` environment variable is not
configured correctly. For more information, see `ALLOWED_HOSTS <https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-ALLOWED_HOSTS>`_.

Docker problems
^^^^^^^^^^^^^^^
If you are having problems bringing up the Docker containers (e.g., ``driver failed programming external connectivity on endpoint``),
restart the Docker service.  On Ubuntu, this can be done with::

    # service docker stop
    docker stop/waiting
    # service docker status
    docker stop/waiting
    # service docker start
    docker start/running, process 15039


--------------
 Still stuck?
--------------

`Contact <http://gwu-libraries.github.io/sfm-ui/contact>`_ the SFM team. We're happy to help.
