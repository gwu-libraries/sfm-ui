================================
 Installation and configuration
================================

----------
 Overview
----------
The supported approach for deploying SFM is Docker containers. For more information on Docker, see :doc:`docker`.

Each SFM service will provide images for the containers needed to run the service
(in the form of ``Dockerfile`` s). These images will be published to `Docker Hub <https://hub.docker.com/>`_.
GWU created images will be part of the `GWUL organization <https://hub.docker.com/u/gwul>`_
and be prefixed with *sfm-*.

`sfm-docker <https://github.com/gwu-libraries/sfm-docker>`_ provides the necessary
``docker-compose.yml`` files to compose the services into a complete instance of SFM.

The following will describe how to setup an instance of SFM that uses the latest release
(and is suitable for a production deployment.) See the development documentation for other
SFM configurations.

SFM *can* be deployed without Docker. The various ``Dockerfile`` s should provide
reasonable guidance on how to accomplish this.


--------------------
 Local installation
--------------------

Installing locally requires Docker and Docker-Compose. See :ref:`docker-installing`.

1. Either clone the sfm-docker repository and copy the example configuration files::

    git clone https://github.com/gwu-libraries/sfm-docker.git
    cd sfm-docker
    # Replace 1.7.0 with the correct version.
    git checkout 1.7.0
    cp example.prod.docker-compose.yml docker-compose.yml
    cp example.env .env

or just download ``example.prod.docker-compose.yml`` and ``example.env`` (replacing 1.7.0 with the correct version)::

    curl -L https://raw.githubusercontent.com/gwu-libraries/sfm-docker/1.7.0/example.prod.docker-compose.yml > docker-compose.yml
    curl -L https://raw.githubusercontent.com/gwu-libraries/sfm-docker/1.7.0/example.env > .env

2. Update configuration in ``.env`` as described in :ref:`install-configuration`.

3. Bring up the containers::

    docker-compose up -d

It may take several minutes for the images to be downloaded and the containers to start.

4. It is also recommended that you scale up the Twitter REST Harvester container::

    docker-compose scale twitterrestharvester=2

Notes:

* The first time you bring up the containers, their images will be pulled from `Docker Hub <https://hub.docker.com>`_. This will take several minutes.
* For instructions on how to make configuration changes *after* the containers have been brought up, see :ref:`install-configuration`.
* To learn more about scaling , see :ref:`docker-scaling`.
* For suggestions on sizing your SFM server, see :ref:`server-sizing`.

-------------------------
 Amazon EC2 installation
