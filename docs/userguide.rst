==========
User Guide
==========

Welcome to Social Feed Manager!

Social Feed Manager (SFM) is an open-source tool for collecting data from social
media sites, including Twitter, Flickr, Tumblr, and Weibo.

This guide is for users who are using SFM to collect. If you're an administrator
trying to set up SFM for your institution, see :ref:`admin-documentation`.

Guide
^^^^^

| `Getting Started`_
| `What is SFM used for?`_
|     `Types of Collections`_
|     `How to use the data`_
| `Setting up Credentials`_
|     :ref:`guide-twitter-credentials`
|           :ref:`guide-manual-twitter-credentials`
|     :ref:`guide-flickr-credentials`
|     :ref:`guide-tumblr-credentials`
|     :ref:`guide-weibo-credentials`
| `Creating Collections`_
|    `Adding Seeds`_
|    :ref:`guide-twitter-user-timelines`
|    :ref:`guide-twitter-search`
|    :ref:`guide-twitter-sample`
|    :ref:`guide-twitter-filter`
|    :ref:`guide-flickr-user-timeline`
|    :ref:`guide-tumblr-blog-posts`
|    :ref:`guide-weibo-timelines`
|    `Choosing Incremental Collecting`_
|    `Collecting Web Resources`_
| `Exporting your Data`_
|
|

---------------
Getting Started
---------------

Social Feed Manager (SFM) is designed for researchers, archivists, and curious
people to collect social media data from Twitter, Tumblr, Flickr, or Sina Weibo.

This is a quick summary of steps to get your first collection up and running.
You can always come back to this user guide for help.

If you want to learn more about what SFM can do, read :ref:`guide-uses`

This guide is for users who have access to SFM to get started on collecting. If
you're an administrator trying to set up SFM for your institution, see
:ref:`admin-documentation`.

* **Sign up**: On the SFM homepage, click "Sign up." Fill out the field,
  including a unique email. Once you sign up, you will be automatically logged in.
* **Get credentials**: You'll need to connect credential authorization through
  the social media platform you want. See :ref:`guide-setting-up-credentials`.
* **Create a collection Set** and within it a collection, where you'll actually
  collect data. See :ref:`guide-creating-collections`.
* **Add Seeds**: Seeds are the criteria used to collect data. You'll add user
  accounts or search criteria. See :ref:`guide-adding-seeds`.
* **Set your collections running!**
* **Export your collections** when you want to see and work with your data, or
  adjust settings. See :ref:`guide-export-data`.



.. _`guide-uses`:

---------------------
What is SFM used for?
---------------------

Social Feed Manager (SFM) systematically collects individual posts--tweets,
photos, blogs--from social media sites. These posts are put into data files
called JSONs and made accessible in spreadsheet formats. Users can then use this
collected data for research, analysis or archiving.

Try `Getting Started`_, or continue reading to learn more.

Some ideas for how to use SFM:
  - **Collecting from individual accounts** like the tweets of every U.S. Senator.          Add link for twitter user timeline instructions
  - **Gathering Flickr images for analysis** like comparing the styles of active            Add link for Flickr user timeline
    photographers.
  - **Researching social media use** by getting a sample of all tweets, or by               Add link for Twitter Sample and Twitter Filter
    filtering by specific search terms.
  - **Capturing a major event** by collecting tweets in a specific geographic               Add link for blogs about geographic location and event capture
    location or by following specific hashtags.
  - **Collecting Tumblr posts** for preserving artistic entries.                            Add link for Tumblr user timeline instructions
  - **Archiving posts** from any social media platform for later research.                  Add link for blog about archiving
  - **Analyzing trends** using the ELK processing tool (note that ELK requires              Add link for ELK
    coding ability--contact your SFM administrator for help).

Note that SFM only collects social media data from Twitter, Tumblr, Flickr, and
Sina Weibo.


