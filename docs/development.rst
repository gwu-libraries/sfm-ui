=============
 Development
=============

--------------------------------------
 Setting up a development environment
--------------------------------------

SFM is composed of a number of components. Development can be performed on each of the
components separately. The following describes setting up an development environment
for a component.

Step 1: Pick a development configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For SFM development, it is recommended to run components within a Docker environment
(instead of directly in your OS, not in Docker). Docker runs natively (and cleanly) on Ubuntu; on OS X
Docker requires Docker Toolbox.

Since Docker can't run natively on OS X, Docker Toolbox
runs it inside a VirtualBox VM, which is largely transparent to the user. Note that GWU's
configuration of the Cisco AnyConnect VPN client breaks Docker Toolbox. You can work
around this with `vpn_fix.sh <https://gist.github.com/arrogantrobot/120e9895db1a97038d3a>`_,
but this is less than optimal.

Depending on your development preferences and the OS you development on, you may want to
consider one of the following configurations:

* Develop locally and run Docker locally: Optimal if using an IDE and not using OS X/
  Cisco AnyConnect.
* Both develop and run Docker in an Ubuntu VM. The VM can be local (e.g., in VMWare Fusion)
  or remote Ubuntu VM (e.g., a WRLC or AWS VM): Optimal if using a text editor.
* Develop locally and run Docker in a local VM with the local code shared into the VM:
  Optimal if using an IDE.

Step 2: Install Docker and Docker Compose
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`install-dependencies`.

Step 3: Clone the component's repo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For example::

    git clone https://github.com/gwu-libraries/sfm-ui.git

Step 4: Configure `docker-compose.yml`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each SFM component should provide a development Docker image and an example `dev.docker-compose.yml`
file (in the `docker/` directory).

The development Docker image will run the component using code that is shared with container.
That is, the code is made available at container run time, rather than build time (as it is
for master or production images). This allows you to change code and have it affect the
running component if the component (e.g., a Django application) is aware of code changes. If
the component is not aware of code changes, you will need to restart the container to get the
changes (`docker kill <container name>` followed by `docker-compose up -d`).

The development `docker-compose.yml` will bring up a container running the component and containers
for any additional components that the component depends on (e.g., a RabbitMQ instance). Copy
`dev.docker-compose.yml` to `docker-compose.yml` and update it as necessary. At the very least,
you will need to change the volumes link to point to your code::

    volumes:
        - "<path of your code>:/opt/sfm-ui"

You may also need to change the defaults for exposed ports to ports that are available in
your environment.

Step 5: Run the code
^^^^^^^^^^^^^^^^^^^^
::

    cd docker
    docker-compose up -d

For additional Docker and Docker-Compose commands, see :ref:`install-helpful-docker`.

------------------
 Development tips
------------------

Admin user accounts
^^^^^^^^^^^^^^^^^^^
When running a development `docker-compose.yml`, each component should automatically
create any necessary admin accounts (e.g., a django admin for SFM UI). Check `dev.docker-compose.yml`
for the username/passwords for those accounts.

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
