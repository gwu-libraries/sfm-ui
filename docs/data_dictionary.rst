.. _data-dictionaries:

=========================================
 Data Dictionaries for CSV/Excel Exports
=========================================

Social Feed Manager captures a variety of data from each platform. These data
dictionaries give explanations for each selected and processed field in
exports.

Note that these are subsets of the data that are collected for each
post. The full data is available for export by selecting "Full JSON" as the export format
or by exporting from the commandline. See :doc:`processing`.

* `Twitter Dictionary`_
* `Tumblr Dictionary`_
* `Flickr Dictionary`_
* `Weibo Dictionary`_

------------------
Twitter Dictionary
------------------

For more info about source tweet data, see the `Twitter API documentation
<https://developer.twitter.com/en/docs>`_, including `Tweet data dictionaries
<https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/intro-to-tweet-json>`_.

Documentation about older archived tweets is archived by the Wayback Machine for
the `Twitter API
<https://web.archive.org/web/*/https://dev.twitter.com/docs>`_, `Tweets
<https://web.archive.org/web/*/https://dev.twitter.com/overview/api/tweets>`_,
and `Entities
<https://web.archive.org/web/*/https://dev.twitter.com/overview/api/tweets>`_.

+------------------------------+-----------------------------------------------------+-------------------------------------------+
| Field	                       | Description                                         | Example                                   |
|                              |                                                     |                                           |
+==============================+=====================================================+===========================================+
| id                           | Twitter identifier for the tweet.                   | 114749583439036416                        |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| tweet_url                    | URL of the tweet on Twitter's website. If the tweet | https://twitter.com/NASA/                 |
|                              | is a retweet, the URL will be redirected to the     | status/394883921303056384                 |
|                              | original tweet.                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| created_at                   | Date and time the tweet was created, in Twitter's   | Fri Sep 16 17:16:47 +0000 2011            |
|                              | default format.                                     |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| parsed_created_at            | Date and time the tweet was created, in ISO 8601    | 2016-12-21T19:30:03+00:00                 |
|                              | format and UTC time zone.                           |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_screen_name             | The unique screen name of the account that authored | NASA                                      |
|                              | the tweet, at the time the tweet was posted. Screen |                                           |
|                              | names are generally displayed with a @ prefixed.    |                                           |
|                              | Note that an account’s screen name may change over  |                                           |
|                              | time.                                               |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| text                         | The text of the tweet. Newline characters are       | Observing Hurricane Raymond Lashing       |
|                              | replaced with a space.                              | Western Mexico: Low pressure System 96E   |
|                              |                                                     | developed quickly over the…               |
|                              |                                                     | http://t.co/YpffdKVrgm                    |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| tweet_type                   | original, reply, quote, or retweet                  | retweet                                   |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| coordinates                  | The geographic coordinates of the tweet. This is    | [-0.22012208, 51.59248806]                |
|                              | only enabled if geotagging is enabled on the        |                                           |
|                              | account. The value, if present, is of the form      |                                           |
|                              | [longitude, latitude].                              |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| hashtags                     | Hashtags from the tweet text, as a comma-separated  | Mars, askNASA                             |
|                              | list. Hashtags are generally displayed with a #     |                                           |
|                              | prefixed.                                           |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| media                        | URLs of media objects (photos, videos, GIFs) that   | https://twitter.com/NASA_Orion/status/    |
|                              | are attached to the tweet.                          | 394866827857100800/photo/1                |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| urls                         | URLs entered by user as part of tweet. Note that    | http://instagram.com/p/gA_zQ5IaCz/        |
|                              | URL may be a shortened URL, e.g. from bit.ly.       |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| favorite_count               | Number of times this tweet had been favorited/liked | 12                                        |
|                              | by other users at the time the tweet was collected. |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| in_reply_to_screen_name      | If tweet is a reply, the screen name of the author  | NASA                                      |
|                              | of the tweet that is being replied to.              |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| in_reply_to_status_id        | If tweet is a reply, the Twitter identifier of the  | 114749583439036416                        |
|                              | tweet that is being replied to.                     |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| in_reply_to_user_id          | If tweet is a reply, the Twitter identifier of the  | 481186914                                 |
|                              | author of the tweet that is being replied to.       |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| lang                         | Language of the tweet text, as determined by        | en                                        |
|                              | Twitter.                                            |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| place                        | The user or application-provided geographic         | Washington, DC                            |
|                              | location from which a tweet was posted.             |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| possibly_sensitive           | Indicates that URL contained in the tweet may       | true                                      |
|                              | reference sensitive content.                        |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| retweet_count                | Number of times the tweet had been retweeted at     | 25                                        |
|                              | the time the tweet was collected.                   |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| retweet_or_quote_id          | If tweet is a retweet or quote tweet, the Twitter   | 114749583439036416                        |
|                              | identifier of the source tweet.                     |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| retweet_or_quote_screen_name | If tweet is a retweet or quote tweet, the screen    | NASA                                      |
|                              | name of the author of the source tweet.             |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| retweet_or_quote_user_id     | If tweet is a retweet or quote tweet, the Twitter   | 481186914                                 |
|                              | identifier of the author or the source tweet.       |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| source                       | The application from which the tweet was posted.    | <a href=\"http://twitter.com/download/    |
|                              |                                                     | iphone\" rel=\"nofollow\">Twitter for     |
|                              |                                                     | iPhone</a>                                |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_id                      | Twitter identifier for the author of the tweet.     | 481186914                                 |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_created_at              | Date and time the tweet was created, in Twitter's   | Wed Mar 18 13:46:38 +0000 2009            |
|                              | default format.                                     |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_default_profile_image   | URL of the user's profile image.                    | https://pbs.twimg.com/profile_images/     |
|                              |                                                     | 942858479592554497/BbazLO9L_normal.jpg    |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_description             | The user-provided account description. Newline      | The safest spacecraft designed by NASA,   |
|                              | characters are replaced with a space.               | Orion will carry humans to the moon and   |
|                              |                                                     | beyond.                                   |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_favourites_count        | Number of tweets that have been favorited/liked     | 19                                        |
|                              | by the user.                                        |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_followers_count         | Number of followers this account had at the time    | 235                                       |
|                              | the tweet was collected.                            |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_friends_count           | Number of users this account was following at the   | 114                                       |
|                              | time the tweet was collected.                       |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_listed_count            | Number of public lists that this user is a member   | 3                                         |
|                              | of.                                                 |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_location                | The user's self-described location. Not necessarily | San Francisco, California                 |
|                              | an actual place.                                    |                                           |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_name                    | The user's self-provided name.                      | Orion Spacecraft                          |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_statuses_count          | Number of tweets that the user has posted.          | 2375                                      |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_time_zone               | The user-provided time zone. Currently deprecated.  | Eastern Time (US & Canada)                |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_urls                    | URLs entered by user as part of user's description. | http://www.Instagram.com/realDonaldTrump  |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+
| user_verified                | Indicates that the user's account is verified.      | true                                      |
|                              |                                                     |                                           |
+------------------------------+-----------------------------------------------------+-------------------------------------------+