Types of Collections
^^^^^^^^^^^^^^^^^^^^

  * :ref:`guide-twitter-user-timelines`: Collect tweets from specific
    Twitter accounts
  * :ref:`guide-twitter-search`: Collects tweets by a user-provided search query
    from recent tweets
  * :ref:`guide-twitter-sample`: Collects a Twitter provided stream of a subset
    of all tweets in real time.
  * :ref:`guide-twitter-filter`: Collects tweets by user-provided criteria from
    a stream of tweets in real time.
  * :ref:`guide-flickr-user-timeline`: Collects posts and photos from specific
    Flickr accounts
  * :ref:`guide-weibo-timelines`: Collects posts from the user and the user's
    friends
  * :ref:`guide-tumblr-blog-posts`: Collects blog posts from specific Tumblr
    blogs
  * :ref:`guide-web-resources`: Secondary collections of resources linked to or
    embedded in social media posts.

How to use the data
^^^^^^^^^^^^^^^^^^^

Once you've collected data, there are a few ways to use it:
  * You could export it into a CSV or Excel format for analysis.                          Add link for exports
  * You could use the ELK processor for data analysis (although ELK requires              Add link for processing
    coding ability, so ask your SFM admin for help).
  * You could set up an archive using the JSON files or excel files.                      Add link for archive blog post

There are some limitations on how data may be used due to each platform's
policies and due to privacy concerns. See here for details.                               Add relevant link


.. _guide-setting-up-credentials:

----------------------
Setting up Credentials
----------------------

Before you can start collecting, you need **credentials** for the social media
platform that you want to use. Credentials are keys used by each platform to
control the data they release to you.

You are responsible for creating your own credentials so that you can control
your own collection rate and make sure that you are following the policies of
each platform.

For more information about platform-specific policies, consult the documentation
for each social media platform's API.

:ref:`guide-twitter-credentials`

:ref:`guide-flickr-credentials`

:ref:`guide-tumblr-credentials`

:ref:`guide-weibo-credentials`



.. _guide-twitter-credentials:

Twitter Credentials
^^^^^^^^^^^^^^^^^^^

The easiest way to set up Twitter credentials is to connect them to your
personal Twitter account (or another Twitter account you control). If you want
more fine-tuned control, you can manually set up application-level credentials
(see below).

To connect to Twitter credentials, first sign in to Twitter with the account you
want to use. Then, on the Credentials page, click *Connect to Twitter*. A
window will pop up from Twitter, asking you for authorization. Click authorize,
and your credentials will automatically connect.

Once credentials are connected, you can start :ref:`guide-creating-collections`.

.. _guide-manual-twitter-credentials:

Manually Adding Twitter Credentials
-----------------------------------

Manually adding Twitter Credentials, rather than connecting them automatically
using your Twitter account (see above), gives you greater control over your
credentials and allows you to use multiple credentials.