-------------------------
To launch an Amazon EC2 instance running SFM, follow the normal procedure for launching an instance.
In *Step 3: Configure Instance Details*, under *Advanced Details* paste the following in
user details and modify as appropriate as described in :ref:`install-configuration`. Also, in the curl
statements change *master* to the correct version, e.g., *1.7.0*::

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
     - mkdir /sfm-processing
     - cd /home/ubuntu
    # This brings up the latest production release. To bring up master, remove prod.
     - curl -L https://raw.githubusercontent.com/gwu-libraries/sfm-docker/1.7.0/example.prod.docker-compose.yml > docker-compose.yml
     - curl -L https://raw.githubusercontent.com/gwu-libraries/sfm-docker/1.7.0/example.env > .env
    # Set config below by uncommenting.
    # Don't forget to escape $ as \$.
    # COMMON CONFIGURATION
    # - echo TZ=America/New_York >> .env
    # VOLUME CONFIGURATION
    # Don't change these.
     - echo DATA_VOLUME=/sfm-data:/sfm-data >> .env
     - echo PROCESSING_VOLUME=/sfm-processing:/sfm-processing >> .env
    # SFM UI CONFIGURATION
    # Don't change this.
     - echo SFM_HOSTNAME=`curl http://169.254.169.254/latest/meta-data/public-hostname` >> .env
     - echo SFM_PORT=80 >> .env
    # Provide your institution name display on sfm-ui footer
    # - echo SFM_INSTITUTION_NAME=yourinstitution >> .env
    # Provide your institution link
    # - echo SFM_INSTITUTION_LINK=http://library.yourinstitution.edu >> .env
    # To send email, set these correctly.
    # - echo SFM_SMTP_HOST=smtp.gmail.com >> .env
    # - echo SFM_EMAIL_USER=someone@gmail.com >> .env
    # - echo SFM_EMAIL_PASSWORD=password >> .env
    # An optional contact email at your institution that is provided to users.
    # - echo SFM_CONTACT_EMAIL=sfm@yourinstitution.edu >> .env
    # To enable connecting to social media accounts, provide the following.
    # - echo TWITTER_CONSUMER_KEY=mBbq9ruffgEcfsktgQztTHUir8Kn0 >> .env
    # - echo TWITTER_CONSUMER_SECRET=Pf28yReB9Xgz0fpLVO4b46r5idZnKCKQ6xlOomBAjD5npFEQ6Rm >> .env
    # - echo WEIBO_API_KEY=13132044538 >> .env
    # - echo WEIBO_API_SECRET=68aea49fg26ea5072ggec14f7c0e05a52 >> .env
    # - echo TUMBLR_CONSUMER_KEY=Fki09cW957y56h6fhRtCnig14QhpM0pjuHbDWMrZ9aPXcsthVQq >> .env
    # - echo TUMBLR_CONSUMER_SECRET=aPTpFRE2O7sVl46xB3difn8kBYb7EpnWfUBWxuHcB4gfvP >> .env
    # For automatically created admin account
    # - echo SFM_SITE_ADMIN_NAME=sfmadmin >> .env
    # - echo SFM_SITE_ADMIN_EMAIL=nowhere@example.com >> .env
    # - echo SFM_SITE_ADMIN_PASSWORD=password >> .env
    # RABBIT MQ CONFIGURATION
    # - echo RABBITMQ_USER=sfm_user >> .env
    # - echo RABBITMQ_PASSWORD=password >> .env
    # - echo RABBITMQ_MANAGEMENT_PORT=15672 >> .env
    # DB CONFIGURATION
    # - echo POSTGRES_PASSWORD=password >> .env
    # WEB HARVESTER CONFIGURATION
    # - echo HERITRIX_USER=sfm_user >> .env
    # - echo HERITRIX_PASSWORD=password >> .env
    # - echo HERITRIX_ADMIN_PORT=8443 >> .env
    # - echo HERITRIX_CONTACT_URL=http://library.myschool.edu >> .env
     - docker-compose up -d
     - docker-compose scale twitterrestharvester=2

When the instance is launched, SFM will be installed and started.

Note the following:

* Starting up the EC2 instance will take several minutes.
* This has been tested with *Ubuntu Server 14.04 LTS*, but may work with other AMI types.
* For suggestions on sizing your SFM server, see :ref:`server-sizing`.
* If you need to make additional changes to your ``docker-compose.yml``, you can ssh into the EC2 instance
  and make changes.  ``docker-compose.yml`` and ``.env`` will be in the default user's
  home directory.
* Make sure to configure a security group that exposes the proper ports. To see which
  ports are used by which services, see `example.prod.docker-compose.yml <https://github.com/gwu-libraries/sfm-docker/blob/master/example.prod.docker-compose.yml>`_.
* To learn more about configuring EC2 instances with user data, see the `AWS user guide <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html>`_.


.. _install-configuration:

---------------
 Configuration
---------------

Configuration is documented in ``example.env``. For a production deployment, pay particular attention to the following:

* Set new passwords for ``SFM_SITE_ADMIN_PASSWORD``, ``RABBIT_MQ_PASSWORD``, ``POSTGRES_PASSWORD``, and ``HERITRIX_PASSWORD``.
* The `data volume strategy <https://docs.docker.com/engine/userguide/dockervolumes/#creating-and-mounting-a-data-volume-container>`_
  is used to manage the volumes that store SFM's data. By default, normal Docker volumes are used. To use a host volume
  instead, change the ``DATA_VOLUME`` and ``PROCESSING_VOLUME`` settings. Host volumes are recommended for production
  because they allow access to the data from outside of Docker.
* Set the ``SFM_HOSTNAME`` and ``SFM_PORT`` appropriately. These are the public hostname (e.g., sfm.gwu.edu) and port (e.g., 80)
  for SFM.
