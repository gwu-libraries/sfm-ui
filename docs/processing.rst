==================================
 Command-line exporting/processing
==================================


While social media data can be exported from the SFM UI, in some cases you may want to export
from the commandline.  These cases include:

* Exporting very large datasets. (Export via the UI is performed serially; export via the commandline
  can be performed in parallel, which may be much faster.)
* Performing more advanced filtering or transformation that is not supported by the UI export.
* Integrating with a processing/analysis pipeline.

To support export and processing from the commandline, SFM provides a processing container.  A processing
container is a Linux shell environment with access to the SFM's data and preloaded with a set of useful tools.

Using a processing container requires familiarity with the Linux shell and shell access to the SFM server.  If
you are interested in using a processing container, please contact your SFM administrator for help.

When exporting/processing data, remember that harvested social media content are stored
in ``/sfm-data``.  ``/sfm-processing`` is provided to store your exports, processed data, or scripts.  Depending
on how it is configured, you may have access to ``/sfm-processing`` from your local filesystem. See :doc:`storage`.

----------------------
 Processing container
----------------------

To bootstrap export/processing, a processing image is provided. A container instantiated from this
image is Ubuntu 14.04 and pre-installed with the warc iterator tools, ``find_warcs.py``, and some other
useful tools. (Warc iterators and ``find_warcs.py`` are described below.)  It will also have read-only
access to the data from ``/sfm-data`` and read/write access to ``/sfm-processing``.

The other tools available in a processing container are:

* `jq <https://stedolan.github.io/jq/>`_ for JSON processing.
* `twarc <https://github.com/edsu/twarc>`_ for access to the `Twarc utils <https://github.com/edsu/twarc/tree/master/utils>`_.
* `JWAT Tools <https://sbforge.org/display/JWAT/JWAT-Tools>`_ for processing WARCs.
* `warctools <https://github.com/internetarchive/warctools>`_ for processing WARCs.
* `parallel <https://www.gnu.org/software/parallel/>`_ for parallelizing processing.
* `csvkit <https://csvkit.readthedocs.io/>`_ for processing CSVs.
* `gron <https://github.com/TomNomNom/gron>`_ for grepping JSON.

To instantiate a processing container, from the directory that contains your ``docker-compose.yml`` file::

    docker-compose run --rm processing /bin/bash


You will then be provided with a bash shell inside the container from which you can execute commands::

    root@0ac9caaf7e72:/sfm-processing# find_warcs.py 4f4d1 | xargs twitter_rest_warc_iter.py | python /opt/twarc/utils/wordcloud.py


Note that once you exit the processing container, the container will be automatically removed.  However, if you have
saved all of your scripts and output files to ``/sfm-processing``, they will be available when you create a new
processing container.


-----------------------
 SFM commandline tools
-----------------------

Warc iterators
==============
SFM stores harvested social media data in WARC files.  A warc iterator tool provides an iterator
to the social media data contained in WARC files. When
used from the commandline, it writes out the social media items one at a time to standard out.
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
* ``tumblr_warc_iter.py``: Tumblr posts

Warc iterator tools can also be used as a library.

Find Warcs
==========
``find_warcs.py`` helps put together a list of WARC files to be processed by other tools, e.g.,
warc iterator tools. (It gets the list of WARC files by querying the SFM API.)

Here is arguments it accepts::

    root@0ac9caaf7e72:/sfm-data# find_warcs.py
    usage: find_warcs.py [-h] [--harvest-start HARVEST_START]
                         [--harvest-end HARVEST_END] [--warc-start WARC_START]
                         [--warc-end WARC_END] [--api-base-url API_BASE_URL]
                         [--debug [DEBUG]] [--newline]
                         collection [collection ...]

For example, to get a list of the WARC files in a particular collection, provide some part of
the collection id::

    root@0ac9caaf7e72:/sfm-data# find_warcs.py 4f4d1
    /sfm-data/collection_set/b06d164c632d405294d3c17584f03278/4f4d1a6677f34d539bbd8486e22de33b/2016/05/04/14/515dab00c05740f487e095773cce8ab1-20160504143638715-00000-47-88e5bc8a36a5-8000.warc.gz

(In this case there is only one WARC file. If there was more than one, it would be space separated. Use ``--newline`` to
to separate with a newline instead.)

The collection id can be found from the SFM UI.

Note that if you are running ``find_warcs.py`` from outside a Docker environment, you will need
to supply ``--api-base-url``.

Sync scripts
============
Sync scripts will extract Twitter data from WARC files for a collection and write tweets to
to line-oriented JSON files and tweet ids to text files. It is called a "sync script" because it will
skip WARCs that have already been processed.

Sync scripts are parallelized, allowing for faster processing.

