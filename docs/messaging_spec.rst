=========================
 Messaging Specification
=========================

--------------
 Introduction
--------------

SFM is architected as a number of components that exchange messages via a messaging
queue. To implement functionality, these components send and receive messages and perform
certain actions. The purpose of this document is to describe this interaction between the
components (called a "flow") and to specify the messages that they will exchange.

Note that as additional functionality is added to SFM, additional flows and messages
will be added to this document.

---------
 General
---------

* Messages may include extra information beyond what is specified below.
  Message consumers should ignore any extra information.
* RabbitMQ will be used for the messaging queue. See the Messaging docs for additional
  information. It is assumed in the flows below that components receive messages by
  connecting to appropriately defined queues and publish messages by submitting them
  to the appropriate exchange.

---------------------------------
 Harvesting social media content
---------------------------------

Harvesting is the process of retrieving social media content from the APIs
of social media services and writing to WARC files.

Background information
======================
* A requester is an application that requests that a harvest be performed. A
  requester may also want to monitor the status of a harvest. In the current
  architecture, the SFM UI serves the role of requester.
* A stream harvest is a harvest that is intended to continue indefinitely until
  terminated. A harvest of a Twitter sample stream
  is an example of a stream harvest. A stream harvest is different from a non-stream
  harvest in that a requester must both start and optionally stop a stream harvest.
  Following the naming conventions from Twitter, a harvest of a REST, non-streaming API
  will be referred to as a REST harvest.
* Depending on the implementation, a harvester may produce a single warc or multiple warcs. It
  is likely that in general stream harvests will result in multiple warcs, but REST harvest will
  result in a single warc.

Flow
====

The following is the flow for a harvester performing a REST harvest and
creating a single warc:

1. Requester publishes a harvest start message.
2. Upon receiving the harvest message, a harvester:

   1. Makes the appropriate api calls.
   2. Writes the api calls to a warc.
3. Upon completing the api harvest, the harvester:

   1. Publishes a warc created message.
   2. Publishes a harvest status message with the status of `completed success` or `completed failure`.


The following is the message flow for a harvester performing a stream harvest and
creating multiple warcs:

1. Requester publishes a harvest start message.
2. Upon receiving the harvest message, a harvester:

   1. Opens the api stream.
   2. Writes the stream results to a warc.
3. When rotating to a new warc, the harvester publishes a warc created message.
4. At intervals during the harvest, the harvester:

   1. Publishes a harvest status message with the status of `running`.
5. When ready to stop, the requester publishes a harvest stop message.
6. Upon receiving the harvest stop message, the harvester:

   1. Closes the api stream.
   2. Publishes a final warc created message.
   3. Publishes a final harvest status message with the status of `completed success` or `completed failure`.

* Any harvester may send harvest status messages with the status of `running` before the final
  harvest status message. A harvester performing a stream harvest must send harvest status messages
  at regular intervals.
* A requester should not send harvest stop messages for a REST harvest. A harvester
  performing a REST harvest may ignore harvest stop messages.

Messages
========

Harvest start message
---------------------

Harvest start messages specify for a harvester the details of a harvest. Example::

    {
        "id": "sfmui:45",
        "type": "flickr_user",
        "path": "/sfm-data/collections/3989a5f99e41487aaef698680537c3f5/6980fac666c54322a2ebdbcb2a9510f5",
        "seeds": [
            {
                "id": "a36fe186fbfa47a89dbb0551e1f0f181",
                "token": "justin.littman",
                "uid": "131866249@N02"
            },
            {
                "id": "ab0a4d9369324901a890ec85f00194ac",
                "token": "library_of_congress"
            }
        ],
        "options": {
            "sizes": ["Thumbnail", "Large", "Original"]
        },
        "credentials": {
            "key": "abddfe6fb8bba36e8ef0278ec65dbbc8",
            "secret": "1642649c54cc3ebe"
        },
        "collection_set": {
            "id": "3989a5f99e41487aaef698680537c3f5"
        },
        "collection": {
            "id": "6980fac666c54322a2ebdbcb2a9510f5"
        }
    }