* Email is configured by providing ``SFM_SMTP_HOST``, ``SFM_EMAIL_USER``, and ``SFM_EMAIL_PASSWORD``.
  (If the configured email account is hosted by Google, you will need to configure the account to "Allow less secure apps."
  Currently this setting is accessed, while logged in to the google account, via https://myaccount.google.com/security#connectedapps).
* Application credentials for social media APIs are configured in by providing the ``TWITTER_CONSUMER_KEY``,
  ``TWITTER_CONSUMER_SECRET``, ``WEIBO_API_KEY``, ``WEIBO_API_SECRET``, and/or ``TUMBLR_CONSUMER_KEY``,
  ``TUMBLR_CONSUMER_SECRET``. These are optional, but will make acquiring credentials easier for users.
  For more information and alternative approaches see :doc:`credentials`.
* Set an admin email address with ``SFM_SITE_ADMIN_EMAIL``. Problems with SFM are sent to this address.
* Set an SFM contact email address with ``SFM_CONTACT_EMAIL``. Users are provided with this address.
* For branding in the SFM UI, provide ``SFM_INSTITUTION_NAME`` and ``SFM_INSTITUTION_LINK``.
* Provide a contact URL (e.g., http://library.gwu.edu) to be used when web harvesting with ``HERITRIX_CONTACT_URL``.

Note that if you make a change to configuration *after* SFM is brought up, you will need to restart containers. If
the change only applies to a single container, then you can stop the container with ``docker kill <container name>``. If
the change applies to multiple containers (or you're not sure), you can stop all containers with ``docker-compose stop``.
Containers can then be brought back up with ``docker-compose up -d`` and the configuration change will take effect.

----------
 Stopping
----------

To stop the containers gracefully::

    docker-compose stop -t 180 twitterstreamharvester
    docker-compose stop

SFM can then be restarted with ``docker-compose up -d``.

-----------------
 Server restarts
-----------------
If Docker is configured to automatically start when the server starts, then SFM will start. (This is enabled by default
when Docker is installed.)

SFM will even be started if it was stopped prior to the server reboot. If you do not want SFM to start, then configure
Docker to not automatically start.

To configure whether Docker is automatically starts, see :ref:`docker-stopping`.

-----------
 Upgrading
-----------

Following are general instructions for upgrading SFM versions. Always consult the release notes of the new version to
see if any additional steps are required.

1. Stop the containers gracefully::

    docker-compose stop -t 180 twitterstreamharvester
    docker-compose stop

This may take several minutes.

2. Make a copy of your existing ``docker-compose.yml`` and ``.env`` files::

    cp docker-compose.yml old.docker-compose.yml
    cp .env old.env

3. Get the latest ``example.prod.docker-compose.yml``. If you previously cloned the sfm-docker repository then::

    git pull
    # Replace 1.7.0 with the correct version.
    git checkout 1.7.0
    cp example.prod.docker-compose.yml docker-compose.yml

otherwise, replacing 1.7.0 with the correct version::

    curl -L https://raw.githubusercontent.com/gwu-libraries/sfm-docker/1.7.0/example.prod.docker-compose.yml > docker-compose.yml

4. If you customized your previous ``docker-compose.yml`` file (e.g., for SFM ELK containers), make the same changes
in your new ``docker-compose.yml``.

5. Make any changes in your ``.env`` file prescribed by the release notes.

6. Bring up the containers::

    docker-compose up -d

It may take several minutes for the images to be downloaded and the containers to start.

7. Deleting images from the previous version is recommended to prevent Docker from filling up too much space. Replacing 1.5.0 with the correct previous version::

    docker rmi $(docker images | grep "1.5.0" | awk '{print $3}')

You may also want to periodically clean up Docker (>= 1.13) with ``docker system prune``.

.. _server-sizing:

---------------
 Server sizing
---------------

While we have not performed any system engineering analysis of optimal server sizing for SFM, the following are
different configurations that we use:

========================  ================  ==========  ========
Use                       Server type       Processors  RAM (gb)
========================  ================  ==========  ========
Production                                  6           16
Sandbox                   m4.large (AWS)    2           8
Use in a class            m4.xlarge (AWS)   4           16
Continuous integration    t2.medium (AWS)   2           4
Heavy dataset processing  m4.4xlarge (AWS)  16          64
Development               Docker for Mac    2           3
========================  ================  ==========  ========
