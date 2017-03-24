==========
User Guide
==========

Welcome to Social Feed Manager!

Social Feed Manager (SFM) is an open-source tool designed for researchers,
archivists, and curious people to collect social media data from Twitter,
Tumblr, Flickr, or Sina Weibo.

If you want to learn more about what SFM can do, read :ref:`guide-uses`

This guide is for users who have access to SFM to learn how to collect. If
you're an administrator setting up SFM for your institution, see
:ref:`admin-documentation`.

To get your first collection up and running:
  * **Sign up**: On the SFM homepage, click "Sign up." Fill out the form,
    including a unique email. Once you sign up, you will be automatically logged in.
  * **Get credentials**: You'll need to authorize access to the social
    media platforms using credentials. See :ref:`guide-setting-up-credentials`.
  * **Create a collection set** and within it a collection, where you'll actually
    collect data. See :ref:`guide-creating-collections`.
  * **Add Seeds**: Seeds are the criteria used to collect data. You'll add user
    accounts or search criteria. See :ref:`guide-adding-seeds`.
  * **Set your collections running!**
  * **Export your collections** when you want to see and work with your data, or
    adjust settings. See :ref:`guide-export-data`.

You can always come back to this user guide for help by clicking *Documentation*
at the bottom of the SFM page and selecting *User Guide*

-----
Guide
-----

| `What is SFM used for?`_
|     `Types of Collections`_
|     `How to use the data`_
|     `Privacy and platform policy considerations`_
|         `Ethical considerations`_
| `Setting up Credentials`_
| `Creating Collections`_
|     `Setting up Collections and Collection Sets`_
|     `Adding Seeds`_
|         `Add Twitter User Timelines`_
|         `Add a Twitter Search`_
|         `Add a Twitter Sample`_
|         `Add a Twitter Filter`_
|         `Add Flickr User Timelines`_
|         `Add Tumblr Blog Posts`_
|         `Add Weibo Timelines`_
|         `Choosing Incremental Collecting`_
|         `Collecting Web Resources`_
| `Exporting your Data`_
|
|


.. _`guide-uses`:

---------------------
What is SFM used for?
---------------------

Social Feed Manager (SFM) collects individual posts--tweets,
photos, blogs--from social media sites. These posts are collected in a raw data
format called JOSN and can be exported in many formats, including spreadsheets.
Users can then use this collected data for research, analysis or archiving.

Try `Getting Started`_, or continue reading to learn more.

Some ideas for how to use SFM:
  - **Collecting from individual accounts** such as the tweets of every U.S.
    Senator (:ref:`guide-twitter-user-timelines`).
  - **Gathering Flickr images for analysis** or archiving the photographs from
    an institution like the Smithsonian (:ref:`guide-flickr-user-timeline`).
  - **Researching social media use** by getting a sample of all tweets
    (:ref:`guide-twitter-sample`), or by filtering by specific search terms
    (:ref:`guide-twitter-filter`).
  - **Capturing a major event** by collecting tweets in a specific geographic
    location or by following specific hashtags.
  - **Collecting Tumblr posts** for preserving artistic entries
    (:ref:`guide-tumblr-blog-posts`).
  - **Archiving posts** from any social media platform for later research.
  - **Analyzing trends** by :ref:`exploring` (note that ELK requires coding
    ability--contact your SFM administrator for help).

Note that SFM currently collects social media data from Twitter, Tumblr, Flickr,
and Sina Weibo.


Types of Collections
^^^^^^^^^^^^^^^^^^^^

  * :ref:`guide-twitter-user-timelines`: Collect tweets from specific
    Twitter accounts
  * :ref:`guide-twitter-search`: Collects tweets by a user-provided search query
    from recent tweets
  * :ref:`guide-twitter-sample`: Collects a Twitter-provided stream of a subset
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
  * You could export it into a CSV or Excel format for a basic analysis
    (:ref:`guide-export-data`), or load the format into analysis software such
    as Stata, SPSS, or Gephi.
  * You could use try :ref:`exploring`, a processor for data analysis (although
    ELK requires coding ability, so ask your SFM admin for help if you need it).
  * You could set up an archive using the JSON files or Excel files.

Privacy and platform policy considerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Collecting and using data from social media platforms is subject to those
platforms' terms (`Twitter <https://twitter.com/rules>`_,
`Flickr <https://www.flickr.com/help/guidelines>`_,
`Sina Weibo <http://www.weibo.com/signup/v5/protocol>`_,
`Tumblr <https://www.tumblr.com/policy/en/terms-of-service>`_),
as you agreed to them when you created your social media account. Social Feed
Manager respects those platforms' terms as an application
(`Twitter <https://dev.twitter.com/overview/terms/policy>`_,
`Flickr <https://www.flickr.com/services/developer>`_,
`Sina Weibo <http://open.weibo.com/wiki/%E9%A6%96%E9%A1%B5>`_,
`Tumblr <https://www.tumblr.com/docs/en/api_agreement>`_).

Social Feed Manager provides data to you for your research and academic use.
Social media platforms' terms of service generally do not allow republishing of
full datasets, and you should refer to their terms to understand what you may
share. Authors typically retain rights and ownership to their content.

Take a look at
`these guidelines <https://gwu-libraries.github.io/sfm-ui/resources/guidelines>`_
on social media collection development.