Another example::

    {
        "id": "test:1",
        "type": "twitter_search",
        "path": "/sfm-data/collections/3989a5f99e41487aaef698680537c3f5/6980fac666c54322a2ebdbcb2a9510f5",
        "seeds": [
            {
                "id": "32786222ef374eb38f1c5d56321c99e8",
                "token": "gwu"
            },
            {
                "id": "0e789cddd0fb41b5950f569676702182",
                "token": "gelman"
            }
        ],
        "credentials": {
            "consumer_key": "EHde7ksBGgflbP5nUalEfhaeo",
            "consumer_secret": "ZtUpemtBkf2maqFiy52D5dihFPAiLebuMOmqN0jeQtXeAlen",
            "access_token": "481186914-c2yZjgbk13np0Z5MWEFQKSQNFBXd8T9r4k90YkJl",
            "access_token_secret": "jK9QOmn5Vbbmfg2ANT6KgfmKRqV8ThXVQ1G6qQg8BCejvp"
        },
        "collection_set": {
            "id": "3989a5f99e41487aaef698680537c3f5"
        },
        "collection": {
            "id": "6980fac666c54322a2ebdbcb2a9510f5"
        }
    }

* The routing key will be `harvest.start.<social media platform>.<type>`. For example,
  `harvest.start.flickr.flickr_photo`.
* `id`: A globally unique identifier for the harvest, assigned by the requester.
* `type`: Identifies the type of harvest, including the social media platform. The
  harvester can use this to map to the appropriate api calls.
* `seeds`: A list of seeds to harvest. Each seed is represented by a map containing `id`, `token` and (optionally) `uid`. Note
  that some harvest types may not have seeds.
* `options`: A name/value map containing additional options for the harvest.  The contents of the map
  are specific to the type of harvest. (That is, the seeds for a flickr photo are going to be
  different than the seeds for a twitter user timeline.)
* `credentials`: All credentials that are necessary to access the social media platform.
  Credentials is a name/value map; the contents are specific to a social media platform.
* `path`: The base path for the collection.

Harvest stop message
--------------------

Harvest stop messages tell a harvester perform a stream harvest to stop. Example::

    {
        "id": "sfmui:45"
    }

* The routing key will be `harvest.stop.<social media platform>.<type>`. For example,
  `harvest.stop.twitter.filter`.

Harvest status message
----------------------

Harvest status messages allow a harvester to provide information on the harvests
it performs. Example::

    {
        "id": "sfmui:45"
        "status": "completed success",
        "date_started": "2015-07-28T11:17:36.640044",
        "date_ended": "2015-07-28T11:17:42.539470",
        "infos": []
        "warnings": [],
        "errors": [],
        "stats": {
            "2016-05-20": {
                "photos": 12,
            },
            "2016-05-21": {
                "photos": 19,
            },
        },
        "token_updates": {
            "a36fe186fbfa47a89dbb0551e1f0f181": "j.littman"
        },
        "uids": {
            "ab0a4d9369324901a890ec85f00194ac": "671366249@N03"
        },
        "warcs": {
            "count": 3
            "bytes": 345234242
        },
        "service": "Twitter Harvester",
        "host": "f0c3c5ef7031",
        "instance": "39",
    }

* The routing key will be `harvest.status.<social media platform>.<type>`. For example,
  `harvest.status.flickr.flickr_photo`.
* `status`: Valid values are `completed success`, `completed failure`, or `running`.
* `infos`, `warnings`, and `errors`:  Lists of messages.  A message should be an object
  (i.e., dictionary) containing a `code` and `message` entry. It may optionally contain
  a `seed_id` entry giving the seed id to which the messages applies. Codes should be consistent
  to allow message consumers to identify types of messages.
* `stats`:  A count of items that are harvested by date.  Items should be a human-understandable
  labels (plural and lower-cased).  Stats is optional for in progress statuses, but required for final statuses.
* `token_updates`: A map of uids to tokens for which a token change was detected while harvesting.
  For example, for Twitter a token update would be provided whenever a user's screen name
  changes.
* `uids`: A map of tokens to uids for which a uid was identified while harvesting at not
  provided in the harvest start message.  For example, for Flickr a uid would be provided
  containing the NSID for a username.
* `warcs`.`count`: The total number of WARCs created during this harvest.
* `warcs`.`bytes`: The total number of bytes of the WARCs created during this harvest.
* `service`, `host`, and `instance` identify what performed the harvest. `service` is the name
  of the harvester. `host` is the Docker container id. `instance` is the harvest process identifier
  (PID) within the container.  This is useful in cases where there are multiple instances of a service
  on a host.  

Warc created message
--------------------

Warc created message allow a harvester to provide information on the warcs that are
created during a harvest. Example::

    {
        "warc": {
            "path": "/sfm-data/collections/3989a5f99e41487aaef698680537c3f5/6980fac666c54322a2ebdbcb2a9510f5/2015/07/28/11/harvest_id-2015-07-28T11:17:36Z.warc.gz",,
            "sha1": "7512e1c227c29332172118f0b79b2ca75cbe8979",
            "bytes": 26146,
            "id": "aba6033aafce4fbabd846026ca47f13e",
            "date_created": "2015-07-28T11:17:36.640178"
        },
        "collection_set": {
            "id": "3989a5f99e41487aaef698680537c3f5"
        },
        "collection": {
            "id": "6980fac666c54322a2ebdbcb2a9510f5"
        },
        "harvest": {
            "id": "98ddaa6e8c1f4b44aaca95bc46d3d6ac",
            "type": "flickr_user"
        }
    }