To manually add credentials:
  * **Navigate to** https://apps.twitter.com/.

  * **Sign in to Twitter and select "Create New App."**

  * **Enter a name for the app** like *Social Feed Manager* or the name of a new
    Collection Set.
  * **Enter a description.** You may copy and paste:
    *This is a social media research and archival tool, which collects data for
    academic researchers through an accessible user interface.*
  * **Enter a Website** such as the SFM url. Any website will work.
  * **Enter a Callback URL** such as the same url used for the website field.
  * **Review and agree to the Twitter Developer Agreement** and click *Create your Twitter
    Application.*
  * Recommended:
      * Click on your new application.
      * Navigate to the *Permissions* tab.
      * Select *Read only* then *Update settings*.
  * **Go to the Credentials page of SFM,** and click *Add Twitter Credential*.
  * Fill out all fields:
      * On the Twitter apps page (https://apps.twitter.com/) click your new
        application.
      * Navigate to the *Keys and Access Tokens* tab.
      * From the top half of the page, copy and paste into the matching fields
        in SFM: *Consumer Key* and *Consumer Secret*.
      * From the bottom half of the page, copy and paste into the matching
        fields in SFM: *Access Token* and *Access Token Secret*.
  * **Click** *Save*
Once credentials are connected, you can start :ref:`guide-creating-collections`.

.. _guide-flickr-credentials:

Flickr Credentials
^^^^^^^^^^^^^^^^^^

* **Navigate to** https://www.flickr.com/services/api/keys/.
* **Sign in to your Yahoo! account.**
* **Click** *Get Another Key*
* **Choose** *Apply for a Non-commercial key,* which is for API users that are
  not charging a fee.
* **Enter an Application Name** like *Social Feed Manager*
* **Enter Application Description** such as: *This is a social media research
  and archival tool, which collects data for academic researchers through an
  accessible user interface.*
* **Check both checkboxes**
* **Click** *Submit*
* **Navigate to the SFM Credentials page** and click *Add Flicker Credential*
* **Enter the Key and Secret** in the correct fields and save.
Once credentials are connected, you can start :ref:`guide-creating-collections`.


.. _guide-tumblr-credentials:

Tumblr Credentials
^^^^^^^^^^^^^^^^^^

* **Navigate to** https://www.tumblr.com/oauth/apps/.
* **Sign in to Tumblr.**
* **Click** *Register Application*
* **Enter an Application Name** like *Social Feed Manager*
* **Enter a website** such as the SFM url
* **Enter Application Description** such as: *This is a social media research
  and archival tool, which collects data for academic researchers through an
  accessible user interface.*
* **Enter Administrative contact email.** You should use your own email.
* **Enter default callback url,** the same url used for the website.
* **Click** *Register*
* **Navigate to the SFM Credentials page** and click *Add Tumblr Credential*
* **Enter the OAuth Consumer Key** in the API key field and save.
Once credentials are connected, you can start :ref:`guide-creating-collections`.



.. _guide-weibo-credentials:

Sina Weibo Credentials
^^^^^^^^^^^^^^^^^^^^^^

Still needed
Once credentials are connected, you can start :ref:`guide-creating-collections`.


.. _guide-creating-collections:

--------------------
Creating Collections
--------------------

**Collections** are the most basic SFM levels used to gather social media data.
Each collection either gathers posts from individual accounts or gathers posts based
on search criteria.

Collections are contained in **Collection Sets**. While Collecion Sets sometimes
only include one collection, sets can be used to organize all of the data from
a single project or archive--for example, a Collection Set about a band might
include a collection of the Twitter user timelines of each band member, a collection of
the band's Flickr, and a Twitter Filter collection of tweets that use the band's
hashtag.

##Instructions about Collection Sets##

Once you are in a Collection Set, click the "Add Collection" dropdown menu and
select the collection type you want to add.

Enter a unique Collection name and a short description. The description is a
great location to describe how you chose what to put in your collection.

Select which credential you want to use. If you need to set up new credentials,
see :ref:`guide-setting-up-credentials`.

.. _guide-adding-seeds:

Adding Seeds
^^^^^^^^^^^^

**Seeds** are the criteria used by SFM to collect social media posts. Seeds may
be individual social media accounts or search terms used to filter posts.

The basic process for adding seeds is the same for every collection type, except
for Twitter Samples:

  * The collection must be turned off first.
  * Then click *Add Seed* for adding one seed or *Add Bulk Seeds* for multiple.
  * Then enter either the user ids or search criteria and save.
  * Finally, when you have added all seeds you want, click *Turn on*

.. _guide-twitter-user-timelines:

Add Twitter User Timelines
--------------------------

Twitter user timeline collections collect the 32,000 most recent tweets from
a list of Twitter accounts.

**Seeds** for Twitter User Timelines are individual Twitter accounts.

To identify a user timeline, you can provide a screen name
(the string after @, like NASA for @NASA, which the user can change)
or Twitter user ID (a numeric string which never changes, like 11348282 for
@NASA). If you provide one identifier, the other will be looked up and displayed
in SFM UI the first time the harvester runs.

Scheduling harvests should depend on how prolific the Twitter users are.
In general, the more frequent the tweeter, the more frequent you’ll want to
schedule harvests.

See :ref:`guide-incremental-collecting` to decide whether or not to collect
incrementally.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect media or web resources.

.. _guide-twitter-search:

Add a Twitter Search
--------------------

Twitter searches collect tweets from the last 7-9 days that match search
queries, similar to a regular search made on Twitter.
Based on relevance, this is **not** a complete search of all tweets, limited
both by time and arbitrary relevance (determined by Twitter).

Search queries must follow standard search term formulation; permitted queries
are listed in the documentation for the `Twitter Search API
<https://dev.twitter.com/rest/public/search>`_, or you can construct a query
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

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect media or web resources.

.. _guide-twitter-sample:

Add a Twitter Sample
--------------------

Twitter samples are a random collection of approximately 0.5--1% of public
tweets, useful for capturing a sample of what people are tweeting about.

Unlike other Twitter collections, there are no seeds for a Twitter sample.

When on, the sample returns data every 30 minutes.

Only one sample or *Twitter Filter* can be run at a time per credential.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collection media or web resources.

.. _guide-twitter-filter:

Add a Twitter Filter
--------------------

Twitter Filter collections harvest a live selection of public tweets from
criteria matching keywords, locations, or users. Because tweets are collected
live, tweets from the past are not included. (Use a *Twitter Search* collection
to find tweets from the recent past.)

There are three different filter queries supported by SFM: track, follow, and
location.

**Track** collects tweets based on a keyword search A space between words
is treated as 'AND' and a comma is treated as 'OR'. Note that exact phrase
matching is not supported. See the `track parameter documentation
<https://dev.twitter.com/streaming/overview/request-parameters#track>`_ for more
information.

**Follow** collects tweets that are posted by or about a user (not including
mentions) from a comma separated list of user IDs (the numeric identifier for
a user account). Tweets collected will include those made by the user, retweeting
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

Only one filter or *Twitter Sample* can be run at a time per credential.

SFM captures the filter stream in 30 minute chunks and then momentarily stops.
Between rate limiting and these momentary stops, you should never assume that
you are getting every tweet.

There is only one seed in a filter collection. Twitter filter collection are
either turned on or off (there is no schedule).

See the :ref:`Collecting web resources` guidance below for deciding whether to
collection media or web resources.

.. _guide-flickr-user-timeline:

Add Flickr User Timelines
-------------------------

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

See :ref:`guide-incremental-collecting` to decide whether or not to collect
incrementally.

.. _guide-tumblr-blog-posts:

Add Tumblr Blog Posts
---------------------

Tumblr Blog Post collections harvest posts from a list of Tumblr blogs.

**Seeds* are individual blogs for these collections. Blogs can be specified with
 or without the .tumblr.com extension.

 See :ref:`guide-incremental-collecting` to decide whether or not to collect
 incrementally.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect image or web resources.

.. _guide-weibo-timelines:

Add Weibo Timelines
-------------------

Weibo Timeline collections harvest weibos (microblogs) by the user and friends
of the user whose credentials are provided.

Note that because collection is determined by the user whose credentials are
provided, there are no seeds for a Weibo timeline collection. To change what is
being collected, change the user's friends from the Weibo website or app.

See the :ref:`Collecting web resources` guidance below for deciding whether to
collect image or web resources.

.. _guide-incremental-collecting:

Choosing Incremental Collecting
-------------------------------

The incremental option will collect tweets that haven't been harvested before,
preventing duplicate tweets. When the incremental option is not selected, the
3,200 most recent tweets will be collected. If a non-incremental harvest is
performed multiple times, there will most likely be
duplicates. However, you will may be able to track changes across time about a user's
timeline, such as retweet and like counts, deletion of tweets, and follower
counts.

.. _guide-web-resources:

Collecting Web Resources
------------------------

Most collection types allow you to select an option to collect web resources
such as images, web pages, etc. that are included in the social media post. When
a social media post includes a URL, SFM will harvest the web page at that URL.
It will harvest only that web page, not any pages linked from that page.

Be very deliberate in collecting web resources. Performing a web harvest both
takes longer and requires significantly more storage than collecting the
original social media post.

.. _guide-export-data:

-------------------
Exporting your Data
-------------------

In order to access the data collected in any harvest, you will need to export it.

For the advanced processing provided by ELK, see
:ref:`Commandline exporting/processing`.

With normal exports, you are able to download yoru data in several formats,
including Excel (.xlsx) and Comma Separated Value (.csv) files, which can be
loaded into spreadsheet or data analytic software.

At the top of the individual collection, click *Export*.

Select the file type you want (.csv is recommended; .xlsx types will also be
easily accessible).

Select the export size you want, based on number of posts per file. Note that
larger file sizes will take longer to download.

Select Deduplicate if you only want one instance of every post. This will clean
up your data, but will make the export take longer.

Item start date/end date allow you to define when you want data from, as
embedded in each post.

Harvest start date/end date allow you to define when you want data from
based on your harvest dates.

When you have the settings you want, click *Save*. At this point, you will be
redirected to the export screen. When the export is complete, the files will
appear for you to click on and download. You will receive an email as well when
your export completes.