-----------------
Tumblr Dictionary
-----------------

For more info about source tweet data, see the `Tumblr API documentation
<https://www.tumblr.com/docs/en/api/v2>`_, particularly `Posts
<https://www.tumblr.com/docs/en/api/v2#posts>`_.

Documentation about older archived posts is archived by the Wayback Machine for the
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
| tumblr_id               | Tumblr identifier for the blog post                 | 154774150409                                     |
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
| post_text               | Body of the post text, using html markup.           | See https://notepad.pw/w8133kzj                  |
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

Documentation about older archived posts is archived by the Wayback Machine `here
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


----------------
Weibo Dictionary
----------------

For more info about source tweet data, see the `Sina Weibo API
friends_timeline documentation
<http://open.weibo.com/wiki/2/statuses/friends_timeline>`_.

Documentation about older archived tweets is archived by the Wayback Machine `here
<https://web.archive.org/web/*/
http://open.weibo.com/wiki/2/statuses/friends_timeline>`_.

*Note that for privacy purposes, Weibo dictionary examples are not consistent.*

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+
| created_at              | Date and time the tweet was created, in             | 2016-12-21T19:30:03+00:00                        |
|                         | ISO 8601 format and UTC time zone.                  |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| weibo_id                | Sina Weibo identifier for the tweet.                | 4060309792585658                                 |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| screen_name             | The unique screen name of the account that          |  下厨房                                          |
|                         | authored the weibo, at the time the weibo was       |                                                  |
|                         | posted.                                             |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| followers_count         | Number of followers this account had at the time    | 3655329                                          |
|                         | the weibo was harvested.                            |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| friends_count           | Number of users this account was following at the   | 2691                                             |
|                         | time the weibo was harvested.                       |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| reposts_count           | Number of times this weibo had been reposted at     | 68                                               |
|                         | the time the weibo was harvested.                   |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| topics                  | Topics (similar to hashtags) from the weibo text    |  魅族三分时刻                                    |
|                         | as a comma-separated list.                          |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| in_reply_to_screen_name | If the weibo is a reply, the screen name of         |  下厨房                                          |
|                         | the original weibo's author.                        |                                                  |
|                         | (This is not yet supported by Sina Weibo.)          |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| weibo_url               | URL of the weibo. If the tweet is a retweet made    | http://m.weibo.cn/1618051664/4060300716095462    |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| text                    | The text of the weibo.                              |  马住！                                          |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url1                    | First URL in text of weibo, as shortened by         | http://t.cn/RM2xyx6                              |
|                         | Sina Weibo.                                         |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url2                    | Second URL in text of weibo, as shortened by        | http://t.cn/Rc52gDY                              |
|                         | Sina Weibo.                                         |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| retweeted_text          | Text of original weibo when the collected weibo     |  马住！                                          |
|                         | is a repost.                                        |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| retweeted_url1          | First URL in text of original weibo, as shortened   | http://t.cn/RVR4cAQ                              |
|                         | by Sina Weibo.                                      |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| retweeted_url2          | Second URL in text of original weibo, as shortened  | http://t.cn/RMAJISP                              |
|                         | by Sina Weibo.                                      |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
