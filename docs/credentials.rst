=================
 API Credentials
=================

Accessing the APIs of social media platforms requires credentials for authentication
(also knows as API keys). Social Feed Manager supports managing those credentials.

Credentials/authentication allow a user to collect data through a platform’s
API. Limits are placed on methods and rate of collection on a per credential
basis.

SFM users are responsible for creating their own new credentials so that
they can control their own collection rates and can ensure that they are
following each platform’s API policies.

Most API credentials have two parts: an application credential and a user
credential.(Flickr is the exception -- only an application credential
is necessary.)

For more information about platform-specific policies, consult the documentation
for each social media platform's API.

----------------------
 Managing credentials
----------------------

SFM supports two approaches to managing credentials: adding credentials and connecting
credentials. Both of these options are available from the Credentials page.

Adding credentials
^^^^^^^^^^^^^^^^^^
For this approach, a user gets the application and/or user credential from the social
media platform and provide them to SFM by completing a form. More information on getting
credentials is below.

Connecting credentials
^^^^^^^^^^^^^^^^^^^^^^
For this approach, SFM is configured with the application credentials for the social
media platform. The user credentials are obtained by the user being redirected to the social
media website to give permission to SFM to access her account.

SFM is configured with the application credentials in the ``docker-compose.yml``. If additional
management is necessary, it can be performed using the Social Accounts section of the Admin
interface.

*This is the easiest approach for users.* Configuring application credentials is encouraged.

--------------------
 Platform specifics
--------------------

Twitter
^^^^^^^
Twitter credentials can be obtained from `https://apps.twitter.com/ <https://apps.twitter.com/>`_. It is recommended to change
the application permissions to read-only.  You *must* provide a callback URL, but the URL you provide doesn't matter.

Weibo
^^^^^
For instructions on obtaining Weibo credentials, see `this guide <http://gwu-libraries.github.io/sfm-ui/posts/2016-04-26-weibo-api-guide>`_.

To use the connecting credentials approach for Weibo, the redirect URL must match
the application's actual URL and use port 80.

Flickr
^^^^^^

Flickr credentials can be obtained from `https://www.flickr.com/services/api/keys/ <https://www.flickr.com/services/api/keys/>`_.

Flickr does not require user credentials.

Tumblr
^^^^^^

Tumblr credentials can be obtained from `https://www.tumblr.com/oauth/apps <https://www.tumblr.com/oauth/apps>`_.
