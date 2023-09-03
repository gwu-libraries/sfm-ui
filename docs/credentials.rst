=================
 API Credentials
=================

Accessing the APIs of social media platforms requires credentials for
authentication (also knows as API keys). Social Feed Manager supports managing
those credentials. Credentials/authentication allow a user to collect data through a platform’s
API. For some social media platforms (e.g., Twitter and Tumblr), limits are
placed on methods and rate of collection on a per credential basis.

SFM users are responsible for creating their own new credentials so that
they can control their own collection rates and can ensure that they are
following each platform’s API policies.

Most API credentials have two parts: an application credential and a user
credential. (Flickr is the exception -- only an application credential
is necessary.)

For more information about platform-specific policies, consult the documentation
for each social media platform's API.

----------------------
 Managing credentials
----------------------

SFM supports two approaches to managing credentials: adding credentials and
connecting credentials. Both of these options are available from the
Credentials page.

Adding credentials
^^^^^^^^^^^^^^^^^^
For this approach, a user gets the application and/or user credential from the
social media platform and provides them to SFM by completing a form. More
information on getting credentials is below.

Connecting credentials
^^^^^^^^^^^^^^^^^^^^^^

*This is the easiest approach for users.*

For this approach, SFM is configured with the application credentials for the
social media platform by the systems administrator. The user credentials are
obtained by the user being redirected to the social media website to give
permission to SFM to access her account.

SFM is configured with the application credentials in the ``.env`` file.
If additional management is necessary, it can be performed using the Social
Accounts section of the Admin interface.


.. _twitter-credentials:

--------------------------
Adding Twitter Credentials
--------------------------

To harvest data from the Twitter API as of April 29, 2023, it is necessary to sign up **and pay for** `Basic access <https://developer.twitter.com/en/portal/products/basic>`_. (The "Free" access tier does not permit users to retrieve Tweets via API, only to publish them.)

Due to the low monthly limits on data retrieval imposed by Twitter (10K Tweets per month, as of 4/29/2023), each SFM user should obtain their own API credentials. 

To obtain application credentials:
  * Navigate to `<https://developer.twitter.com/en/apply-for-access>`_.
  * Sign in to Twitter, or create an account if you don't already have one.
  * Once you are logged into the Twitter Developer Portal, you can click the **Upgrade** button to upgrade your account to Basic Access.
  * Follow the prompts to describe your intended use case for academic research. 
  * When a description for your app is requested, you may include:
    *This is an instance of Social Feed Manager, a social media research and 
    archival tool, which collects data for
    academic researchers through an accessible user interface.*
  * Enter a website such as the Social Feed Manager URL. Any website will work.
  * You must provide a callback URL which is \h\t\t\p://<SFM hostname>/accounts/twitter/login/callback/. 
    Note that the URL should begin with *http*, not *https*, even if you are using https.
  * Turn on Enable Callback Locking and Allow this application to be used to Sign in with Twitter.
  * It is recommended to change the application permissions to read-only.
  * **Review and agree to the Twitter Developer Agreement**.
  
To manually add a Twitter Credential in your SFM user account:
  * Go to the Credentials page of SFM, and click `Add Twitter2 Credential`.
  * There are two ways of saving your credentials in SFM:
      1. Enter an `API key`, `API key secret`, `Access token`, and `Access token secret`.
      2. Or enter a `Bearer token` (recommended).
  * To obtain your credentials, visit the `Twitter Developer Portal Dashboard <https://developer.twitter.com/en/portal/dashboard>`_ and select your project. Under the `Apps` section, click on the key icon to access the `Keys and tokens` menu.
  * Generate the credentials needed (either the API key/secret and Access token/secret, or the Bearer token).
  * Save these keys, tokens, and secrets somewhere secure.
  * Enter the credentials in the Twitter2 Credential form on SFM, and click `Save`.

.. _flickr-credentials:

--------------------------
Adding Flickr Credentials
--------------------------

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
  * **Navigate to the SFM Credentials page** and click *Add Flickr Credential*
  * **Enter the Key and Secret** in the correct fields and save.


.. _tumblr-credentials:

--------------------------
Adding Tumblr Credentials
--------------------------

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


.. _weibo-credentials:

------------------------
Adding Weibo Credentials
------------------------
For instructions on obtaining Weibo credentials, see `this guide
<http://gwu-libraries.github.io/sfm-ui/posts/2016-04-26-weibo-api-guide>`_.

To use the connecting credentials approach for Weibo, the redirect URL must
match the application's actual URL and use port 80.
