==========
User Guide
==========

Welcome to Social Feed Manager!

Social Feed Manager (SFM) is an open-source tool for collecting data from social
media sites, including Twitter, Flickr, Tumblr, and Weibo.

This guide is for users who are using SFM to collect. If you're an administrator
trying to set up SFM for your institution, see :ref:`admin-documentation`.

Blah Blah Blah
  * `Getting Started`_:
  * `What is SFM used for?`_: Collects tweets by a user-provided search query from recent tweets
  * ``_: Collects a Twitter provided stream of a subset of all tweets in real
    time.
  * `Twitter filter`_: Collects tweets by user-provided criteria from a stream of
    tweets in real time.
  * `Flickr user`_: Collects posts and photos from specific Flickr accounts
  * `Weibo timeline`_: Collects posts from the user and the user's friends
  * `Tumblr blog posts`_: Collects blog posts from specific Tumblr blogs
  * `Collecting Web resources`_: Secondary collections of resources linked to or
    embedded in social media posts.

---------------
Getting Started
---------------

Social Feed Manager (SFM) is designed for researchers, archivists, and curious
people to collect social media data from Twitter, Tumblr, Flickr, or Sina Weibo.

This introduction will help you get your first collection up and running. You
can always come back to this user guide for help.

If you want to learn more about what SFM can do, read 'What is SFM used for?'_:

This guide is for users who have access to SFM to get started on collecting. If
you're an administrator trying to set up SFM for your institution, see
:ref:`admin-documentation`.

Signing up
^^^^^^^^^^

Signing up is easy!

On the SFM homepage, click "Sign up." Fill out the field, including a unique
email. Once you sign up, you will be automatically logged in.


---------------------
What is SFM used for?
---------------------

Social Feed Manager (SFM) systematically collects individual posts--tweets,
photos, blogs--from social media sites. These posts are put into data files
called JSONs and made accessible in spreadsheet formats. Users can then use this
collected data for research, analysis or archiving.

To get started, click here, or continue reading to learn more.                              Add link for quick start?

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

  * `Twitter user timeline`_: Collect tweets from specific Twitter accounts
  * `Twitter search`_: Collects tweets by a user-provided search query from recent tweets
  * `Twitter sample`_: Collects a Twitter provided stream of a subset of all tweets in real
    time.
  * `Twitter filter`_: Collects tweets by user-provided criteria from a stream of
    tweets in real time.
  * `Flickr user`_: Collects posts and photos from specific Flickr accounts
  * `Weibo timeline`_: Collects posts from the user and the user's friends
  * `Tumblr blog posts`_: Collects blog posts from specific Tumblr blogs
  * `Collecting Web resources`_: Secondary collections of resources linked to or
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



.. _guide-weibo-credentials:

Sina Weibo Credentials
^^^^^^^^^^^^^^^^^^^^^^

Still needed

--------------------
Creating Collections
--------------------






-------------------
Exporting your Data
-------------------
