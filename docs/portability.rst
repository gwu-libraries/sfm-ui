=========================================
 Collection set / Collection portability
=========================================

----------
 Overview
----------
Collections and collection sets are portable. That means they can be moved to another SFM instance or
to another environment, such as a repository. This can also be used to backup an SFM instance.

A collection includes all of the social media items (stored in WARCs) and the database
records for the collection sets, collections, users, groups, credentials, seeds, harvests, and WARCs, as well
as the history of collection sets, collections, credentials, and seeds. The
database records are stored in JSON format in the ``records`` subdirectory of the collection. Each collection
has a complete set of JSON database records to support loading it into a different SFM instance.

Here are the JSON database records for an example collection::

    [root@1da93afd43b5:/sfm-data/collection_set/4c59ebf2dcdc4a0e9660e32d004fa846/072ff07ea9954b39a1883e979de92d22/records# ls
    collection.json      groups.json	 historical_collection.json	 historical_seeds.json	users.json
    collection_set.json  harvest_stats.json  historical_collection_set.json  info.json		warcs.json
    credentials.json     harvests.json	 historical_credentials.json	 seeds.json

Thus, moving a collection set only requires moving/copying the collection set's directory; moving a collection
only requires moving/copying a collection's directory.  Collection sets are in ``/sfm-data/collection_set`` and
are named by their collection set ids.  Collections are subdirectories of their collection set
and are named by their collection ids.

A ``README.txt`` is automatically created for each collection and collection set. Here a ``README.txt`` for
an example collection set::

    This is a collection set created with Social Feed Manager.

    Collection set name: test collection set
    Collection set id: 4c59ebf2dcdc4a0e9660e32d004fa846

    This collection set contains the following collections:
    * test twitter sample (collection id 59f9ff647ffd4fa28fd7e5bc4d161743)
    * test twitter user timeline (collection id 072ff07ea9954b39a1883e979de92d22)


    Each of these collections contains a README.txt.

    Updated on Oct. 18, 2016, 3:09 p.m.


-------------------------------------------------
 Preparing to move a collection set / collection
-------------------------------------------------

Nothing needs to be done to prepare a collection set or collection for moving. The collection set and collection
directories contain all of the files required to load it into a different SFM instance.

The JSON database records are refreshed from the database on a nightly basis. Alternatively, they
can be refreshed used the ``serializecollectionset`` and ``serializecollection`` management commands::

    root@1da93afd43b5:/opt/sfm-ui/sfm# ./manage.py serializecollectionset 4c59ebf2d


---------------------------------------
 Loading a collection set / collection
---------------------------------------

1. Move/copy the collection set/collection to ``/sfm-data/collection_set``. Collection sets should be placed
   in this directory. Collections should be placed into a collection set directory.
2. Execute the ``deserializecollectionset`` or ``deserializecollection`` management command::

    root@1da93afd43b5:/opt/sfm-ui/sfm# ./manage.py deserializecollectionset /sfm-data/collection_set/4c59ebf2dcdc4a0e9660e32d004fa846

Note:

* If loading a collection set, all of the collection set's collections will also be loaded.
* When loading, all related items are also loaded.  For example, when a collection is loaded, all of the seeds,
  harvests, credentials, and their histories are also loaded.
* If a database record already exists for a collection set, loading will not continue for the collection set or any
  of its collections or related records (e.g., groups).
* If a database record already exists for a collection, loading will not continue for the collection or any of the
  related records (e.g., users, harvests, WARCs).
* If a database record already exists for a user or group, it will not be loaded.
* Collections that are loaded are turned off.
* Users that are loaded are set to inactive.
* A history note is added to collection sets and collections to document the load.

-------------------------------
 Moving an entire SFM instance
-------------------------------

1. Stop the source instance: ``docker-compose stop``.
2. Copy the ``/sfm-data`` directory from the source server to the destination server.
3. If preserving processing data, also copy the ``/sfm-processing`` directory from the source server to the destination
   server.
4. Copy the ``docker-compose.yml`` and ``.env`` files from the source server to the destination server.
5. Make any changes necessary in the ``.env`` file, e.g., ``SFM_HOSTNAME``.
6. Start the destination instance: ``docker-compose up -d``.

If moving between AWS EC2 instances and ``/sfm-data`` is on a separate EBS volume, the volume can be detached from
the source EC2 instances and attached to the destination EC2 instance.