=========================================
 Data Dictionaries for CSV/Excel Exports
=========================================

Social Feed Manager captures a variety of data from each platform. These data
dictionaries give explanations for each selected and processed field in csv
exports.

* `Twitter Dictionary`_
* `Tumblr Dictionary`_
* `Flickr Dictionary`_

------------------
Twitter Dictionary
------------------

For more info about source tweet data, see the `Twitter API documentation
<https://dev.twitter.com/docs>`_, including `Tweets
<https://dev.twitter.com/docs/platform-objects/tweets>`_ and `Entities
<https://dev.twitter.com/docs/platform-objects/entities>`_.

Documentation about older archived tweets is archived by Wayback Machine for
`the Twitter API
<https://web.archive.org/web/*/https://dev.twitter.com/docs>`_, `Tweets
<https://web.archive.org/web/*/https://dev.twitter.com/overview/api/tweets>`_,
and `Entities
<https://web.archive.org/web/*/https://dev.twitter.com/overview/api/tweets>`_.

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+
| created_at              | Date and time the tweet was created, in             | 2016-12-21T19:30:03+00:00                        |
|                         | ISO 8601 format and UTC time zone.                  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| twitter_id              | Twitter identifier for the tweet.                   | 114749583439036416                               |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| screen_name             | The unique screen name of the account that          | NASA                                             |
|                         | authored the tweet, at the time the tweet was       |                                                  |
|                         | posted. Note that an account's screen name may      |                                                  |
|                         | change over time.                                   |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| followers_count         | Number of followers this account had at the time    | 235                                              |
|                         | the tweet was harvested.                            |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| friends_count           | Number of users this account was following at the   | 114                                              |
|                         | time the tweet was harvested.                       |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| favorite_count/         | Number of times this tweet had been favorited/liked | 12                                               |
| like_count              | by other users at the time the tweet was harvested. |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| retweet_count           | Number of times this tweet had been retweeted at    | 25                                               |
|                         | the time the tweet was harvested.                   |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| hashtags                | Hashtags from the tweet                             | Mars, askNASA                                    |
|                         | text, as a comma-separated list.                    |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| mentions                | Other Twitter accounts mentioned in the text of the | NASA_Airborne, NASA_Ice                          |
|                         | tweet, separated by comma and space.                |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| in_reply_to_screen_name | If the tweet is a reply, the screen name of         | wiredscience                                     |
|                         | the original tweet's author.                        |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| twitter_url             | URL of the tweet. If the tweet is a retweet made    | http://twitter.com/NASA/status/394883921303056384|
|                         | using the Twitter retweet feature, the URL will     | retweet redirecting to original tweet:           |
|                         | redirect to the original tweet.                     | http://twitter.com/NASA/status/394875351894994944|
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| text                    | The text of the tweet.  Newline characters are      | Observing Hurricane Raymond Lashing Western      |
|                         | stripped out.                                       | Mexico: Low pressure System 96E developed quickly|
|                         |                                                     | over the... http://t.co/YpffdKVrgm               |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| is_retweet              | `Yes` if tweet is a retweet of another tweet,       | Yes                                              |
|                         | according to the tweet's metadata; otherwise `No`.  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| is_quote                | `Yes` if tweet is a quote of another tweet,         | No                                               |
|                         | according to the tweet's metadata; otherwise `No`.  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| coordinates             | The geographic coordinates of the tweet.  This is   | [-0.22012208, 51.59248806]                       |
|                         | only enabled if geotagging is enabled on the        |                                                  |
|                         | account.  The value, if present, is of the form     |                                                  |
|                         | [longitude, latitude]                               |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url1                    | First URL in text of tweet, as shortened by         | http://t.co/WGJ9VmoKME                           |
|                         | Twitter.                                            |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url1_expanded           | Expanded version of `url1`; URL entered by user and | http://instagram.com/p/gA_zQ5IaCz/               |
|                         | displayed in Twitter. Note that the user-entered    |                                                  |
|                         | URL may itself be a shortened URL,                  |                                                  |
|                         | e.g. from bit.ly.                                   |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url2                    | Second URL in text of tweet, as shortened           | https://t.co/ZTUQZcikJa                          |
|                         | Twitter.                                            |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url2_expanded           | Expanded version of `url2`; URL entered by user and | http://instagram.com/p/gA_zQ5IaCz/               |
|                         | displayed in Twitter. Note that the user-entered    |                                                  |
|                         | URL may itself be a shortened URL,                  |                                                  |
|                         | e.g. from bit.ly.                                   |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| media_url               | URL of the media embedded in the tweet.  If the     | http://pbs.twimg.com/media/Cyir15CVIAAfAWd.jpg   |
|                         | media embedded in the tweet is a video, this is     |                                                  |
|                         | the URL of the video's thumbnail image              |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+



-----------------
Tumblr Dictionary
-----------------

For more info about source tweet data, see the `Tumblr API documentation
<https://www.tumblr.com/docs/en/api/v2>`_, particularly `Posts
<https://www.tumblr.com/docs/en/api/v2#posts>`_.

