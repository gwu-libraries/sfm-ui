=================
 Troubleshooting
=================

--------------
 General tips
--------------

* Upgrade to the latest version of Docker and Docker-Compose.
* Make sure expected containers are running with ``docker ps``.
* Check the logs with ``docker-compose logs`` and ``docker logs <container name>``.
* Additional information is available via the admin interface that is not available from the UI.
  To access the admin interface, log in as an account that has superuser status and under "Welcome, <your name>,"
  click Admin. By default, a superuser account called `sfmadmin` is created. The password can be found in ``.env``.


-------------------
 Specific problems
-------------------

Skipped harvests
^^^^^^^^^^^^^^^^
A new harvest will not be requested if the previous harvest has not completed. Instead, a harvest record will be created
with the status of skipped. Some of the reasons that this might happen include:

* Harvests are scheduled too closely together, such that the previous harvest cannot complete before the new harvest is requested.
* There are not enough running harvesters, such that harvest requests have to wait too long before being processed.
* There is a problem with harvesters, such that they are not processing harvest requests.
* Something else has gone wrong, and a harvest request was not completed.

After correcting the problem to resume harvesting for a collection, void the last (non-skipped) harvest. To void a
harvest, go to that harvest's detail page and click the void button.

Connection errors when harvesting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If harvests from a container fail with something like::

    HTTPSConnectionPool(host='api.flickr.com', port=443): Max retries exceeded with url: /services/rest/?user_id=148553609%40N08&nojsoncallback=1&method=flickr.people.getInfo&format=json (Caused by ProxyError('Cannot connect to proxy.', error('Tunnel connection failed: 500 [Errno -3] Temporary failure in name resolution',)))

then stop and restart the container.  For example::

    docker-compose stop flickrharvester
    docker-compose up -d

Bind error
^^^^^^^^^^
If when bringing up the containers you receive something like::

    ERROR: driver failed programming external connectivity on endpoint docker_sfmuiapp_1 (98caab29b4ba3c2b08f70fdebad847980d80a29a2c871164257e454bc582a060): Bind for 0.0.0.0:8080 failed: port is already allocated

it means another application is already using a port configured for SFM. Either shut down the other application
or choose a different port for SFM. (Chances are the other application is Apache.)

Bad Request (400)
^^^^^^^^^^^^^^^^^
If you receive a Bad Request (400) when trying to access SFM, your ``SFM_HOSTNAME`` environment variable is not
configured correctly. Check what ``SFM_HOSTNAME`` is set to in ``.env``, and update and restart (``docker-compose stop ui`` then ``docker-compose up -d``) if necessary. For more information, see `ALLOWED_HOSTS <https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-ALLOWED_HOSTS>`_.

Social Network Login Failure for Twitter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you receive a Social Network Login Failure when trying to connect a Twitter account, make sure that the Twitter app
from which you got the Twitter credentials is configured with a callback URL. The URL should be *http://<SFM hostname>/accounts/twitter/login/callback/*.

If you have made a change to the credentials configured in ``.env``, try deleting twitter from Social Applications in the admin interface and restarting SFM UI (``docker-compose stop ui`` then ``docker-compose up -d``).

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

CSV export problems
^^^^^^^^^^^^^^^^^^^
Excel for Mac has problems with unicode characters in CSV files. As a work-around, export to Excel (XLSX) format.

--------------
 Still stuck?
--------------

`Contact <http://gwu-libraries.github.io/sfm-ui/contact>`_ the SFM team. We're happy to help.