There are sync scripts for Twitter REST collections (`twitter_rest_sync.sh`) and Twitter stream
collections (`twitter_stream_sync.sh`). Usage is `./<script> <collection id> <destination directory> <# of threads>`.
For example::

    cd /opt/processing
    mkdir /sfm-processing/test
    ./twitter_rest_sync.sh e76b140351574015a6aac8999b06dcc7 /sfm-processing/test 2

READMEs
=======
The `exportreadme` management command will output a README file that can be used as part of the
documentation for a dataset.  The README contains information on the collection, including the
complete change log. Here is an example of creating a README::

    docker-compose exec ui /bin/bash -c "/opt/sfm-ui/sfm/manage.py exportreadme 4f4d1 > /sfm-processing/README.txt"

For examples, see the README files in `this open dataset <https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi%3A10.7910%2FDVN%2FPDI7IN>`_.

Note that this is a management command; thus, it is executed differently than the commandline tools
described above.

---------
 Recipes
---------

Extracting URLs
===============
The `"Extracting URLs from #PulseNightclub for seeding web archiving" blog post <http://gwu-libraries.github.io/sfm-ui/posts/2016-07-11-pulse-processing>`_
provides some useful guidance on extracting URLs from tweets, including unshortening and sorting/counting.

Exporting to line-oriented JSON files
=====================================
This recipe is for exporting social media data from WARC files to line-oriented JSON files. There will be one JSON file
for each WARC. This may be useful for some processing or for loading into some analytic tools.

This recipe uses `parallel <https://www.gnu.org/software/parallel/>`_ for parallelizing the export.

Create a list of WARC files::

    find_warcs.py --newline 7c37157 > source.lst

Replace `7c37157` with the first few characters of the collection id that you want to export. The collection id is
available on the colllection detail page in SFM UI.

Create a list of JSON destination files::

    cat source.lst | xargs basename -a | sed 's/.warc.gz/.json/' > dest.lst

This command puts all of the JSON files in the same directory, using the filename of the WARC file with a .json file extension.

If you want to maintain the directory structure, but use a different root directory::

    cat source.lst | sed 's/sfm-data\/collection_set/sfm-processing\/export/' | sed 's/.warc.gz/.json/'

Replace `sfm-processing\/export` with the root directory that you want to use.

Perform the export::

    parallel -a source.lst -a dest.lst --xapply "twitter_stream_warc_iter.py {1} > {2}"

Replace `twitter_stream_warc_iter.py` with the name of the warc iterator for the type of social media data that you
are exporting.

You can also perform a filter on export using jq. For example, this only exports tweets in Spanish::

    parallel -a source.lst -a dest.lst --xapply "twitter_stream_warc_iter.py {1} | jq -c 'select(.lang == \"es\")' > {2}"

And to save space, the JSON files can be gzip compressed::

    parallel -a source.lst -a dest.lst --xapply "twitter_stream_warc_iter.py {1} | gzip > {2}"

You might also want to change the file extension of the destination file to ".json.gz" by adjusting the commmand use
to create the list of JSON destination files.  To access the tweets in a gzipped JSON file, use::

    gzip -c <filepath>

Counting posts
===============
`wc -l` can be used to count posts. To count the number of tweets in a collection::

    find_warcs.py 7c37157 | xargs twitter_stream_warc_iter.py | wc -l

To count the posts from line-oriented JSON files created as described above::

    cat dest.lst | xargs wc -l

*wc -l gotcha*: When doing a lot of counting, `wc -l` will output a partial total and then reset
the count. The partial totals must be added together to get the grand total. For example::

        [Some lines skipped ...]
            1490 ./964be41e1714492bbe8ec5793e05ec86-20160725070757217-00000-7932-62ebe35d576c-8002.json
            4514 ./5f78a79c6382476889d1ed4734d6105a-20160722202703869-00000-5110-62ebe35d576c-8002.json
           52043 ./417cf950a00d44408458c93f08f0690e-20160910032351524-00000-1775-c4aea5d70c14-8000.json
        54392684 total
        [Some lines skipped ...]
           34778 ./30bc1c34880d404aa3254f82dd387514-20160806132811173-00000-21585-62ebe35d576c-8000.json
           30588 ./964be41e1714492bbe8ec5793e05ec86-20160727030754726-00000-10044-62ebe35d576c-8002.json
        21573971 total

Using jq to process JSON
========================
For tips on using jq with JSON from Twitter and other sources, see:

* `Getting Started Working with Twitter Data Using jq <http://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20160407-twitter-analysis-with-jq/Working-with-twitter-using-jq.ipynb>`_
* `Recipes for processing Twitter data with jq <http://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20161122-twitter-jq-recipes/twitter_jq_recipes.ipynb>`_
* `Reshaping JSON with jq <http://programminghistorian.org/lessons/json-and-jq.html>`_
