=============
 Development
=============

--------------------------------------
 Setting up a development environment
--------------------------------------

SFM is composed of a number of components. Development can be performed on each of the
components separately.

For SFM development, it is recommended to run components within a Docker environment
(instead of directly in your OS, without Docker).

Step 1: Install Docker and Docker Compose
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`docker-installing`.

Step 2: Clone sfm-docker and create copies of docker-compose files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For example::

    git clone https://github.com/gwu-libraries/sfm-docker.git
    cd sfm-docker
    cp example.docker-compose.yml docker-compose.yml
    cp example.env .env

For the purposes of development, you can make changes to ``docker-compose.yml``
and ``.env``. This will be described more below.


Step 3: Clone the component repos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For example::

    git clone https://github.com/gwu-libraries/sfm-ui.git

Repeat for each of the components that you will be working on. Each of these should
be in a sibling directory of sfm-docker.

-----------------------------
 Running SFM for development
-----------------------------

To bring up an instance of SFM for development, change to the sfm-docker directory and execute::

    docker-compose up -d

You may not want to run all of the containers. To omit a container, simply comment it out in ``docker-compose.yml``.

By default, the code that has been committed to master for each of the containers will be executed. To execute
your local code (i.e., the code you are editing), you will want to link in your local code. To link in the local
code for a container, uncomment the volume definition that points to your local code. For example::

        volumes:
            - "../sfm-twitter-harvester:/opt/sfm-twitter-harvester"

sfm-utils and warcprox are dependencies of many components. By default, the code that has been committed to master
for sfm-utils or warcprox will be used for a component. To use your local code as a dependency, you will want
to link in your local code. Assuming that you have cloned sfm-utils and warcprox, to link in the local code
as a dependency for a container, change ``SFM_REQS`` in ``.env`` to "dev" and comment the volume definition
that points to your local code. For example::

        volumes:
            - "../sfm-twitter-harvester:/opt/sfm-twitter-harvester"
            - "../sfm-utils:/opt/sfm-utils"
            - "../warcprox:/opt/warcprox"

Note:
* As a Django application, SFM UI will automically detect code changes and reload. Other components must be killed 
and brought back up to reflect code changes.

---------------
 Running tests
---------------

Unit tests
^^^^^^^^^^
Some components require a ``test_config.py`` file that contains credentials. For example, sfm-twitter-harvester
requires a ``test_config.py`` containing::

    TWITTER_CONSUMER_KEY = "EHdoTksBfgGflP5nUalEfhaeo"
    TWITTER_CONSUMER_SECRET = "ZtUpemtBkf2cEmaqiy52Dd343ihFu9PAiLebuMOmqN0QtXeAlen"
    TWITTER_ACCESS_TOKEN = "411876914-c2yZjbk1np0Z5MWEFYYQKSQNFFGBXd8T4k90YkJl"
    TWITTER_ACCESS_TOKEN_SECRET = "jK9QOmn5VRF5mfgAN6KgfmCKRqThXVQ1G6qQg8BCejvp"

Note that if this file is not present, unit tests that require it will be skipped. Each component's README
will describe the ``test_config.py`` requirements.

Also note that some unit tests may fail unless the local environment contains an `LC_ALL` environment variable
set to `en_US.UTF-8`.

Unit tests for most components can be run with::

    python -m unittest discover

The notable exception is SFM UI, which can be run with::

    cd sfm
    ./manage.py test --settings=sfm.settings.test_settings

Integration tests
^^^^^^^^^^^^^^^^^
Many components have integration tests, which are run inside docker containers. These components
have a ``ci.docker-compose.yml`` file which can be used to bring up a minimal environment for
running the tests.

As described above, some components require a ``test_config.py`` file.

To run integration tests, bring up SFM::

    docker-compose -f docker/dev.docker-compose.yml up -d

Run the tests::

    docker exec docker_sfmtwitterstreamharvester_1 python -m unittest discover

You will need to substitute the correct name of the container. (``docker ps`` will list
the containers.)

And then clean up::

    docker-compose -f docker/dev.docker-compose.yml kill
    docker-compose -f docker/dev.docker-compose.yml rm -v --force

For reference, see each component's ``.travis.yml`` file which shows the steps of running
the integration tests.

Smoke tests
^^^^^^^^^^^
sfm-docker contains some smoke tests which will verify that a development instance of SFM is running correctly.

To run the smoke tests, first bring up SFM::

    docker-compose -f example.docker-compose.yml -f smoketests.docker-compose.yml up -d

wait, and then run the tests::

    docker-compose -f example.docker-compose.yml -f smoketests.docker-compose.yml run --rm smoketests /bin/bash -c "appdeps.py --port-wait mq:5672 --port-wait ui:8080 && python -m unittest discover"

Note that the smoke tests are not yet complete and require test fixtures that are only available in a development deploy.

For reference, the `continuous integration deploy instructions <https://github.com/gwu-libraries/sfm-ui/wiki/Continuous-integration-deploy>`_
shows the steps of running the smoke tests.

