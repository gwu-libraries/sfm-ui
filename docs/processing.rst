============
 Processing
============


Your social media data can be used in a processing/analysis pipeline. SFM provides several
tools and approaches to support this.

-------
 Tools
-------

Warc iterators
==============
A warc iterator tool provides an iterator to the social media data contained in WARC files. When
used from the commandline, it writes out the social items one at a time to standard out.
(Think of this as ``cat``-ing a line-oriented JSON file. It is also equivalent to the output of
Twarc.)

Each social media type has a separate warc iterator tool. For example, ``twitter_rest_warc_iter.py``
extracts tweets recorded from the Twitter REST API. For example::

    root@0ac9caaf7e72:/sfm-data# twitter_rest_warc_iter.py
    usage: twitter_rest_warc_iter.py [-h] [--pretty] [--dedupe]
                                     [--print-item-type]
                                     filepaths [filepaths ...]

Here is a list of the warc iterators:

* ``twitter_rest_warc_iter.py``: Tweets recorded from Twitter REST API.
* ``twitter_stream_warc_iter.py``: Tweets recorded from Twitter Streaming API.
* ``flickr_photo_warc_iter.py``: Flickr photos
* ``weibo_warc_iter.py``: Weibos

Warc iterator tools can also be used as a library.

Find Warcs
==========
``find_warcs.py`` helps put together a list of WARC files to be processed by other tools, e.g.,
warc iterator tools. (It gets the list of WARC files by querying the SFM API.)

Here is arguments it accepts::

    root@0ac9caaf7e72:/sfm-data# find_warcs.py
    usage: find_warcs.py [-h] [--include-web] [--harvest-start HARVEST_START]
                         [--harvest-end HARVEST_END] [--api-base-url API_BASE_URL]
                         [--debug [DEBUG]]
                         collection [collection ...]

For example, to get a list of the WARC files in a particular collection, provide some part of
the collection id::

    root@0ac9caaf7e72:/sfm-data# find_warcs.py 4f4d1
    /sfm-data/collections/b06d164c632d405294d3c17584f03278/4f4d1a6677f34d539bbd8486e22de33b/2016/05/04/14/515dab00c05740f487e095773cce8ab1-20160504143638715-00000-47-88e5bc8a36a5-8000.warc.gz

(In this case there is only one WARC file. If there was more than one, it would be space separated.)

The collection id can be found from the SFM UI.

Note that if you are running ``find_warcs.py`` from outside a Docker environment, you will need
to supply ``--api-base-url``.


------------
 Approaches
------------

Processing in container
=======================
To bootstrap processing, a processing image is provided. A container instantiated from this
image is Ubuntu 14.04 and pre-installed with the warc iterator tools, ``find_warcs.py``, and some other
use tools. It will also have read-only access to the data from ``/sfm-data``.

The other tools are:

* `jq <https://stedolan.github.io/jq/>`_ for JSON processing.
* `twarc <https://github.com/edsu/twarc>`_ for access to the `Twarc utils <https://github.com/edsu/twarc/tree/master/utils>`_.
* `JWAT Tools <https://sbforge.org/display/JWAT/JWAT-Tools>`_ for processing WARCs.
* `warctools <https://github.com/internetarchive/warctools>`_ for processing WARCs.

To instantiate::

    docker run -it --rm --link=[container name of SFM UI]:api --volumes-from=[container name of data container]:ro --volume=[path on your local filesystem for working files]:/sfm-processing gwul/sfm-processing:[version]


For example::

    docker run -it --rm --link=docker_sfmuiapp_1:api --volumes-from=docker_sfmdata_1:ro --volume=/home/ubuntu/sfm-processing:/sfm-processing gwul/sfm-processing:1.0.0


You will then be provided with a bash shell inside the container from which you can execute commands::

    root@0ac9caaf7e72:/sfm-processing# find_warcs.py 4f4d1 | xargs twitter_rest_warc_iter.py | python /opt/twarc/utils/wordcloud.py

``/sfm-processing`` will be linked in from your local filesystem.  You can place scripts in this directory to make them
available inside the processing container or write output files to this directory to make them available outside the
processing container.

Note that once you exit the processing container, the container will be automatically removed.  However, if you have
saved all of your scripts and output files to ``/sfm-processing``, they will be available when you create a new
processing container.


Processing locally
==================
In a typical Docker configuration, the data directory will be linked into the Docker environment.
This means that the data is available both inside and outside the Docker environment. Given this,
processing can be performed locally (i.e., outside of Docker).

The various tools can be installed locally::

    GLSS-F0G5RP:tmp justinlittman$ virtualenv ENV
    GLSS-F0G5RP:tmp justinlittman$ source ENV/bin/activate
    (ENV)GLSS-F0G5RP:tmp justinlittman$ pip install git+https://github.com/gwu-libraries/sfm-utils.git
    (ENV)GLSS-F0G5RP:tmp justinlittman$ pip install git+https://github.com/gwu-libraries/sfm-twitter-harvester.git
    (ENV)GLSS-F0G5RP:tmp justinlittman$ twitter_rest_warc_iter.py
    usage: twitter_rest_warc_iter.py [-h] [--pretty] [--dedupe]
                                     [--print-item-type]
                                     filepaths [filepaths ...]
    twitter_rest_warc_iter.py: error: too few arguments