===============================================
 Data Dictionary for Twitter CSV/Excel Exports
===============================================

Social Feed Manager captures entire tweets, with all their data. To download
selected, processed fields for each tweet in a user timeline, use the csv export
 option, available on each user page.

------------------
Twitter Dictionary
------------------

For more info about source tweet data, see the `Twitter API documentation
<https://dev.twitter.com/docs>`_, including `Tweets
<https://dev.twitter.com/docs/platform-objects/tweets>`_ and `Entities
<https://dev.twitter.com/docs/platform-objects/entities>`_.

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
| post_text               | Body of the post text, using html markup.           | See https://notepad.pw/w8133kzj                  |
|                         |                                                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tags                    | Hashtags from the post                              | nasa, space, solarsystem,                        |
|                         | as a comma-separated list.                          | chiefscientist, scientist                        |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tumblr_url              | Full url location of the post.                      | http://nasa.tumblr.com/post/154774150409/        |
|                         |                                                     | 10-questions-for-our-chief-scientist             |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| tumblr_short_url        | Short url of the post.                              | https://tmblr.co/Zz_Uqj2G9GXq9                   |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