--------------------
 Requirements files
--------------------

This will vary a depending on whether a project has warcprox and sfm-utils as a dependency, but in general:

* ``requirements/common.txt`` contains dependencies, except warcprox and sfm-utils.
* ``requirements/release.txt`` references the last released version of warcprox and sfm-utils.
* ``requirements/master.txt`` references the master version of warcprox and sfm-utils.
* ``requirements/dev.txt`` references local versions of warcprox and sfm-utils in development mode.

To get a complete set of dependencies, you will need ``common.txt`` and either ``release.txt``, ``master.txt`` or ``dev.txt``.
For example::

    virtualenv ENV
    source ENV/bin/activate
    pip install -r requirements/common.txt -r requirements/dev.txt

------------------
 Development tips
------------------

Admin user accounts
^^^^^^^^^^^^^^^^^^^
Each component should automatically create any necessary admin accounts (e.g., a django
admin for SFM UI). Check ``.env`` for the username/passwords for those accounts.

RabbitMQ management console
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The RabbitMQ management console can be used to monitor the exchange of messages. In particular, use it
to monitor the messages that a component sends, create a new queue, bind that queue to `sfm_exchange`
using an appropriate routing key, and then retrieve messages from the queue.

The RabbitMQ management console can also be used to send messages to the exchange so that
they can be consumed by a component. (The exchange used by SFM is named `sfm_exchange`.)

For more information on the RabbitMQ management console, see :ref:`messaging-rabbitmq`.

Blocked ports
^^^^^^^^^^^^^
When running on a remote VM, some ports (e.g., 15672 used by the RabbitMQ management console) may
be blocked. `SSH port forwarding <https://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding>`_
can help make those ports available.

Django logs
^^^^^^^^^^^
Django logs for SFM UI are written to the Apache logs. In the docker environment, the level of various
loggers can be set from environment variables.  For example, setting `SFM_APSCHEDULER_LOG` to `DEBUG`
in the `docker-compose.yml` will turn on debug logging for the apscheduler logger. The logger for
the SFM UI application is called ui and is controlled by the `SFM_UI_LOG` environment variable.

Apache logs
^^^^^^^^^^^
In the SFM UI container, Apache logs are sent to stdout/stderr which means they can be viewed with
`docker-compose logs` or `docker logs <container name or id>`.

Initial data
^^^^^^^^^^^^
The development and master docker images for SFM UI contain some initial data. This includes a user ("testuser",
with password "password"). For the latest initial data, see `fixtures.json`. For more information on fixtures,
see the `Django docs <https://docs.djangoproject.com/en/1.8/howto/initial-data/>`_.

Runserver
^^^^^^^^^
There are two flavors of the the development docker image for SFM UI.  `gwul/sfm-ui:master` runs SFM UI with
Apache, just as it will in production.  `gwul/sfm-ui:master-runserver` runs SFM UI with `runserver <https://docs.djangoproject.com/en/1.8/ref/django-admin/#runserver-port-or-address-port>`_,
which dynamically reloads changed Python code. To switch between them, change `UI_TAG` in `.env`.

Note that as an byproduct of how runserver dynamically reloads Python code, there are actually 2 instances of the application
running. This may produce some odd results, like 2 schedulers running. This will not occur with Apache.

Job schedule intervals
^^^^^^^^^^^^^^^^^^^^^^
To assist with testing and development, a 5 minute interval can be added by setting `SFM_FIVE_MINUTE_SCHEDULE` to
`True` in the `docker-compose.yml`.

Connecting to the database
^^^^^^^^^^^^^^^^^^^^^^^^^^
To connect to postgres using psql::

    docker exec -it sfm_db_1 psql -h db -U postgres -d sfmdatabase

You will be prompted for the password, which you can find in `.env`.

.. _install-helpful-docker:

-------------
 Docker tips
-------------

Building vs. pulling
^^^^^^^^^^^^^^^^^^^^
Containers are created from images. Images are either built locally or pre-built and pulled from
`Docker Hub <https://hub.docker.com/>`_. In both cases, images are created based on the docker build (i.e., the
Dockerfile and other files in the same directory as the Dockerfile).

In a docker-compose.yml, pulled images will be identified by the `image` field, e.g., `image: gwul/sfm-ui:master`. Built images
will be identified by the `build` field, e.g., `build: app-dev`.

In general, you will want to use pulled images. These are automatically built when changes are made to the Github repos.
You should periodically execute `docker-compose pull` to make sure you have the latest images.

You may want to build your own image if your development requires a change to the docker build (e.g., you modify
fixtures.json).

Killing, removing, and building in development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Killing a container will cause the process in the container to be stopped. Running the container again will cause
process to be re-started. Generally, you will kill and run a development container to get the process to be run
with changes you've made to the code.

Removing a container will delete all of the container's data. During development, you will remove a container to make
sure you are working with a clean container.

Building a container creates a new image based on the Dockerfile. For a development image, you only need to build
when making changes to the docker build.
