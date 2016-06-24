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
``docker-compose.yml`` files to compose the services into a complete instance of SFM. The latest production release is ``prod.docker-compose.yml``.

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

.. _install-configuration:
---------------
 Configuration
---------------

* Passwords are kept in ``secrets.env``.  A template for this file (``example.secrets.env``) is provided.
* Application credentials for social media APIs are configured by providing the ``TWITTER_CONSUMER_KEY``,
  ``TWITTER_CONSUMER_SECRET``, ``WEIBO_API_KEY``, and/or ``WEIBO_API_SECRET``. For more information and alternative approaches see :doc:`credentials`.
* Debug mode for sfm-ui is controlled by the ``DEBUG`` environment variable in ``docker-compose.yml``.
  If setting ``DEBUG`` to false, the ``SFM_HOST`` environment variable must be provided with the host.
  See the `Django documentation <https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts>`_
  for ``ALLOWED_HOSTS``.
* The default timezone is America/New_York (EST/EDT). To select a different timezone, change ``TZ=America/New_York`` in
  ``docker-compose.yml``.
* Email is configured by providing the ``SFM_HOST``, ``SFM_SMTP_HOST``, ``SFM_EMAIL_USER``, and ``SFM_EMAIL_PASSWORD``
  environment variables.  ``SFM_HOST`` is used to determine the host name when constructing links contained in the emails.

* The `data volume strategy <https://docs.docker.com/engine/userguide/dockervolumes/#creating-and-mounting-a-data-volume-container>`_
  is used to manage the volumes that store SFM's data. By default, normal Docker volumes are used; to use
  a host volume instead, add the host directory to the ``volumes`` field.  This will allow you to access the
  data outside of Docker.  For example::

    sfmdata:
        image: ubuntu:14.04
        command: /bin/true
        volumes:
             - /myhost/data:/sfm-data


--------------------
 Local installation
--------------------

Installing locally requires Docker and Docker-Compose. See :ref:`docker-installing`.

1. Either clone this repository::

    git clone git@github.com:gwu-libraries/sfm-docker.git

or just download ``docker-compose.yml`` and ``example.secrets.env``::

    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/prod.docker-compose.yml > docker-compose.yml
    curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/example.secrets.env > secrets.env

2. Put real secrets in ``secrets.env`` as described in :ref:`install-configuration`.

3. Update ``docker-compose.yml``. It is annotated with the various configuration options, see :ref:`install-configuration`. At the least,
   set the ``SFM_HOST`` environment variable with the host/IP and the port.

4. Bring up the containers::

    docker-compose up -d


Notes:

* There is an example ``docker-compose.yml`` file for running the latest master code called ``master.docker-compose.yml``
  that can be used instead of ``prod.docker-compose.yml``.
* The first time you bring up the containers, their images will be pulled from `Docker Hub <https://hub.docker.com>`_.
  This will take several minutes.

-------------------------
 Amazon EC2 installation
-------------------------
To launch an Amazon EC2 instance running SFM, follow the normal procedure for launching an instance.
In *Step 3: Configure Instance Details*, under *Advanced Details* paste the following in
user details and modify as appropriate::

    #cloud-config
    repo_update: true
    repo_upgrade: all

    packages:
     - python-pip

    runcmd:
     - curl -sSL https://get.docker.com/ | sh
     - usermod -aG docker ubuntu
     - pip install -U docker-compose
     - mkdir /sfm-data
    # This brings up the latest production release. To bring up master, replace prod with master.
     - curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/prod.docker-compose.yml > docker-compose.yml
     - curl -L https://github.com/gwu-libraries/sfm-docker/raw/master/example.secrets.env > secrets.env
    # Set secrets below. Secrets that are not commented out are required.
    # Secrets that are commented out are not required. To include, remove the #.
    # Don't forget to escape $ as \$.
    # The password used for logging into the Rabbit Admin. Username is sfm_user.
     - echo RABBITMQ_DEFAULT_PASS=password >> secrets.env
    # Postgres password.
     - echo POSTGRES_PASSWORD=password >> secrets.env
    # The password for the admin account for SFM UI. Username is sfmadmin.
     - echo SFM_SITE_ADMIN_PASSWORD=password >> secrets.env
    # The account used to send email via SMTP from SFM UI.
    # - echo SFM_EMAIL_USER=justinlittman@email.gwu.edu >> secrets.env
    # - echo SFM_EMAIL_PASSWORD=password >> secrets.env
    # The password used to log into the Heritrix UI. Username is sfm_user.
     - echo HERITRIX_PASSWORD=password >> secrets.env
    # API keys for allowing users to connect to social media platform APIs.
    # If not provided, credentials can still be provided in SFM UI.
    # - echo TWITTER_CONSUMER_KEY=EHdoeW7ksBgflP5nUalEfhao >> secrets.env
    # - echo TWITTER_CONSUMER_SECRET=ZtUemftBkf2cEmaqiyW2Ddihu9FPAiLebuMOmqN0jeQtXeAlen >> secrets.env
    # - echo WEIBO_API_KEY=1313340598 >> secrets.env
    # - echo WEIBO_API_SECRET=68ae6a497f2f6eac07ec14bf7c0e0fa52 >> secrets.env
    # Values must be provided for all of the following.
    # HERITRIX_CONTACT_URL is included in the HTTP request when harvesting web
    # resources with Heritrix.
     - export HERITRIX_CONTACT_URL=http://library.gwu.edu
    # The following are optional.
    # The SMTP server used to send email.
     - export SMTP_HOST=smtp.gmail.com
    # The email address of the admin account for SFM UI.
     - export SITE_ADMIN_EMAIL=nowhere@example.com
    # The time zone.
     - export TZ=America/New_York
    # The host name of the server.
     - export HOST=`curl http://169.254.169.254/latest/meta-data/public-hostname`
     - sed -i 's/\/sfm-data/"\/sfm-data:\/sfm-data"/' docker-compose.yml
     - sed -i "s/HERITRIX_CONTACT_URL=http:\/\/library.gwu.edu/HERITRIX_CONTACT_URL=${HERITRIX_CONTACT_URL}/" docker-compose.yml
     - sed -i "s/SFM_SMTP_HOST=smtp.gmail.com/SFM_SMTP_HOST=${SMTP_HOST}/" docker-compose.yml
     - sed -i "s/SFM_SITE_ADMIN_EMAIL=nowhere@example.com/SFM_SITE_ADMIN_EMAIL=${SITE_ADMIN_EMAIL}/" docker-compose.yml
     - sed -i "s/TZ=EST/TZ=${TZ}/g" docker-compose.yml
     - sed -i "s/SFM_HOST=sfm.gwu.edu:8080/SFM_HOST=${HOST}/" docker-compose.yml
     - docker-compose up -d

When the instance is launched, SFM will be installed and started.

Note the following:

* Starting up the EC2 instance will take several minutes.
* This has been tested with *Ubuntu Server 14.04 LTS*, but may work with other AMI types.
* We don't have recommendations for sizing, but providing multiple processors even for
  testing/experimentation.
* If you need to make additional changes to your ``docker-compose.yml``, you can ssh into the EC2 instance
  and make changes.  ``docker-compose.yml`` and ``secrets.env`` will be in the default user's
  home directory.
* Make sure to configure a security group that exposes the proper ports. To see which
  ports are used by which services, see `master.docker-compose.yml <https://github.com/gwu-libraries/sfm-docker/blob/master/master.docker-compose.yml>`_.
* To learn more about configuring EC2 instances with user data, see the `AWS user guide <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html>`_.