Documentation about older archived posts is archived by Wayback Machine for the
`original Tumblr API
<https://web.archive.org/web/*/https://www.tumblr.com/docs/en/api/>`_ and the
`newer Tumblr API
<https://web.archive.org/web/*/https://www.tumblr.com/docs/en/api/v2>`_.

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+
| created_at              | Date and time the tweet was created, in             | 2016-12-21 19:30:03+00:00                        |
|                         | ISO 8601 format and UTC time zone.                  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tumblr_id               | Tumblr identifier for the tweet.                    | 154774150409                                     |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| blog_name               | The short name used to uniquely identify a blog.    | nasa                                             |
|                         | This is the first part of the blog url, like        |                                                  |
|                         | <nasa.tumblr.com>.                                  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| post_type               | The type of post, such as one of the following:     | text                                             |
|                         | text, quote, link, answer, video, audio,            |                                                  |
|                         | photo, or chat.                                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| post_slug               | Text summary of the post, taken from the final      | 10-questions-for-our-chief-scientist             |
|                         | portion of the url.                                 |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| post_summary            | Text summary of the post, taken from the title      | 10 Questions for Our Chief Scientist             |
|                         | of the post.                                        |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| post_text               | Body of the post text, using html markup.           | *See* https://notepad.pw/w8133kzj                |
|                         |                                                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tags                    | Hashtags from the post                              | nasa, space, solarsystem,                        |
|                         | as a comma-separated list.                          | chiefscientist, scientist                        |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tumblr_url              | Full url location of the post.                      | `http://nasa.tumblr.com/post/154774150409/       |
|                         |                                                     | 10-questions-for-our-chief-scientist <http://    |
|                         |                                                     | nasa.tumblr.com/post/154774150409/10-questions-  |
|                         |                                                     | for-our-chief-scientist>`_                       |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tumblr_short_url        | Short url of the post.                              | https://tmblr.co/Zz_Uqj2G9GXq9                   |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+



-----------------
Flickr Dictionary
-----------------

For more info about source tweet data, see the `Flickr API documentation
<https://www.flickr.com/services/api/>`_, particularly *People* and *Photos*.

Documentation about older archived posts is archived by Wayback Machine `here
<https://web.archive.org/web/*/https://www.flickr.com/services/api/>`_.

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+
| photo_id                | Unique Flickr identifier of the photo.              | 11211844604                                      |
|                         |                                                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| date_posted             | Date and time that the post was uploaded to         | 2013-12-04 21:39:40+00:00                        |
|                         | Flickr, in ISO 8601 format and UTC time zone.       |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| date_taken              | Date and time that media was captured, either       | 6/7/2014 13:35                                   |
|                         | extracted from EXIF or from the date posted,        |                                                  |
|                         | in mm/dd/yyyy hh:mm format.                         |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| license                 | Licensing allowed for media, given as a             | 4                                                |
|                         | numeral according to the following key:             | *(Attribution license)*                          |
|                         |                                                     |                                                  |
|                         | - 0 = All Rights Reserved                           |                                                  |
|                         | - 1 = Attribution-NonCommercial-Sharealike License  |                                                  |
|                         | - 2 = Attribution-NonCommercial License             |                                                  |
|                         | - 3 = Attribution-NonCommercial NoDerivs License    |                                                  |
|                         | - 4 = Attribution License                           |                                                  |
|                         | - 5 = Attribution-ShareAlike License                |                                                  |
|                         | - 6 = Attribution-NoDerivs License                  |                                                  |
|                         | - 7 = No known copyright restrictions               |                                                  |
|                         | - 8 = United States Government work                 |                                                  |
|                         | - More information at creativecommons.org/licenses  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| safety_level            | Appropriateness of post, given as a numeral         | 0                                                |
|                         | according to the following key:                     | *(Safe level)*                                   |
|                         |                                                     |                                                  |
|                         | - 0 = Safe - Content suitable for everyone          |                                                  |
|                         | - 1 = Moderate - Approximately PG-13 content        |                                                  |
|                         | - 2 = Restricted - Approximately R rated content    |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| original_format         | File format of uploaded media.                      | jpg                                              |
|                         |                                                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| owner_nsid              | Unique Flickr identifier of the owner account.      | 28399705@N04                                     |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| owner_username          | Unique plaintext username of the owner account.     | GW Museum and Textile Museum                     |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| title                   | Title of the post.                                  | Original Museum entrance                         |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| description             | Short description of the post.                      | Historic photo courtesy of The Textile           |
|                         |                                                     | Museum Archives.                                 |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| media                   | Media type of the post.                             | photo                                            |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| photopage               | Location url of the post.                           | `https://www.flickr.com/photos/textilemuseum/    |
|                         |                                                     | 11211844604/                                     |
|                         |                                                     | <https://www.flickr.com/photos/textilemuseum/    |
|                         |                                                     | 11211844604/>`_                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
