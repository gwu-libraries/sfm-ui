================
Collection types
================

Each collection type connects to one of a social media platform's APIs, or
methods for retrieving data. Understanding what each collection type provides is
important to ensure you collect what you need and are aware of any limitations.
Reading the social media platform's documentation provides further important
details.

Collection types
  * `Twitter user timeline`_: Collect tweets from specific Twitter handles
  * `Twitter search`_: Collects tweets by user-chosen criteria from a sample of
    recent tweets
  * `Twitter sample`_: Collects a Twitter provided stream of all tweets in real
    time.
  * `Twitter filter`_: Collects tweets by user-chosen criteria from a stream of
    tweets in real time.
  * `Flickr user`_: Collects posts and photos from specific Flickr handles
  * `Weibo timeline`_: Collects posts from the user and the user's friends
  * `Tumblr blog posts`_: Collects blog posts from specific Tumblr Handles
  * `Collecting Web resources`_: Secondary collections of resources linked to in
    social media posts.


.. _Twitter user timeline:

---------------------
Twitter user timeline
---------------------

Collects tweets and their metadata by particular Twitter user accounts using
`Twitter's user_timeline API
<https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_.
Twitter provides up to 3,200 of the most recent tweets from each user.

Each Twitter user timeline collection can have multiple seeds, where each seed
is a user timeline.

To identify a user timeline, you can provide a screen name
(the string after @, like NASA for @NASA, which the user can change)
or Twitter user ID (a numeric string which never changes, like 11348282 for
@NASA). If you provide one identifier, the other will be looked up and displayed
in SFM UI the first time the harvester runs.

The number of user timeline seeds is not limited in collections, but harvests
may longer if the collection exceeds Twitter's rate limits.

Incorrect or private user timeline seeds are handled by SFM by notifying you
when these are found; all other valid seeds will be collected.

The incremental option will collect tweets that haven't been harvested before,
preventing duplicate tweets. When the incremental option is not selected, the
3,200 most recent tweets will be collected; there will (most likely) be
duplicates, but you will may be able to track changes in time about a user's
timeline, such as retweet and like counts, deletion of tweets, and follower
counts.

Scheduling harvests should depend on how prolific the Twitter users are.
In general, the more frequent the tweeter, the more frequent you’ll want to
schedule harvests.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect media or web resources.


.. _Twitter search:

---------------
Twitter search
---------------

Collects tweets from the previous week that match search queries using
the `Twitter Search API <https://dev.twitter.com/rest/public/search>`_, similar
to a regular search made on `Twitter <https://twitter.com/search-home>`_.
Based on relevance, this is **not** a complete search of all tweets, limited
both by time and arbitrary relevance (determined by Twitter).

Search collections are made up of only one search query.

Search queries mostly follow standard search term formulation; permitted queries
are listed in the documentation for the `Twitter Search API
<https://dev.twitter.com/rest/public/search>`_, or you can construct a query
using the `Twitter Advanced Search query builder
<https://twitter.com/search-advanced>`_.

Broad Twitter searches may take longer to complete---possibly days---due
to Twitter’s rate limits and the amount of data available from the Search
API. In choosing a schedule, make sure that there is enough time between
searches, so that the previous search is not cut off. In some cases, you may only
want to run the search once and then turn off the collection.

The incremental option will collect tweets that haven't been harvested before,
preventing duplicate tweets. When the incremental option is not selected, the
search will be performed again, and there will (most likely) be duplicates; you
may be able to track changes in time about a user's timeline, such as retweet
and like counts, deletion of tweets, and follower counts.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect media or web resources.


.. _Twitter sample:

--------------
Twitter sample
--------------

Collects a random sample of all public tweets using the `Twitter sample stream
<https://dev.twitter.com/streaming/reference/get/statuses/sample>`_, useful for
capturing a sample of what people are talking about on Twitter.
The Twitter sample stream returns approximately 0.5-1% of public tweets,
which is approximately 3GB a day (compressed).

There are no seeds like in other Twitter collections; rather, the sample returns
data every 30 minutes when on.

Only one sample or :ref:`Twitter filter` can be run at a time per credential.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collection media or web resources.


.. _Twitter filter:

---------------
Twitter filter
---------------