* The routing key will be `warc_created`.
* Each warc created message will be for a single warc.

---------------------------------
 Exporting social media content
---------------------------------

Exporting is the process of extracting social media content from WARCs and writing
to export files. The exported content may be a subset or derivate of the original
content. A number of different export formats will be supported.

Background information
======================
* A requester is an application that requests that an export be performed. A
  requester may also want to monitor the status of an export. In the current
  architecture, the SFM UI serves the role of requester.
* Depending on the nature of the export, a single or multiple files may be produced.

Flow
====

The following is the flow for an export:

1. Requester publishes an export start message.
2. Upon receiving the export start message, an exporter:

   1. Makes calls to the SFM REST API to determine the WARC files from which to export.
   2. Limits the content is specified by the export start message.
   3. Writes to export files.
3. Upon completing the export, the exporter publishes an export status message
   with the status of `completed success` or `completed failure`.

Export start message
--------------------

Export start messages specify the requests for an export. Example::

    {
        "id": "f3ddcbfc5d6b43139d04d680d278852e",
        "type": "flickr_user",
        "collection": {
            "id": "005b131f5f854402afa2b08a4b7ba960"
        },
        "path": "/sfm-data/exports/45",
        "format": "csv",
        "dedupe": true,
        "segment_size": 100000,
        "item_date_start": "2015-07-28T11:17:36.640178",
        "item_date_end": "2016-07-28T11:17:36.640178",
        "harvest_date_start": "2015-07-28T11:17:36.640178",
        "harvest_date_end": "2016-07-28T11:17:36.640178"
    }

Another example::

    {
        "id": "f3ddcbfc5d6b43139d04d680d278852e",
        "type": "flickr_user",
        "seeds": [
            {
                "id": "48722ac6154241f592fd74da775b7ab7",
                "uid": "23972344@N05"
            },
            {
                "id": "3ce76759a3ee40b894562a35359dfa54",
                "uid": "85779209@N08"
            }
        ],
        "path": "/sfm-data/exports/45",
        "format": "json",
        "segment_size": null
    }

* The routing key will be `export.start.<social media platform>.<type>`. For example,
  `export.start.flickr.flickr_user`.
* `id`: A globally unique identifier for the harvest, assigned by the requester.
* `type`: Identifies the type of export, including the social media platform. The
  export can use this to map to the appropriate export procedure.
* `seeds`: A list of seeds to export. Each seed is represented by a map containing `id` and `uid`.
* `collection`: A map containing the `id` of the collection to export.
* Each export start message must have a `seeds` or `collection` but not both.
* `path`: A directory into which the export files should be placed. The directory may not exist.
* `format`: A code for the format of the export. (Available formats may change.)
* `dedupe`: If true, duplicate social media content should be removed.
* `item_date_start` and `item_date_end`: The date of social media content should be within this range.
* `harvest_date_start` and `harvest_date_end`: The harvest date of social media content should be within this range.
* `segment_size`: Maximum number of items to include in a single file. `null` means that all items should be placed in a
  single file.

Export status message
----------------------

Export status messages allow an exporter to provide information on the exports
it performs. Example::

    {
        "id": "f3ddcbfc5d6b43139d04d680d278852e"
        "status": "completed success",
        "date_started": "2015-07-28T11:17:36.640044",
        "date_ended": "2015-07-28T11:17:42.539470",
        "infos": []
        "warnings": [],
        "errors": [],
        "service": "Twitter Harvester",
        "host": "f0c3c5ef7031",
        "instance": "39",
    }

* The routing key will be `export.status.<social media platform>.<type>`. For example,
  `export.status.flickr.flickr_user`.
* `status`: Valid values are `running`, `completed success` or `completed failure`.
* `infos`, `warnings`, and `errors`:  Lists of messages.  A message should be an object
  (i.e., dictionary) containing a `code` and `message` entry.  Codes should be consistent
  to allow message consumers to identify types of messages.
* `service`, `host`, and `instance` identify what performed the harvest. `service` is the name
  of the harvester. `host` is an identifier for the location of the harvest, e.g., the Docker
  container id. `instance` is an identifier for the process of the service on the host, e.g.,
  the PID. The is helps in cases there may be multiple instances of a service on a host.
