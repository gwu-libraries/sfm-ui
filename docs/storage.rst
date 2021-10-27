=========
 Storage
=========

-----------------
 Storage volumes
-----------------

SFM stores data in multiple directories, which may be set up as separate volumes:

* sfm-db-data: Postgres database for sfm-ui data
* sfm-export-data: exports storage 
* sfm-containers-data: Docker containers data
* sfm-collection-set-data: collection set data, including WARCs
* sfm-mq-data: RabbitMQ data
* sfm-processing: The processing volume is where processed data is stored when using a processing container.
  (See :doc:`processing`.) It is available within containers as /sfm-processing.


--------------
 Volume types
--------------

There are 2 types of volumes:

* Internal to Docker. The files on the volume will only be available from within Docker containers.
* Linked to a host location. The files on the volumes will be available from within Docker containers and from the
  host operating system.

The type of volume is specified in the `.env` file. When selecting a link to a host location, the path on the host
environment must be specified::

    # Docker internal volume
    DATA_VOLUME_COLLECTION_SET=/sfm-collection-set-data
    # Linked to host location
    #DATA_VOLUME_COLLECTION_SET=/src/sfm-data/sfm-collection-set-data:/sfm-collection-set-data
    # Docker internal volume
    PROCESSING_VOLUME=/sfm-processing
    # Linked to host location
    #PROCESSING_VOLUME=/src/sfm-processing:/sfm-processing

We recommend that you use an internal volume only for development; for other uses linking to a host
location is recommended. This make it easier to place the data on specific storage devices (e.g., NFS or EBS) and to
backup the data.

----------------
 File ownership
----------------

SFM files are owned by the sfm user (default uid 990) in the sfm group (default gid 990). If you use a link to a host
location and list the files, the uid and gid may be listed instead of the user and group names.

If you shell into a Docker container, you will be the root user. Make sure that any operations you perform will not
leave behind files that do not have appropriate permissions for the sfm user.

Note then when using Docker for Mac and linking to a host location, the file ownership may not appear as expected.

---------------------------------
 Directory structure of SFM data
---------------------------------

The following is a outline of the structure of sfm data::

    /sfm-collection-set-data/
        collection_set/
            <collection set id>
                README.txt (README for collection set)
                <collection id>/
                    README.txt (README for collection)
                    state.json (Harvest state record)
                    records/
                        JSON records for the collection metadata
                    <year>/<month>/<day>/<hour>/
                        WARC files
    /sfm-containers-data
        containers/
            <container id>/
                Working files for individual containers
    /sfm-export-data
        export/
            <export id>/
                Export files
    /sfm-db-data
        postgresql/
            Postgres db files
    /sfm-mq-data
        rabbitmq
            RabbitMQ files

----------------
 Space warnings
----------------

SFM will monitor free space on data volumes and sfm-processing. Administrators will be notified when the amount of free space
crosses a configurable threshold.  The threshold is set in the `.env` file::

    # sfm-data free space threshold to send notification emails. Values must end with MB,GB,TB. eg. 500MB,10GB,1TB
    # Use DATA_THRESHOLD_SHARED when all data volumes are on the same filesystem and DATA_SHARED_USED is True.
    #DATA_THRESHOLD_SHARED=6GB
    DATA_VOLUME_THRESHOLD_DB=10GB
    DATA_VOLUME_THRESHOLD_MQ=10GB
    DATA_VOLUME_THRESHOLD_EXPORT=10GB
    DATA_VOLUME_THRESHOLD_CONTAINERS=10GB
    DATA_VOLUME_THRESHOLD_COLLECTION_SET=10GB
    # sfm-processing free space threshold to send notification emails,only ends with MB,GB,TB. eg. 500MB,10GB,1TB
    PROCESSING_VOLUME_THRESHOLD=10GB

------------------------------------------------------------
 Moving from a Docker internal volume to a linked volume
------------------------------------------------------------

These instructions are for Ubuntu. They may need to be adjusted for other operating systems.

1. Stop docker containers::

        docker-compose stop
        
2. Copy sfm data directory contents from inside the container to a linked volume. Linked volumes can be on a mounted filesystem or within a directory on the same filesystem::

        sudo docker cp sfm_data_1:/sfm-collection-set-data /sfm-data/sfm-collection-set-data
        sudo docker cp sfm_data_1:/sfm-export-data /sfm-data/sfm-export-data
        sudo docker cp sfm_data_1:/sfm-db-data /sfm-data/-sfm-db-data
        sudo docker cp sfm_data_1:/sfm-mq-data /sfm-data/sfm-mq-data
        sudo docker cp sfm_data_1:/sfm-containers-data /sfm-data/sfm-containers-data
        
3. Set ownership::

        sudo chown -R 990:990 /sfm-data/*
        
        sudo chown -R 999:999 /sfm-data/postgresql/
        sudo chown -R 999:999 /sfm-data/rabbitmq/

4. Change .env::

        DATA_VOLUME_MQ=/sfm-data/sfm-mq-data:/sfm-mq-data
        DATA_VOLUME_DB=/sfm-data/sfm-db-data:/sfm-db-data
        DATA_VOLUME_EXPORT=/sfm-data/sfm-export-data:/sfm-export-data
        DATA_VOLUME_CONTAINERS=/sfm-data/sfm-containers-data:/sfm-containers-data
        DATA_VOLUME_COLLECTION_SET=/sfm-data/sfm-collection-set-data:/sfm-collection-set-data

5. Restart containers::

        docker-compose up -d
