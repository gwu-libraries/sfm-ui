================
Collection types
================

Each collection type connects to one of a social media platform's APIs, or methods for retrieving data. Understanding
what each collection type provides is important to ensure you collect what you need and are aware of any limitations.
Reading the social media platform's documentation provides further important details.

.. _Twitter search:

---------------
Twitter search
---------------

Queries the `Twitter Search API <https://dev.twitter.com/rest/public/search>`_ to retrieve public tweets from a sampling
of tweets from the most recent 7-9 days. This is not a comprehensive search of all tweets.

To formulate a search query,
use the `Twitter Advanced Search query builder <https://twitter.com/search-advanced>`_. Pay careful attention to the
query syntax described in Twitter’s documentation.  This query is the seed for the collection; Twitter search
collections only have one seed.

Due to Twitter’s rate limits and the amount of data available from the Search API, broad Twitter searches may take a
long time to complete (up to multiple days).  In choosing a schedule, make sure that there is enough time between
searches.  In some cases, you may only want to run the search once and then turn off the collection.

If the incremental option is selected, only new tweets (i.e., tweets that have not yet been harvested in this
collection) will be harvested.  In general, you will want to select the incremental option.

See the :ref:`Collecting web resources` guidance below for deciding whether to collection media or web resources.

.. _Twitter filter:

---------------
Twitter filter
---------------

Collects public tweets from the `Twitter filter streaming API <https://dev.twitter.com/streaming/reference/post/statuses/filter>`_,
matching keywords, locations, or users. The tweets are from the current time going forward. Tweets from the past are
not available with this collection type. (Create a Twitter search collection with the same terms to collect tweets from
the recent past).

When creating a Twitter filter pay careful attention to query syntax described in Twitter’s documentation.  The filter
query is the seed for the collection; Twitter filter collections only have one seed.

There are limits on how many tweets Twitter will supply, so filters on high-volume terms/hashtags will not return all tweets
available.  Thus, you will want to strategize about how broad/narrow to construct your filter. Twitter only allows you
to run one filter at a time with a set of Twitter API credentials; SFM enforces this for you.

SFM captures the filter stream in 30 minute chunks and then momentarily stops.  Between rate limiting and this momentary
stop, you should never assume that you are getting every tweet.

Unlike other collection types, Twitter filter collections are either turned on or off; they do not operate according to
a schedule.

See the :ref:`Collecting web resources` guidance below for deciding whether to collection media or web resources.

.. _Twitter user timeline:

---------------------
Twitter user timeline
---------------------

Collects tweets by a particular Twitter user account using `Twitter's user_timeline API <https://dev.twitter.com/rest/reference/get/statuses/user_timeline>`_.
Twitter provides up to the most recent 3,200 tweets by that account, provided a limited ability to collect tweets from
the past.

Each Twitter user timeline collection can have multiple seeds, where each seed is a user timeline. To identify a user
timeline, you can provide a screen name or Twitter user ID (UID). If you provide one, the other will be looked up and
displayed in SFM UI. The Twitter user ID is a number and does not change; a user may change her screen name.  The user
ID will be used for retrieving the user timeline.

There is no limit on the number of user timeline seeds supported in a collection.  However, they may take a long time 
to collect due to Twitter’s rate limits.

Note that SFM will handle incorrect or private user timeline seeds. You will be notified when these are found; the other
valid seeds will be collected.

If the incremental option is selected, only new tweets (i.e., tweets that have not yet been harvested for that user
timeline) will be harvested, meaning you will not collect duplicate tweets. If the incremental option is not selected,
you will collect the most 3,200 recent tweets, meaning you will get duplicates across harvests. However, you may be able
to examine differences across time in a user’s timeline, e.g., deleted tweets, or track changes in follower or
retweet counts.

In choosing a schedule, you may want to consider how prolific a tweeter the Twitter user is. In general, the more
frequent the tweeter, the more frequent you’ll want to schedule harvests.

See the :ref:`Collecting web resources` guidance below for deciding whether to collection media or web resources.

.. _Twitter sample:

--------------
Twitter sample
--------------

Collects tweets from the `Twitter sample stream <https://dev.twitter.com/streaming/reference/get/statuses/sample>`_.
The Twitter sample stream returns approximately 0.5-1% of public tweets, which is approximately 3GB a day (compressed).

See the :ref:`Collecting web resources` guidance below for deciding whether to collection media or web resources.

.. _Flickr user:

-----------
Flickr user
-----------

Collects metadata about public photos by a specific Flickr user.

Each Flickr user collection can have multiple seeds, where each seed is a Flickr user. To identify a user,
you can provide a either a username or an NSID. If you provide one, the other will be looked up and displayed in the
SFM UI. The NSID is a unique identifier and does not change; a user may change her username.

For each user, the user's information will be collected using Flickr's `people.getInfo <https://www.flickr.com/services/api/flickr.people.getInfo.html>`_ API and the list of her public
photos will be retrieved from `people.getPublicPhotos <https://www.flickr.com/services/api/flickr.people.getPublicPhotos.html>`_. Information on each photo will be collected with
`photos.getInfo <https://www.flickr.com/services/api/flickr.photos.getInfo.html>`_.

Depending on the image sizes you select, the actual photo files will be collected as well. Be very careful in selecting
the original file size, as this may require a significant amount of storage. Also note that some Flickr users may have 
a large number of public photos, which may require a significant amount of storage. It is advisable to check the Flickr
website to determine the number of photos in each Flickr user's public photo stream before harvesting.

If the incremental option is selected, only new photos will be collected.

.. _Weibo timeline:

--------------
Weibo timeline
--------------

Collects Weibos by the user and friends of the user whose credentials are provided using the
`Weibo friends_timeline API <http://open.weibo.com/wiki/2/statuses/friends_timeline>`_.

Note that because collection is determined by the user whose credentials are provided, there are no seeds for a
Weibo timeline collection. To change what is being collected, change the user's friends from the Weibo website
or app.

See the :ref:`Collecting web resources` guidance below for deciding whether to collect image or web resources.

.. _Tumblr blog posts:

-----------------
Tumblr blog posts
-----------------
Collects blog posts by a specified Tumblr blog using the `Tumblr Posts API <https://www.tumblr.com/docs/en/api/v2#posts>`_.

Each Tumblr blog post collection can have multiple seeds, where each seed is a blog. The blog can be specified
with or without the .tumblr.com extension.

If the incremental option is selected, only new blog posts will be collected.

See the :ref:`Collecting web resources` guidance below for deciding whether to collect image or web resources.

.. _Collecting web resources:

------------------------
Collecting Web resources
------------------------
Each collection type allows you to select an option to collect web resources such as images, web pages, etc. that are
included in the social media post. When a social media post includes a URL, SFM will harvest the web page at that URL.
It will harvest only that web page, not any pages linked from that page.

Be very deliberate in collecting web resources.  Performing a web harvest both takes longer and requires significantly
more storage than collecting the original social media post.
