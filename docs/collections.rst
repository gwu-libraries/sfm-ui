================
Collection types
================

Each collection type connects to one of a social media platform's APIs, or
methods for retrieving data. Understanding what each collection type provides is
important to ensure you collect what you need and are aware of any limitations.
Reading the social media platform's documentation provides further important
details.

Collection types
  * `Twitter user timeline`_: Collect tweets from specific Twitter accounts
  * `Twitter search`_: Collects tweets by a user-provided search query from recent tweets
  * `Twitter sample`_: Collects a Twitter provided stream of a subset of all tweets in real
    time.
  * `Twitter filter`_: Collects tweets by user-provided criteria from a stream of
    tweets in real time.
  * `Flickr user`_: Collects posts and photos from specific Flickr accounts
  * `Weibo timeline`_: Collects posts from the user and the user's friends
  * `Weibo search`_: Collects recent weibo posts by a user-provided search query
  * `Tumblr blog posts`_: Collects blog posts from specific Tumblr blogs

.. _guide-twitter-user-timelines:

.. _Twitter user timeline:

---------------------
Twitter user timeline
---------------------

Twitter user timeline collections collect the 3,200 most recent tweets from each of
a list of Twitter accounts using `Twitter's user_timeline API
<https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html>`_.

**Seeds** for Twitter user timelines are individual Twitter accounts.

To identify a user timeline, you can provide a screen name
(the string after @, like NASA for @NASA)
or Twitter user ID (a numeric string which never changes, like 11348282 for
@NASA). If you provide one identifier, the other will be looked up and displayed
in SFM the first time the harvester runs. The user may change the screen name
over time, and the seed will be updated accordingly. 

The harvest schedule should depend on how prolific the Twitter users are.
In general, the more frequent the tweeter, the more frequent you’ll want to
schedule harvests.

SFM will notify you when incorrect or private user timeline seeds are requested;
all other valid seeds will be collected.

See :ref:`guide-incremental-collecting` to decide whether or not to collect
incrementally.

.. _guide-twitter-search:

.. _Twitter search:

---------------
Twitter search
---------------

Twitter searches collect tweets from the last 7-9 days that match search
queries, similar to a regular search done on Twitter, using
the `Twitter Search API <https://developer.twitter.com/en/docs/tweets/search/overview/standard>`_.
This is **not** a complete search of all tweets; results are limited
both by time and arbitrary relevance (determined by Twitter).

Search queries must follow standard search term formulation; permitted queries
are listed in the documentation for the `Twitter Search API
<https://developer.twitter.com/en/docs/tweets/search/guides/standard-operators>`_,
or you can construct a query
using the `Twitter Advanced Search query builder
<https://twitter.com/search-advanced>`_.

Broad Twitter searches may take longer to complete -- possibly days -- due
to Twitter’s rate limits and the amount of data available from the Search
API. In choosing a schedule, make sure that there is enough time between
searches. (If there is not enough time between searches, later harvests will
be skipped until earlier harvests complete.) In some cases, you may only
want to run the search once and then turn off the collection.

See :ref:`guide-incremental-collecting` to decide whether or not to collect
incrementally.

.. _guide-twitter-sample:

.. _Twitter sample:

--------------
Twitter sample
--------------

Twitter samples are a random collection of approximately 0.5--1% of public
tweets, using the `Twitter sample stream
<https://developer.twitter.com/en/docs/tweets/sample-realtime/overview/GET_statuse_sample>`_, useful for
capturing a sample of what people are talking about on Twitter.
The Twitter sample stream returns approximately 0.5-1% of public tweets,
which is approximately 3GB a day (compressed).

Unlike other Twitter collections, there are no seeds for a Twitter sample.

When on, the sample returns data every 30 minutes.

Only one sample or :ref:`Twitter filter` can be run at a time per credential.

.. _guide-twitter-filter:

.. _Twitter filter:

---------------
Twitter filter
---------------

Twitter Filter collections harvest a live selection of public tweets from
criteria matching keywords, locations, languages, or users, based on the
`Twitter filter streaming API
<https://developer.twitter.com/en/docs/tweets/filter-realtime/overview/statuses-filter>`_. Because
tweets are collected live, tweets from the past are not included. (Use a
:ref:`Twitter search` collection to find tweets from the recent past.)

There are four different filter queries supported by SFM: track, follow, 
location, and language.

**Track** collects tweets based on a keyword search. A space between words
is treated as 'AND' and a comma is treated as 'OR'. Note that exact phrase
matching is not supported. See the `track parameter documentation
<https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters#track>`_ for more
information.

- Note: When entering a comma-separated list of search terms for the track or follow parameters, make sure to use the standard ``,`` character.  When typing in certain languages that use a non-Roman alphabet, a different character is generated for commas.  For example, when typing in languages such as Arabic, Farsi, Urdu, etc., typing a comma generates the ``،`` character.  To avoid errors, the Track parameter should use the Roman ``,`` character; for example:   سواقة المرأه , قرار قيادة سيارة 