Ethical considerations
----------------------

In addition to respecting the platforms' terms, as a user of Social Feed Manager
and data collected within it, it is your responsibility to consider the ethical
aspects of collecting and using social media data. Your discipline or
professional organization may offer guidance.

Many people have written about the important ethical and legal considerations in
collecting and using social media data. To begin understanding these aspects,
here are a few resources with which to start:

* Social Feed Manager's `"Building Social Media Archives: Collection Development
  Guidelines" <https://gwu-libraries.github.io/sfm-ui/resources/guidelines>`_,
  2017
* Sara Mannheimer and Elizabeth A. Hull, `"Sharing selves: Developing an ethical
  framework for curating social media data"
  <https://scholarworks.montana.edu/xmlui/bitstream/handle/1/12661/Mannheimer-Hull-Sharing-Selves-2017.pdf>`_,
  2017.
* Association of Internet Researchers, `“Ethical Decision-Making and Internet
  Research” <http://aoir.org/reports/ethics2.pdf>`_, 2012.
* Annette Markham, `“OKCupid data release fiasco”
  <https://points.datasociety.net/okcupid-data-release-fiasco-ba0388348cd>`_,
  May 18, 2016.
* North Carolina State University Libraries, `“Social Media Toolkit: Legal and
  Ethical Implications”
  <https://www.lib.ncsu.edu/social-media-archives-toolkit/legal>`_, 2015.
* Katrin Weller and Katharina Kinder-Kurlanda, `“A manifesto for data sharing in
  social media research”
  <https://www.lib.ncsu.edu/social-media-archives-toolkit/legal>`_,
  Proceedings of the 8th ACM Conference on Web Science, 2016.



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

| :ref:`twitter-credentials`
| :ref:`flickr-credentials`
| :ref:`tumblr-credentials`
| :ref:`weibo-credentials`
|
|



.. _guide-creating-collections:

--------------------
Creating Collections
--------------------

**Collections** are the most basic SFM levels used to gather social media data.
Each collection either gathers posts from individual accounts or gathers posts based
on search criteria.

Collections are contained in **collection sets**. While collection sets
sometimes only include one collection, sets can be used to organize all of the
data from a single project or archive--for example, a collection set about a
band might include a collection of the Twitter user timelines of each band
member, a collection of the band's Flickr, and a Twitter Filter collection of
tweets that use the band's hashtag.

Before you begin collecting, you may want to consider these `collection
development guidelines
<https://gwu-libraries.github.io/sfm-ui/resources/guidelines>`_.

Setting up Collections and Collection Sets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because collections are housed in collection sets, you must make a collection
set first.

Navigate to the Collection Sets page from the top menu, then click the *Add
Collection Set* button.

Give the collection set a unique name and description. A collection set is like
a folder for all collections in a project.

If you are part of a group project, you can contact your SFM administrator and
set up a new group which you can share each collection set with. (This can be
changed or added later on).

Once you are in a collection set, click the "Add Collection" dropdown menu and
select the collection type you want to add.

Enter a unique collection name and a short description. The description is a
great location to describe how you chose what to put in your collection.

Select which credential you want to use. If you need to set up new credentials,
see :ref:`guide-setting-up-credentials`.

.. _guide-adding-seeds:

Adding Seeds
^^^^^^^^^^^^

**Seeds** are the criteria used by SFM to collect social media posts. Seeds may
be individual social media accounts or search terms used to filter posts.

The basic process for adding seeds is the same for every collection type, except
for Twitter Sample:

  * Turn off the collection.
  * Click *Add Seed* for adding one seed or *Add Bulk Seeds* for multiple.
  * Enter either the user ids or search criteria and save.
  * When you have added all seeds you want, click *Turn on*.

.. _guide-twitter-user-timelines:

Add Twitter User Timelines
--------------------------

Twitter user timeline collections collect the 3,200 most recent tweets from
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

**Seeds** are individual blogs for these collections. Blogs can be specified with
or without the .tumblr.com extension.

See :ref:`guide-incremental-collecting` to decide whether or not to collect incrementally.

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


.. _guide-export-data:

-------------------
Exporting your Data
-------------------

In order to access the data in a collection, you will need to export it.

With normal exports, you are able to download your data in several formats,
including Excel (.xlsx) and Comma Separated Value (.csv) files, which can be
loaded into spreadsheet or data analytic software.

To export:
  * At the top of the individual collection, click *Export*.

  * Select the file type you want (.csv is recommended; .xlsx types will also be
    easily accessible).

  * Select the export size you want, based on number of posts per file. Note that
    larger file sizes will take longer to download.

  * Select Deduplicate if you only want one instance of every post. This will clean
    up your data, but will make the export take longer.

  * Item start date/end date allow you to limit the export based on the date
    each post was created.

  * Harvest start date/end date allow you to limit the export based on the
    harvest dates.

  * When you have the settings you want, click *Save*. You will be
    redirected to the export screen. When the export is complete, the files,
    along with a README file describing what was included in the export and the
    collection, will appear for you to click on and download. You will receive
    an email as well when your export completes.

  * To help understand each category of meta-data in each export, see
    :ref:`data-dictionaries`.


For the advanced processing provided by ELK, see
:ref:`Commandline exporting/processing`.