Collects a live selection of public tweets from criteria matching keywords,
locations, or users, based on the `Twitter filter streaming API
<https://dev.twitter.com/streaming/reference/post/statuses/filter>`_. Because
tweets are collected live, tweets from the past are not included. (Use a
:ref:`Twitter search` collection to find tweets from the recent past.)

There are three different filter queries supported by SFM: track, follow, and
location.

**Track** collects tweets based on a keyword search A space between words
is treated as 'AND' and a comma is treated as 'OR'. Note that exact phrase
matching is not supported. See the `track parameter documentation
<https://dev.twitter.com/streaming/overview/request-parameters#track>`_ for more
information.

**Follow** collects tweets that are posted by or about a user (not including
mentions) from a comma separated list of user IDs (the part after the @, like
NASA in @NASA). Tweets collected will include those made by the user, retweeting
the user, or replying to the user. See the `follow parameter documentation
<https://dev.twitter.com/streaming/overview/request-parameters#follow>`_ for
more information.

**Location** collects tweets that were geolocated within specific parameters,
based on a bounding box made using the southwest and northeast corner
coordinates. See the `location parameter documentation
<https://dev.twitter.com/streaming/overview/request-parameters#location>`_ for
more information.

Twitter will return a limited number of tweets, so filters that return many
results will not return all available tweets. Therefore, more narrow filters
will usually return more complete results.

Only one filter or :ref:`Twitter sample` can be run at a time per credential.

SFM captures the filter stream in 30 minute chunks and then momentarily stops.
Between rate limiting and this momentary stop, you should never assume that
you are getting every tweet.

There is only one seed in a filter collection, and is either turned on or off.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collection media or web resources.


.. _Flickr user:

-----------
Flickr user
-----------

Collects metadata about public photos by a specific Flickr user, and,
optionally, copies of the photos at specified sizes.

Each Flickr user collection can have multiple seeds, where each seed is a Flickr
user. To identify a user, you can provide a either a username or an NSID. If you
provide one, the other will be looked up and displayed in the SFM UI during the
first harvest. The NSID is a unique identifier and does not change; usernames
may be changed but are unique.

For each user, the user's information will be collected using Flickr's
`people.getInfo <https://www.flickr.com/services/api/flickr.people.getInfo.html>`_
API and the list of her public photos will be retrieved from `people.getPublicPhotos
<https://www.flickr.com/services/api/flickr.people.getPublicPhotos.html>`_.
Information on each photo will be collected with
`photos.getInfo <https://www.flickr.com/services/api/flickr.photos.getInfo.html>`_.

Depending on the image sizes you select, the actual photo files will be
collected as well. Be very careful in selecting the original file size, as this
may require a significant amount of storage. Also note that some Flickr users
may have a large number of public photos, which may require a significant amount
of storage. It is advisable to check the Flickr website to determine the number
of photos in each Flickr user's public photo stream before harvesting.

If the incremental option is selected, only new photos will be collected.

.. _Weibo timeline:

--------------
Weibo timeline
--------------

Collects Weibos by the user and friends of the user whose credentials are
provided using the `Weibo friends_timeline API
<http://open.weibo.com/wiki/2/statuses/friends_timeline>`_.

Note that because collection is determined by the user whose credentials are
provided, there are no seeds for a Weibo timeline collection. To change what is
being collected, change the user's friends from the Weibo website or app.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect image or web resources.

.. _Tumblr blog posts:

-----------------
Tumblr blog posts
-----------------
Collects blog posts by a specified Tumblr blog using the `Tumblr Posts API
<https://www.tumblr.com/docs/en/api/v2#posts>`_.

Each Tumblr blog post collection can have multiple seeds, where each seed is a
blog. The blog can be specified with or without the .tumblr.com extension.

If the incremental option is selected, only new blog posts will be collected.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect image or web resources.

.. _Collecting web resources:

------------------------
Collecting Web resources
------------------------
Most collection types allow you to select an option to collect web resources
such as images, web pages, etc. that are included in the social media post. When 
a social media post includes a URL, SFM will harvest the web page at that URL.
It will harvest only that web page, not any pages linked from that page.

Be very deliberate in collecting web resources.  Performing a web harvest both
takes longer and requires significantly more storage than collecting the
original social media post.
