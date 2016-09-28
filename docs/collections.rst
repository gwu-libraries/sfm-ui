=================
Collection types
=================

Each collection type connects to one of a social media platform's APIs,
or methods for retrieving data.
Understanding what each collection type provides is important to ensure you
collect what you need and are aware of any limitations. Reading the social media
platform's documentation provides further important details.

.. _Twitter search:

---------------
Twitter search
---------------

Queries the `Twitter Search API <https://dev.twitter.com/rest/public/search>`_
to retrieve public tweets from a sampling of tweets from the most recent 7 days.
This is not a comprehensive search of all tweets. To formulate a search query,
use the `Twitter Advanced Search query builder <https://twitter.com/search-advanced>`_.

.. _Twitter filter:

---------------
Twitter filter
---------------

Collects public tweets from the `Twitter filter streaming API <https://dev.twitter.com/streaming/reference/post/statuses/filter>`_,
matching keywords, locations, or users. The tweets are from the current time going
forward. Tweets from the past are not available with this collection type.
(Create a Twitter search collection with the same terms to collect tweets from the recent past).
There are limits on how many tweets Twitter will supply, so filters on high-volume
hashtags will not return all tweets available. Twitter only allows you to run one
filter collection type at a time with an SFM credential.

.. _Twitter user timeline:

---------------------
Twitter user timeline
---------------------

Collects tweets by a particular Twitter user account. If the screen name is provided, 
SFM will look up that account's Twitter user ID (UID), which does
not change.  Twitter provides up to the most recent 3,200 tweets by that account. 
If "incremental" is selected as an option for the collection, future harvests will 
only collect tweets since the last harvested tweet. SFM queries `Twitter's user_timeline
API <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_ to retrieve
tweets. 

.. _Twitter sample:

--------------
Twitter sample
--------------

Collects tweets from the `Twitter sample stream <https://dev.twitter.com/streaming/reference/get/statuses/sample>`_,
which contains  approximately 0.5-1% of public tweets. This stream produces a lot of data,
currently a 3GB a day (compressed).

.. _Flickr user:

-----------
Flickr user
-----------

Collects metadata about public photos by a specific Flickr user. Will collect the photos themselves if 
the "Web resources" checkbox is selected.

.. _Weibo timeline:

--------------
Weibo timeline
--------------

Collects Weibos by the user and friends of the user whose credentials are provided. 
Uses the `Weibo friends_timeline API <http://open.weibo.com/wiki/2/statuses/friends_timeline>`_. 

.. _Tumblr blog posts:

-----------------
Tumblr blog posts
-----------------
Collects blog posts by a specified Tumblr blog.

.. _Collecting web resources:

------------------------
Collecting Web resources
------------------------
Each collection type allows you to select an option to collect web resources. When a social media post
includes a URL, SFM will harvest the web page at that URL. It will harvest only that web page, not any
pages linked from that page. Note that the web pages require more storage than the social media itself,
so select this option only if you are prepared to handle that data. 
