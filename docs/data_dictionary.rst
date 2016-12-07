===============================================
 Data Dictionary for Twitter CSV/Excel Exports
===============================================

Social Feed Manager captures entire tweets, with all their data. To download selected, processed fields for each tweet in a user timeline, use the csv export option, available on each user page. 

This data dictionary currently only describes SFM's Twitter exports.  Tumblr, Flickr,
and Weibo exports contain fewer columns that are generally self-explanatory and/or are
similar to the columns described here in the Twitter export.

For more info about source tweet data, see the `Twitter API documentation <https://dev.twitter.com/docs>`_, including `Tweets <https://dev.twitter.com/docs/platform-objects/tweets>`_ and `Entities <https://dev.twitter.com/docs/platform-objects/entities>`_.

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+ 
| created_at              | Date and time the tweet was created, in             | 12/1/2016  1:22:35 AM                            | 
|                         | Excel-friendly format.                              |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| twitter_id              | Twitter identifier for the tweet.                   | 114749583439036416                               |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| screen_name             | The screen name of the account that authored the    | NASA                                             |
|                         | tweet, at the time the tweet was posted.            |                                                  |
|                         | Note that an account's screen name may change over  |                                                  |
|                         | time.                                               |                                                  |
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
| favorites_count         | Number of times this tweet had been favorited by    | 12                                               |
|                         | other users at the time the tweet was harvested.    |                                                  |
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
| url2                    | Second URL in text of tweet, as shortened           |                                                  |
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
