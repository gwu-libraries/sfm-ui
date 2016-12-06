===============================================
 Data Dictionary for Twitter CSV/Excel Exports
===============================================

Social Feed Manager captures entire tweets, with all their data. To download selected, processed fields for each tweet in a user timeline, use the csv export option, available on each user page. 

For more info about source tweet data, see the `Twitter API documentation <https://dev.twitter.com/docs>`_, including `Tweets <https://dev.twitter.com/docs/platform-objects/tweets>`_ and `Entities <https://dev.twitter.com/docs/platform-objects/entities>`_.

+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| Field	                  | Description                                         | Example                                          |
|                         |                                                     |                                                  |
+=========================+=====================================================+==================================================+ 
| created_at              | UTC time when the tweet was created	                | 2013-10-28T17:52:53Z                             | 
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| twitter_id              | Twitter identifier for the tweet	                | 114749583439036416                               |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| screen_name             | The screen name of the account that authored the    | NASA                                             |
|                         | tweet. Screen_names are unique                      |                                                  |
|                         | but subject to change.                              |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| followers_count         | Number of followers this account had at the time    | 235                                              |
|                         | the tweet was harvested                             |                                                  | 
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| friends_count           | Number of users this account wass following at the  | 114                                              |
|                         | time the tweet was harvested                        |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| retweet_count           | Number of times the tweet has been retweeted at the | 25                                               | 
|                         | time the tweet was harvested.                       |                                                  | 
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| hashtags                | Hashtags which have been parsed out of the tweet    | Mars, askNASA                                    |
|                         | text, as a comma-separated list                     |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| in_reply_to_screen_name | If the tweet is a reply, the screen name of         | wiredscience                                     |
|                         | the original tweet's author                         |                                                  | 
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| twitter_url             | URL of the tweet. If the tweet is a retweet made    | http://twitter.com/NASA/status/394883921303056384|
|                         | using the Twitter retweet feature, the URL will     | retweet redirecting to original tweet:           | 
|                         | redirect to the original tweet                      | http://twitter.com/NASA/status/394875351894994944|
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| coordinates             | The geographic coordinates of the tweet.  This is   | [-0.22012208, 51.59248806]                       | 
|                         | only enabled if geotagging is enabled on the        |                                                  |
|                         | account.  The value, if present, is of the form     |                                                  |
|                         | [longitude, latitude]                               |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| text                    | The UTF-8 text of the tweet                         | Observing Hurricane Raymond Lashing Western      | 
|                         |                                                     | Mexico: Low pressure System 96E developed quickly|
|                         |                                                     | over the... http://t.co/YpffdKVrgm               |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| mentions                | Other Twitter users mentioned in the text of the    | @NASA_Airborne, @NASA_Ice                        | 
|                         | tweet, separated by comma and space.                |                                                  | 
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| is_retweet              | Tweet is a retweet of another tweet, according to   | Yes                                              | 
|                         | the tweet's metadata                                |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| is_quote                | Tweet is a quote of another tweet, according to     | No                                               | 
|                         | the tweet's metadata                                |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url1                    | First URL in text of tweet, as shortened by Twitter | http://t.co/WGJ9VmoKME                           |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url1_expanded           | Expanded version of URL; URL entered by user and    | http://instagram.com/p/gA_zQ5IaCz/               |
|                         | displayed in Twitter. May itself be a user-shortened|                                                  |
|                         | URL, e.g. from bit.ly. Further expansion available  |                                                  |
|                         | in sfm web interface, not in csv export.            |                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url2                    | Second URL in text of tweet, as shortened by Twitter|                                                  |
|                         |                                                     |                                                  |
+-------------------------+-----------------------------------------------------+--------------------------------------------------+
| url2_expanded           | Expanded version of URL; URL entered by user and    |                                                  |
|                         | displayed in Twitter. May itself be a user-shortened|                                                  |
|                         | URL, e.g. from bit.ly. Further expansion available  |                                                  |
|                         | in SFM web interface, not in csv export             |                                                  |
|                         |                                                     |                                                  | 
+-------------------------+-----------------------------------------------------+--------------------------------------------------+ 
