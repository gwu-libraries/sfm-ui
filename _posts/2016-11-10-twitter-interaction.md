---
layout: article
permalink: /posts/2016-11-10-twitter-interaction
title: "On retweets, replies, quotes & favorites:  A guide for researchers"
author: justin_littman 
excerpt: "A Jupyter notebook that explores the affordances of the Twitter API for retweets, replies, quotes, and favorites."
---

# On retweets, replies, quotes & favorites:  A guide for researchers

This notebook explores the affordances of the Twitter API for retweets, replies, quotes, and favorites. It is motivated by questions from several George Washington University researchers who are interested in using [Social Feed Manager](http://go.gwu.edu/sfm) to collect datasets for studying dialogues and interaction on Twitter.

We will not discuss affordances of the Twitter API that are perspectival, that is, depend on the Twitter account that is used to access the API. So, for example, we will not consider [GET statuses/retweets_of_me](https://dev.twitter.com/rest/reference/get/statuses/retweets_of_me).

The source of this notebook is [available](https://github.com/gwu-libraries/notebooks/tree/master/20161110-twitter-interaction).

## Setup

Before proceeding, we will install [Twarc](https://github.com/DocNow/twarc). Twarc is a Twitter client. It is generally used from the commandline,
but we will use it as a library.

This assumes that you have run Twarc locally and already have credentials stored in ~/.twarc.

As you are reading this, feel free to skip any of the sections of code.


```python
# This installs Twarc
# !pip install twarc
# This is temporary until https://github.com/DocNow/twarc/pull/118 is merged.
!pip install git+https://github.com/justinlittman/twarc.git@retweets#egg=twarc
# This imports some classes and functions that will be used later in this notebook.
from twarc import Twarc, load_config, default_config_filename
import json
import codecs

# This creates an instance of Twarc.
credentials = load_config(default_config_filename(), 'main')
t = Twarc(consumer_key=credentials['consumer_key'],
          consumer_secret=credentials['consumer_secret'],
          access_token=credentials['access_token'],
          access_token_secret=credentials['access_token_secret'])

# Create a summary of a tweet, only showing relevant fields.
def summarize(tweet, extra_fields = None):
    new_tweet = {}
    for field, value in tweet.items():
        if field in ["text", "id_str", "screen_name", "retweet_count", "favorite_count", "in_reply_to_status_id_str", "in_reply_to_screen_name", "in_reply_to_user_id_str"] and value is not None:
            new_tweet[field] = value
        elif extra_fields and field in extra_fields:
            new_tweet[field] = value
        elif field in ["retweeted_status", "quoted_status", "user"]:
            new_tweet[field] = summarize(value)
    return new_tweet

# Print out a tweet, with optional colorizing of selected fields.
def dump(tweet, colorize_fields=None, summarize_tweet=True):
    colorize_field_strings = []
    for line in json.dumps(summarize(tweet) if summarize_tweet else tweet, indent=4, sort_keys=True).splitlines():
        colorize = False
        for colorize_field in colorize_fields or []:
            if "\"{}\":".format(colorize_field) in line:       
                print "\x1b" + line + "\x1b"
                break
        else:
            print line
```

    Requirement already satisfied (use --upgrade to upgrade): twarc from git+https://github.com/justinlittman/twarc.git@retweets#egg=twarc in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages
    Requirement already satisfied (use --upgrade to upgrade): pytest in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from twarc)
    Requirement already satisfied (use --upgrade to upgrade): python-dateutil in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from twarc)
    Requirement already satisfied (use --upgrade to upgrade): requests-oauthlib in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from twarc)
    Requirement already satisfied (use --upgrade to upgrade): unicodecsv in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from twarc)
    Requirement already satisfied (use --upgrade to upgrade): py>=1.4.29 in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from pytest->twarc)
    Requirement already satisfied (use --upgrade to upgrade): six>=1.5 in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from python-dateutil->twarc)
    Requirement already satisfied (use --upgrade to upgrade): requests>=2.0.0 in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from requests-oauthlib->twarc)
    Requirement already satisfied (use --upgrade to upgrade): oauthlib>=0.6.2 in /Users/justinlittman/JUPYTER/lib/python2.7/site-packages (from requests-oauthlib->twarc)
    [33mYou are using pip version 7.1.2, however version 9.0.1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.


## Tweet types

### A tweet

Before examining the specific types of tweets that we're interested in, we're going to look at a plain-old tweet.

Here's my first tweet.


```python
%%html
<!-- This renders embeds a tweet in the notebook. -->
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">First day at Gelman Library. First tweet. <a href="http://t.co/Gz5ybAD6os">pic.twitter.com/Gz5ybAD6os</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/503873833213104128">August 25, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<!-- This renders embeds a tweet in the notebook. -->
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">First day at Gelman Library. First tweet. <a href="http://t.co/Gz5ybAD6os">pic.twitter.com/Gz5ybAD6os</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/503873833213104128">August 25, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>


Tweets retrieved from the Twitter API are in [JSON](http://json.org/), a simple structured text format. Below I will provide the entire tweet; in the rest of this notebook I will only provide a subset of the tweet containing the relevant fields. Twitter provides [documentation on the complete set of fields in a tweet](https://dev.twitter.com/overview/api/tweets).



```python
# Retrieve a single tweet from the Twitter API
tweet = list(t.hydrate(['503873833213104128']))[0]
# Pretty-print the tweet
dump(tweet, summarize_tweet=False)
```

    {
        "contributors": null, 
        "coordinates": null, 
        "created_at": "Mon Aug 25 11:57:38 +0000 2014", 
        "entities": {
            "hashtags": [], 
            "media": [
                {
                    "display_url": "pic.twitter.com/Gz5ybAD6os", 
                    "expanded_url": "https://twitter.com/justin_littman/status/503873833213104128/photo/1", 
                    "id": 503873819560665088, 
                    "id_str": "503873819560665088", 
                    "indices": [
                        42, 
                        64
                    ], 
                    "media_url": "http://pbs.twimg.com/media/Bv4ekbqIYAAcmXY.jpg", 
                    "media_url_https": "https://pbs.twimg.com/media/Bv4ekbqIYAAcmXY.jpg", 
                    "sizes": {
                        "large": {
                            "h": 576, 
                            "resize": "fit", 
                            "w": 1024
                        }, 
                        "medium": {
                            "h": 338, 
                            "resize": "fit", 
                            "w": 600
                        }, 
                        "small": {
                            "h": 191, 
                            "resize": "fit", 
                            "w": 340
                        }, 
                        "thumb": {
                            "h": 150, 
                            "resize": "crop", 
                            "w": 150
                        }
                    }, 
                    "type": "photo", 
                    "url": "http://t.co/Gz5ybAD6os"
                }
            ], 
            "symbols": [], 
            "urls": [], 
            "user_mentions": []
        }, 
        "extended_entities": {
            "media": [
                {
                    "display_url": "pic.twitter.com/Gz5ybAD6os", 
                    "expanded_url": "https://twitter.com/justin_littman/status/503873833213104128/photo/1", 
                    "id": 503873819560665088, 
                    "id_str": "503873819560665088", 
                    "indices": [
                        42, 
                        64
                    ], 
                    "media_url": "http://pbs.twimg.com/media/Bv4ekbqIYAAcmXY.jpg", 
                    "media_url_https": "https://pbs.twimg.com/media/Bv4ekbqIYAAcmXY.jpg", 
                    "sizes": {
                        "large": {
                            "h": 576, 
                            "resize": "fit", 
                            "w": 1024
                        }, 
                        "medium": {
                            "h": 338, 
                            "resize": "fit", 
                            "w": 600
                        }, 
                        "small": {
                            "h": 191, 
                            "resize": "fit", 
                            "w": 340
                        }, 
                        "thumb": {
                            "h": 150, 
                            "resize": "crop", 
                            "w": 150
                        }
                    }, 
                    "type": "photo", 
                    "url": "http://t.co/Gz5ybAD6os"
                }
            ]
        }, 
        "favorite_count": 4, 
        "favorited": false, 
        "geo": null, 
        "id": 503873833213104128, 
        "id_str": "503873833213104128", 
        "in_reply_to_screen_name": null, 
        "in_reply_to_status_id": null, 
        "in_reply_to_status_id_str": null, 
        "in_reply_to_user_id": null, 
        "in_reply_to_user_id_str": null, 
        "is_quote_status": false, 
        "lang": "en", 
        "place": null, 
        "possibly_sensitive": false, 
        "retweet_count": 0, 
        "retweeted": false, 
        "source": "<a href=\"http://twitter.com/download/android\" rel=\"nofollow\">Twitter for Android</a>", 
        "text": "First day at Gelman Library. First tweet. http://t.co/Gz5ybAD6os", 
        "truncated": false, 
        "user": {
            "contributors_enabled": false, 
            "created_at": "Thu Feb 02 12:19:18 +0000 2012", 
            "default_profile": true, 
            "default_profile_image": false, 
            "description": "", 
            "entities": {
                "description": {
                    "urls": []
                }
            }, 
            "favourites_count": 206, 
            "follow_request_sent": false, 
            "followers_count": 174, 
            "following": false, 
            "friends_count": 78, 
            "geo_enabled": true, 
            "has_extended_profile": false, 
            "id": 481186914, 
            "id_str": "481186914", 
            "is_translation_enabled": false, 
            "is_translator": false, 
            "lang": "en", 
            "listed_count": 12, 
            "location": "", 
            "name": "Justin Littman", 
            "notifications": false, 
            "profile_background_color": "C0DEED", 
            "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", 
            "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", 
            "profile_background_tile": false, 
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/481186914/1460820528", 
            "profile_image_url": "http://pbs.twimg.com/profile_images/496478011533713408/GjecBUNj_normal.jpeg", 
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/496478011533713408/GjecBUNj_normal.jpeg", 
            "profile_link_color": "1DA1F2", 
            "profile_sidebar_border_color": "C0DEED", 
            "profile_sidebar_fill_color": "DDEEF6", 
            "profile_text_color": "333333", 
            "profile_use_background_image": true, 
            "protected": false, 
            "screen_name": "justin_littman", 
            "statuses_count": 481, 
            "time_zone": "Eastern Time (US & Canada)", 
            "translator_type": "none", 
            "url": null, 
            "utc_offset": -18000, 
            "verified": false
        }
    }


Here's what the summary of that same tweet:


```python
dump(tweet)
```

    {
        "favorite_count": 4, 
        "id_str": "503873833213104128", 
        "retweet_count": 0, 
        "text": "First day at Gelman Library. First tweet. http://t.co/Gz5ybAD6os", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


### A tweet that has been retweeted

First, we want to look at a tweet that has been retweeted.  I'll choose this one from my user timeline:


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">.<a href="https://twitter.com/DameWendyDBE">@DameWendyDBE</a>: Invest in data science training for librarians.  In future, libraries will be data warehouses. <a href="https://twitter.com/hashtag/SaveTheWeb?src=hash">#SaveTheWeb</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/743520583518920704">June 16, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">.<a href="https://twitter.com/DameWendyDBE">@DameWendyDBE</a>: Invest in data science training for librarians.  In future, libraries will be data warehouses. <a href="https://twitter.com/hashtag/SaveTheWeb?src=hash">#SaveTheWeb</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/743520583518920704">June 16, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>


Let's retrieve the JSON for this tweet from the Twitter API.


```python
tweet = list(t.hydrate(['743520583518920704']))[0]
dump(tweet, colorize_fields=['retweet_count'])
```

    {
        "favorite_count": 12, 
        "id_str": "743520583518920704", 
        "retweet_count": 19, 
        "text": ".@DameWendyDBE: Invest in data science training for librarians.  In future, libraries will be data warehouses. #SaveTheWeb", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


The relevant field is *retweet_count*. This field provides the number of times this tweet was retweeted. Note that this number may vary over time, as additional people retweet the tweet.

### A tweet that is a retweet
Second, we want to look at a tweet that is a retweet. I'll also choose this one from my user timeline:


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Reproducible Research: Citing your execution env using <a href="https://twitter.com/docker">@Docker</a> and a DOI: <a href="https://t.co/S4DChzE9Au">https://t.co/S4DChzE9Au</a> via <a href="https://twitter.com/SoftwareSaved">@SoftwareSaved</a> <a href="https://t.co/SPMcKa35J4">pic.twitter.com/SPMcKa35J4</a></p>&mdash; Docker (@docker) <a href="https://twitter.com/docker/status/720856949407940608">April 15, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Reproducible Research: Citing your execution env using <a href="https://twitter.com/docker">@Docker</a> and a DOI: <a href="https://t.co/S4DChzE9Au">https://t.co/S4DChzE9Au</a> via <a href="https://twitter.com/SoftwareSaved">@SoftwareSaved</a> <a href="https://t.co/SPMcKa35J4">pic.twitter.com/SPMcKa35J4</a></p>&mdash; Docker (@docker) <a href="https://twitter.com/docker/status/720856949407940608">April 15, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>


Here is the JSON from the Twitter API.


```python
tweet = list(t.hydrate(['724575206937899008']))[0]
dump(tweet, colorize_fields=['retweeted_status', 'retweet_count'])
```

    {
        "favorite_count": 0, 
        "id_str": "724575206937899008", 
        "retweet_count": 42, 
        "retweeted_status": {
            "favorite_count": 39, 
            "id_str": "720856949407940608", 
            "retweet_count": 42, 
            "text": "Reproducible Research: Citing your execution env using @Docker and a DOI: https://t.co/S4DChzE9Au via @SoftwareSaved https://t.co/SPMcKa35J4", 
            "user": {
                "id_str": "1138959692", 
                "screen_name": "docker"
            }
        }, 
        "text": "RT @docker: Reproducible Research: Citing your execution env using @Docker and a DOI: https://t.co/S4DChzE9Au via @SoftwareSaved https://t.\u2026", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


Two fields are significant. First, the *retweeted_status* contains the source tweet (i.e., the tweet that was retweeted). The present or absence of this field can be used to identify tweets that are retweets. Second, the *retweet_count* is the count of the retweets of the source tweet, not this tweet.

### A tweet that is a retweet of a retweet
As a corollary to our look at a retweet, let's look at a tweet that is a retweet of a retweet. (I'll refer to this as a second order retweet.) Here's a tweet that I retweeted from my @jlittman_dev account that was a retweet from my @justin_littman account of a source tweet from @SocialFeedMgr.


```python
tweet = list(t.hydrate(['794490469627686913']))[0]
dump(tweet, colorize_fields=['retweet_count', 'retweeted_status'])
```

    {
        "favorite_count": 0, 
        "id_str": "794490469627686913", 
        "retweet_count": 8, 
        "retweeted_status": {
            "favorite_count": 4, 
            "id_str": "793896478037114880", 
            "retweet_count": 8, 
            "text": "Software doesn't live forever. How to get collections OUT of Social Feed Manager, a new blog post by @justin_littman https://t.co/CagQvSF7pJ", 
            "user": {
                "id_str": "713856598079315968", 
                "screen_name": "SocialFeedMgr"
            }
        }, 
        "text": "RT @SocialFeedMgr: Software doesn't live forever. How to get collections OUT of Social Feed Manager, a new blog post by @justin_littman htt\u2026", 
        "user": {
            "id_str": "2875189485", 
            "screen_name": "jlittman_dev"
        }
    }


The second order tweet is treated as if it is a retweet of the source tweet. The *retweet_count* of the source tweet is incremented and the *retweeted_status* that appears in the second order tweet is the source tweet. There is no indication that this is a retweet of a retweet. Thus, in reconstructing interaction, you can't determine from who a user discovered a tweet that she later retweeted.

### A tweet that has been quoted
Third, we want to consider a tweet that has been quoted. A quote tweet is a retweet that contains some additional text.

To test this, I [quoted my first tweet](https://twitter.com/jlittman_dev/status/727930772691292161) from a different twitter account (@jlittman_dev).


```python
tweet = list(t.hydrate(['503873833213104128']))[0]
dump(summarize(tweet))
```

    {
        "favorite_count": 4, 
        "id_str": "503873833213104128", 
        "retweet_count": 0, 
        "text": "First day at Gelman Library. First tweet. http://t.co/Gz5ybAD6os", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


There is nothing in the tweet to indicate that it has been quoted. This is similar to what you find on Twitter website: if you look at the [full rendering of this tweet](https://twitter.com/justin_littman/status/503873833213104128), there is no indication that it was quoted.

Quotes don't count as a retweet, as the *retweet_count* on the source tweet is 0.


### A tweet that is a quote
Fourth, we want to look at a tweet that is a quote.


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Let us know what can add to <a href="https://twitter.com/SocialFeedMgr">@SocialFeedMgr</a> docs to take the &quot;crash&quot; out of &quot;crash course&quot; <a href="https://twitter.com/ianmilligan1">@ianmilligan1</a>. And all other feedback welcome. <a href="https://t.co/BbjOLSvdCm">https://t.co/BbjOLSvdCm</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/794162076717613056">November 3, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Let us know what can add to <a href="https://twitter.com/SocialFeedMgr">@SocialFeedMgr</a> docs to take the &quot;crash&quot; out of &quot;crash course&quot; <a href="https://twitter.com/ianmilligan1">@ianmilligan1</a>. And all other feedback welcome. <a href="https://t.co/BbjOLSvdCm">https://t.co/BbjOLSvdCm</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/794162076717613056">November 3, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>



```python
tweet = list(t.hydrate(['794162076717613056']))[0]
dump(summarize(tweet, extra_fields=['quoted_status_id', 'quoted_status_id_str']), colorize_fields=['quoted_status', 'quoted_status_id', 'quoted_status_id_str'], summarize_tweet=False)
```

    {
        "favorite_count": 4, 
        "id_str": "794162076717613056", 
        "quoted_status": {
            "favorite_count": 11, 
            "id_str": "794000147130687488", 
            "retweet_count": 1, 
            "text": "Well, it was a crash course in some AWS things and Docker, but got Social Feed Manager up and running on Amazon! https://t.co/empcsmLSSt", 
            "user": {
                "id_str": "255681367", 
                "screen_name": "ianmilligan1"
            }
        }, 
        "quoted_status_id": 794000147130687488, 
        "quoted_status_id_str": "794000147130687488", 
        "retweet_count": 1, 
        "text": "Let us know what can add to @SocialFeedMgr docs to take the \"crash\" out of \"crash course\" @ianmilligan1. And all ot\u2026 https://t.co/eA0qLGu8ht", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


The relevant field in this quote tweet is *quoted_status*, which contains the source tweet. *quoted_status_id* and *quoted_status_id_str* are the tweet id of the source tweet, which is redundant of the tweet id contained in *quoted_status*.

### A tweet that has been replied
Fifth, we want to look at a tweet to which another user has replied. Here's a tweet that I posted, to which @jefferson_bail replied:


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Yesterday I learned about the <a href="https://twitter.com/jefferson_bail">@jefferson_bail</a> test for projects: Is it sufficiently &quot;do-goody and feel-goody&quot;?</p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/789411809807572992">October 21, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Yesterday I learned about the <a href="https://twitter.com/jefferson_bail">@jefferson_bail</a> test for projects: Is it sufficiently &quot;do-goody and feel-goody&quot;?</p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/789411809807572992">October 21, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>


There is nothing to indicate that this tweet has a reply.

### A tweet that is a reply
Sixth, we want to look at a tweet that is a reply to another tweet. Here's @jefferson_bail's response to my tweet:


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/justin_littman">@justin_littman</a> Ha! I don&#39;t even remember what I was talking about. I believe that was my fifth meeting in a row starting at 7am, so...</p>&mdash; Jefferson Bailey (@jefferson_bail) <a href="https://twitter.com/jefferson_bail/status/789486128189444096">October 21, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/justin_littman">@justin_littman</a> Ha! I don&#39;t even remember what I was talking about. I believe that was my fifth meeting in a row starting at 7am, so...</p>&mdash; Jefferson Bailey (@jefferson_bail) <a href="https://twitter.com/jefferson_bail/status/789486128189444096">October 21, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>



```python
tweet = list(t.hydrate(['789486128189444096']))[0]
dump(summarize(tweet, extra_fields=['in_reply_to_status_id_str', 'in_reply_to_user_id']), colorize_fields=['in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'in_reply_to_user_id_str'], summarize_tweet=False)
```

    {
        "favorite_count": 0, 
        "id_str": "789486128189444096", 
        "in_reply_to_screen_name": "justin_littman", 
        "in_reply_to_status_id_str": "789411809807572992", 
        "in_reply_to_user_id": 481186914, 
        "in_reply_to_user_id_str": "481186914", 
        "retweet_count": 0, 
        "text": "@justin_littman Ha! I don't even remember what I was talking about. I believe that was my fifth meeting in a row starting at 7am, so...", 
        "user": {
            "id_str": "346054122", 
            "screen_name": "jefferson_bail"
        }
    }


The relevant fields in a reply tweet are *in_reply_to_status_id*, *in_reply_to_status_id_str*, *in_reply_to_screen_name*, *in_reply_to_user_id*, *in_reply_to_user_id_str*. The names of each of these fields reasonably describe their contents. The most significant of these is *in_reply_to_status_id*, which supports finding the tweet to which the reply tweet is a reply.

Thus, based on the metadata that is provided for a tweet, a chain of replies can be followed backwards from the reply tweet to the replied to tweet, but not vice versa, i.e., from the replied to tweet to the reply tweet.

### A tweet that is favorited
Here is the most favorited tweet from my user timeline:


```python
%%html
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Slides from my <a href="https://twitter.com/hashtag/iipcWAC16?src=hash">#iipcWAC16</a> presentation on aligning social media archiving and web archiving: <a href="https://t.co/Rj8LEbBOp8">https://t.co/Rj8LEbBOp8</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/720621197550071808">April 14, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
```


<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Slides from my <a href="https://twitter.com/hashtag/iipcWAC16?src=hash">#iipcWAC16</a> presentation on aligning social media archiving and web archiving: <a href="https://t.co/Rj8LEbBOp8">https://t.co/Rj8LEbBOp8</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/720621197550071808">April 14, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>



```python
tweet = list(t.hydrate(['720621197550071808']))[0]
dump(tweet, colorize_fields=['favorite_count'])
```

    {
        "favorite_count": 14, 
        "id_str": "720621197550071808", 
        "retweet_count": 13, 
        "text": "Slides from my #iipcWAC16 presentation on aligning social media archiving and web archiving: https://t.co/Rj8LEbBOp8", 
        "user": {
            "id_str": "481186914", 
            "screen_name": "justin_littman"
        }
    }


The *favorite_count* provides the number of times the tweet has been favorited.

In the case of a retweet, *favorite_count* is the favorite count of the source tweet. (This is similar to *retweet_count*.)

## The Twitter API
In this section, we look at the various methods in Twitter's APIs that are relevant to retweets, replies, quotes, and favorites.

### GET statuses/show/:id and GET statuses/lookup
[GET statuses/show/:id](https://dev.twitter.com/rest/reference/get/statuses/show/id) is used to retrieve a single tweet by tweet id. [GET statuses/lookup](https://dev.twitter.com/rest/reference/get/statuses/lookup) is used to retrieve multiple tweets by tweet ids.

In the above examples, GET statuses/lookup using only a single tweet id was used to retrieve the tweets.

### GET statuses/user_timeline
[GET statuses/user_timeline](https://dev.twitter.com/rest/reference/get/statuses/user_timeline) retrieves a user timeline given a screen name or user id. This is one of the primary methods for collecting social media data.

While GET statuses/user_timeline supports getting tweets from the past, it is limited to the last 3,200 tweets.

To test this, we will retrieve the user timeline of @jlittman_dev and looks for retweets, quotes, replies, favorited tweets, and retweeted tweets.


```python
found_retweet = False
found_quote = False
found_reply = False
found_favorited = False
found_retweeted = False
for tweet in t.timeline(screen_name='jlittman_dev'):
    if 'retweeted_status' in tweet:
        print "{} is a retweet.".format(tweet['id_str'])
        found_retweet = True
    if 'quoted_status' in tweet:
        print "{} is a quote.".format(tweet['id_str'])
        found_quote = True
    if tweet['in_reply_to_status_id']:
        print "{} is a reply to {} by {}".format(tweet['id_str'], tweet['in_reply_to_status_id_str'], tweet['in_reply_to_screen_name'])
        found_reply = True
    if tweet['retweet_count'] > 0:
        print "{} has been retweeted {} times.".format(tweet['id_str'], tweet['retweet_count'])
        found_retweeted = True
    if tweet['favorite_count'] > 0:
        print "{} has been favorited {} times.".format(tweet['id_str'], tweet['favorite_count'])
        found_favorited = True
print "Found retweet: {}".format(found_retweet)
print "Found quote: {}".format(found_quote)
print "Found reply: {}".format(found_reply)
print "Found favorited: {}".format(found_favorited)
print "Found retweeted: {}".format(found_retweeted)
```

    795976980416098304 is a reply to 795976763809693696 by jlittman_dev2
    795975981370576896 is a reply to 795975688981544960 by jlittman_dev2
    795974800028082176 is a quote.
    795972820413140992 has been retweeted 2 times.
    795972820413140992 has been favorited 1 times.
    794629362972815361 is a reply to 793892668606676994 by justin_littman
    794490469627686913 is a retweet.
    794490469627686913 has been retweeted 8 times.
    727933040803057667 is a retweet.
    727933040803057667 has been retweeted 2 times.
    727930772691292161 is a quote.
    577868461440823296 has been favorited 1 times.
    Found retweet: True
    Found quote: True
    Found reply: True
    Found favorited: True
    Found retweeted: True


This demonstrates that the following are available from the user timeline:
* retweets by the user
* quotes by the user
* replies by the user
* favorited tweets
* retweeted tweets

Other than the counts for favorited tweets and retweeted tweets, it does not include the tweets of other users such as quotes of this user or replies to tweets of this user.

### GET statuses/retweets/:id

[GET statuses/retweets/:id](https://dev.twitter.com/rest/reference/get/statuses/retweets/id) returns the most recent retweets for a tweet. Only the most recent 100 retweets are available.

To test this, let's compare the *retweet_count* against the number of tweets returned by GET statuses/retweets/:id for that tweet.


```python
tweet = list(t.hydrate(['743520583518920704']))[0]
print "The retweet count is {}".format(tweet['retweet_count'])
retweets = t.retweets('743520583518920704')
print "Retrieved {} retweets".format(len(list(retweets)))
```

    The retweet count is 19
    Retrieved 19 retweets


### GET statuses/retweeters/ids

[GET statuses/retweeters/ids](https://dev.twitter.com/rest/reference/get/statuses/retweeters/ids) retrieves the user ids that retweeted a tweet.

### GET search/tweets
[GET search/tweets](https://dev.twitter.com/rest/reference/get/search/tweets) (also known as the [Twitter Search API](https://dev.twitter.com/rest/public/search)) allows searching "against a sampling of recent Tweets published in the past 7 days."

Some of the query parameters that are relevant to retweets, quotes, and replies are:

* *from* for tweets posted by a user, e.g., from:justin_littman
* *to* for tweets that are a reply to the user, e.g., to:justin_littman
* *@* for tweets mentioning that screen name, e.g., @justin_littman

Because the Search API is time limited and an unknown size sample, it will not be further explored in this notebook.

### POST statuses/filter
[POST statuses/filter](https://dev.twitter.com/streaming/reference/post/statuses/filter) allows filtering of the stream of tweets on the Twitter platform by keywords ([track](https://dev.twitter.com/streaming/overview/request-parameters#track)), users ([follow](https://dev.twitter.com/streaming/overview/request-parameters#follow)), and geolocation ([location](https://dev.twitter.com/streaming/overview/request-parameters#location)).

POST statuses/filter only allows collecting tweets moving forward; it cannot be used to retrieve past tweets.

#### Follow parameter
For this test, I will use the follow parameter to determine what is captured when following a user. Note that the follow parameter takes a list of user ids. User ids do not change (unlike screen names).

Because this test requires creating tweets from multiple accounts and recording the filter stream, it will not be performed live in this notebook. Rather, I used Twarc to record the filter stream of @jlittman_dev (user id 2875189485):

    twarc.py --follow 2875189485 > follow.json
    
I then performed the following actions on the Twitter website:

1. @jlittman_dev: Posted [a tweet](https://twitter.com/jlittman_dev/status/795972820413140992).
2. @jlittman_dev2: Retweeted @jlittman_dev's tweet from step 1.
3. @jlittman_dev2: Posted [a tweet](https://twitter.com/jlittman_dev2/status/795974171754897409).
4. @jlittman_dev: [Quotes @jlittman_dev's tweet](https://twitter.com/jlittman_dev/status/795974800028082176) from step 3.
5. @jlittman_dev2: [Quoted](https://twitter.com/jlittman_dev2/status/795975523625299968) [a tweet by @jlittman_dev](https://twitter.com/jlittman_dev/status/795972351250796545).
6. @jlittman_dev2: [Replied](https://twitter.com/jlittman_dev2/status/795975688981544960) to [a tweet by @jlittman_dev](https://twitter.com/jlittman_dev/status/795972351250796545).
7. @jlittman_dev: [Replied to the reply](https://twitter.com/jlittman_dev/status/795974800028082176) of @jlittman_dev2 from step 6.
8. @jlittman_dev: [Replied](https://twitter.com/jlittman_dev/status/795976980416098304) to [a tweet by @jlittman_dev2](https://twitter.com/jlittman_dev2/status/795976763809693696).

We will now look at the tweets that were captured by the filter stream.

The first tweet is the tweet posted by @jlittman_dev in step 1. Thus, tweets by the followed user are captured.


```python
# Load the tweets
with codecs.open('./follow.json', 'r') as f:
    lines = f.readlines()
# Print the number of tweets
print len(lines)
# Print the first tweet
tweet1 = json.loads(lines[0])
dump(tweet1)
```

    6
    {
        "favorite_count": 0, 
        "id_str": "795972820413140992", 
        "retweet_count": 0, 
        "text": "This for testing how the Twitter stream API filters tweets.", 
        "user": {
            "id_str": "2875189485", 
            "screen_name": "jlittman_dev"
        }
    }


The second tweet is @jlittman_dev2's retweet of @jlittman_dev's tweet. This is step 2, showing that retweets by other users of tweets by the followed user are captured. 


```python
# Print the second tweet
tweet2 = json.loads(lines[1])
dump(tweet2)
```

    {
        "favorite_count": 0, 
        "id_str": "795973981035778053", 
        "retweet_count": 0, 
        "retweeted_status": {
            "favorite_count": 0, 
            "id_str": "795972820413140992", 
            "retweet_count": 1, 
            "text": "This for testing how the Twitter stream API filters tweets.", 
            "user": {
                "id_str": "2875189485", 
                "screen_name": "jlittman_dev"
            }
        }, 
        "text": "RT @jlittman_dev: This for testing how the Twitter stream API filters tweets.", 
        "user": {
            "id_str": "795968058280083456", 
            "screen_name": "jlittman_dev2"
        }
    }


The third tweet is the quote by @jlittman_dev of @jlittman_dev2 tweet. This is step 4, showing that quote tweets posted by the followed user are captured.

Note that the quoted tweet (step 3) is not captured because @jlittman_dev2 isn't being followed; however, it is available as the *quoted_status* of the quote tweet.


```python
# Print the third tweet
tweet3 = json.loads(lines[2])
dump(tweet3)
```

    {
        "favorite_count": 0, 
        "id_str": "795974800028082176", 
        "quoted_status": {
            "favorite_count": 0, 
            "id_str": "795974171754897409", 
            "retweet_count": 0, 
            "text": "This is a tweet that will be requoted.", 
            "user": {
                "id_str": "795968058280083456", 
                "screen_name": "jlittman_dev2"
            }
        }, 
        "retweet_count": 0, 
        "text": "I am quoting this tweet. https://t.co/xobWto3mAc", 
        "user": {
            "id_str": "2875189485", 
            "screen_name": "jlittman_dev"
        }
    }


The fourth tweet is a reply by @jlittman_dev2 to a tweet by @jlittman_dev. This is step 6. Thus, replies to the followed user are captured.

Note that the tweet from step 5 (@jlittman_dev2's quote tweet of @jlittman_dev's tweet) was not captured. Thus, quote tweets in which the followed user is quoted are not captured.


```python
# Print the fourth tweet
tweet4 = json.loads(lines[3])
dump(tweet4)
```

    {
        "favorite_count": 0, 
        "id_str": "795975688981544960", 
        "in_reply_to_screen_name": "jlittman_dev", 
        "in_reply_to_status_id_str": "795972351250796545", 
        "in_reply_to_user_id_str": "2875189485", 
        "retweet_count": 0, 
        "text": "@jlittman_dev I am replying to test tweet 15.", 
        "user": {
            "id_str": "795968058280083456", 
            "screen_name": "jlittman_dev2"
        }
    }


The fifth tweet is from step 7, @jlittman_dev's reply to @jlittman_dev's reply. Thus, replies by the followed user to replies are captured.


```python
# Print the fifth tweet
tweet5 = json.loads(lines[4])
dump(tweet5)
```

    {
        "favorite_count": 0, 
        "id_str": "795975981370576896", 
        "in_reply_to_screen_name": "jlittman_dev2", 
        "in_reply_to_status_id_str": "795975688981544960", 
        "in_reply_to_user_id_str": "795968058280083456", 
        "retweet_count": 0, 
        "text": "@jlittman_dev2 I am replying to your reply of test tweet 15.", 
        "user": {
            "id_str": "2875189485", 
            "screen_name": "jlittman_dev"
        }
    }


The final tweet is a reply by @jlittman_dev to a tweet by @jlittman_dev2. Thus, replies by the followed user are captured.


```python
# Print the sixth tweet
tweet6 = json.loads(lines[5])
dump(tweet6)
```

    {
        "favorite_count": 0, 
        "id_str": "795976980416098304", 
        "in_reply_to_screen_name": "jlittman_dev2", 
        "in_reply_to_status_id_str": "795976763809693696", 
        "in_reply_to_user_id_str": "795968058280083456", 
        "retweet_count": 0, 
        "text": "@jlittman_dev2 Replying to your tweet.", 
        "user": {
            "id_str": "2875189485", 
            "screen_name": "jlittman_dev"
        }
    }


The only tweet in our test of the follow parameter of the twitter filter stream that wasn't captured was the quote of a followed user's tweet by another user.

#### Track parameter
Let's see if we can capture that with the track parameter, by using the user's screen name as the keyword.

Note that a user can change her screen name, so that will need to be monitored if using this approach.

Again, I used Twarc to record the filter stream, this time tracking @jlittman_dev (as a keyword):

    twarc.py --track @jlittman_dev > track.json
    
I then performed the following actions on the Twitter website:

1. @jlittman_dev2: Posted [a tweet mentioning @justin_littman](https://twitter.com/jlittman_dev2/status/796403542777065473).
2. @jlittman_dev2: [Quoted](https://twitter.com/jlittman_dev2/status/796403611144224769) [a tweet by @jlittman_dev](https://twitter.com/jlittman_dev/status/795972351250796545).

Only a single tweet is captured.


```python
# Load the tweets
with codecs.open('./track.json', 'r') as f:
    lines = f.readlines()
# Print the number of tweets
print len(lines)
# Print the first tweet
tweet1 = json.loads(lines[0])
dump(tweet1)
```

    1
    {
        "favorite_count": 0, 
        "id_str": "796403542777065473", 
        "retweet_count": 0, 
        "text": "I am mentioning @jlittman_dev again.", 
        "user": {
            "id_str": "795968058280083456", 
            "screen_name": "jlittman_dev2"
        }
    }


This is the tweet that resulted from the mention of @jlittman_dev (step 1). Again, the tweet quoting the followed user wasn't captured.

#### POST statuses/filter summary
Thus, to summarize for a given user, the following can be captured using the filter stream and the follow parameter:

* Tweets, quotes, and replies by that user.
* Retweets of tweets by that user.
* Replies to that user by another user.

but not quotes of that user's tweets by another user. The track parameter does not help with catching quotes of that user's tweets.

## Summary

The Twitter API provides extensive support for retrieving data for studying dialogues and interaction on Twitter.

The following table summarizes what is available in a tweet for retweets, replies, quotes, and favorites.

For a tweet that is ... | Available
------------ | -------------
Retweeted | Count of retweets
A retweet | Source tweet
Quoted | No
A quote | Quoted tweet
Favorited | Count of favorites
Replied to | No
A reply | Replied to tweet

The two most helpful API methods for retweets, replies, quotes, and favorites are GET statuses/user_timeline and POST statuses/filter. The following table summarizes the affordances of these methods:

Tweet type | GET statuses/user_timeline | POST statuses/filter
------------ | ------------- | -------------
Tweets by the user | Yes | Yes
Retweets by the user | Yes | Yes
Retweets by other users of tweet by the user | No | Yes
Quotes by the user | Yes | Yes
Quotes by other users of tweet by the user | No | No
Replies by user | Yes | Yes
Replies by other users to tweet by the user | No | Yes

Note that Social Feed Manager supports collecting using both of these methods.


```python

```