**Follow** collects tweets that are posted by or about a user (not including
mentions) from a comma separated list of user IDs (the numeric identifier for
a user account). Tweets collected will include those made by the user, retweeting
the user, or replying to the user. See the `follow parameter documentation
<https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters#follow>`_ for
more information.

- Note: The Twitter website does not provide a way to look up the user ID for a user account. You can use `https://tweeterid.com <https://tweeterid.com/>`_ for this purpose.


**Location** collects tweets that were geolocated within specific parameters,
based on a bounding box made using the southwest and northeast corner
coordinates. See the `location parameter documentation
<https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters#locations>`_ for
more information.

**Language** collects tweets that Twitter detected as being written in the specified languages.
For example, specifying `en,es` will only collect Tweets detected to be in the English or Spanish languages.
See the `language parameter documentation
<https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters#language>`_ for
more information.

Twitter will return a limited number of tweets, so filters that return many
results will not return all available tweets. Therefore, more narrow filters
will usually return more complete results.

Only one filter or :ref:`Twitter sample` can be run at a time per credential.

SFM captures the filter stream in 30 minute chunks and then momentarily stops.
Between rate limiting and these momentary stops, you should never assume that
you are getting every tweet.

There is only one seed in a filter collection. Twitter filter collection are
either turned on or off (there is no schedule).

.. _guide-flickr-user-timeline:

.. _Flickr user:

-----------
Flickr user
-----------

Flickr User Timeline collections gather metadata about public photos by a
specific Flickr user, and, optionally, copies of the photos at specified sizes.

Each Flickr user collection can have multiple seeds, where each seed is a Flickr
user. To identify a user, you can provide a either a username or an NSID. If you
provide one, the other will be looked up and displayed in the SFM UI during the
first harvest. The NSID is a unique identifier and does not change; usernames
may be changed but are unique.

Usernames can be difficult to find, so to ensure that you have the correct
account, use `this tool <http://www.webpagefx.com/tools/idgettr/>`_ to find the
NSID from the account URL (i.e., the URL when viewing the account on the Flickr
website).

Depending on the image sizes you select, the actual photo files will be
collected as well. Be very careful in selecting the original file size, as this
may require a significant amount of storage. Also note that some Flickr users
may have a large number of public photos, which may require a significant amount
of storage. It is advisable to check the Flickr website to determine the number
of photos in each Flickr user's public photo stream before harvesting.

For each user, the user's information will be collected using Flickr's
`people.getInfo <https://www.flickr.com/services/api/flickr.people.getInfo.html>`_
API and the list of her public photos will be retrieved from `people.getPublicPhotos
<https://www.flickr.com/services/api/flickr.people.getPublicPhotos.html>`_.
Information on each photo will be collected with
`photos.getInfo <https://www.flickr.com/services/api/flickr.photos.getInfo.html>`_.

See :ref:`guide-incremental-collecting` to decide whether or not to collect
incrementally.

.. _guide-tumblr-blog-posts:

.. _Tumblr blog posts:

-----------------
Tumblr blog posts
-----------------

Tumblr Blog Post collections harvest posts by specified Tumblr blogs using the
`Tumblr Posts API <https://www.tumblr.com/docs/en/api/v2#posts>`_.

**Seeds** are individual blogs for these collections. Blogs can be specified with
or without the .tumblr.com extension.

See :ref:`guide-incremental-collecting` to decide whether or not to collect incrementally.

.. _guide-weibo-timelines:
.. _Weibo timeline:

--------------
Weibo timeline
--------------

Weibo Timeline collections harvest weibos (microblogs) by the user and friends
of the user whose credentials are provided using the `Weibo friends_timeline API
<http://open.weibo.com/wiki/2/statuses/friends_timeline>`_.

Note that because collection is determined by the user whose credentials are
provided, there are no seeds for a Weibo timeline collection. To change what is
being collected, change the user's friends from the Weibo website or app.

.. _Weibo search:

--------------
Weibo search
--------------

Collects recent weibos that match a search query using the `Weibo
search_topics API <http://open.weibo.com/wiki/2/search/topics>`_.
The Weibo API does not return a complete search of all Weibo posts. 
It only returns the most recent 200 posts matching a single keyword
when found between pairs of '#' in Weibo posts (for example: `#keyword#` or
`#你好#`)

The incremental option will attempt to only count weibo posts that haven't been harvested before,
maintaining a count of non-duplicate weibo posts.  Because the Weibo search API does not accept
`since_id` or `max_id` parameters, filtering out already-harvested weibos from the
search count is accomplished within SFM.

When the incremental option is not selected, the search will be performed again,
and there will most likely be duplicates in the count.


.. _guide-incremental-collecting:

----------------------
Incremental collecting
----------------------

The incremental option is the default and will collect tweets or posts that have been published since the last harvest. 
When the incremental option is not selected, the maximum number of tweets or posts will be harvested each 
time the harvest runs. If a non-incremental harvest is performed multiple times, there will most likely be
duplicates. However, with these duplicates, you may be able to track changes across time in a user's
timeline, such as changes in retweet and like counts, deletion of tweets, and follower counts.
