---
layout: article
permalink: /posts/2017-03-31-extended-tweets
title: "On Extended Tweets"
author: justin_littman 
excerpt: "This post describes the impact of recent changes made by Twitter to allow extended tweets on the REST and Streaming APIs."
---

Last spring, Twitter [announced some forthcoming changes](https://blog.twitter.com/express-even-more-in-140-characters) to the structure of a tweet. These include (1) removing @replies (at the beginning of a tweet) from the body of the tweet and (2) removing media attachments (URLs at the end of a tweet) from the body of the tweet. Together, these enabled “extended tweets” which are tweets that (including @replies and media attachments) can include more than 140 characters. Those of us who are trying to squeeze in those last few words without sacrificing grammar will appreciate the additional characters.

Twitter followed this up a few weeks ago with some [additional details](https://dev.twitter.com/overview/api/upcoming-changes-to-tweets) on changes this would entail in the Twitter API. Yesterday (March 30), the [first of these changes went live](https://blog.twitter.com/2017/now-on-twitter-140-characters-for-your-replies) on the Twitter website.  These changes impact applications like Social Feed Manager that collect social media data.  The goal of this blog post is to explore the salient changes.

The new features will impact the [REST API](https://dev.twitter.com/rest/public) and the [Streaming API](https://dev.twitter.com/streaming/overview) differently.

Here’s a sample tweet that I’ll be referring to:

![tweet]({{ site.github.url }}/images/extended-tweets/tweet.png)

## REST API
Adding the query parameter `tweet_mode=extended` will return extended tweets. Here’s an [example of an extended tweet](https://gist.github.com/justinlittman/4b0a49cfaa63cc3b92ca6471b7adbbd6). For comparison, here is the [classic (non-extended) version](https://gist.github.com/justinlittman/3822b318ebdd8dc5d5c7b64aee78389a).

In extended tweets from the REST API, the `full_text` field replaces the `tex`t field. The `full_text` field may contain more than 140 characters:

![full_text]({{ site.github.url }}/images/extended-tweets/full_text.png)

In addition, the `display_text_range` field contains the offsets in `full_text` of the body of the tweet:

![display_text_range]({{ site.github.url }}/images/extended-tweets/display_text_range.png)


## Streaming API
The Streaming API does not accept parameters, so there is no ability to select extended tweets or classic tweets. Rather, if a tweet contains some of the extended features, then an additional field called `extended_tweet` is added. `extended_tweet` includes `full_text` (which may be more than 140 characters), `display_text_range` (the offsets in full_text of the body of the tweet), and `entities` / `extended_entities` (parsed out hashtags, mentions, URLs, media, etc.).

Here’s the `extended_tweet` section from a [sample tweet](https://gist.github.com/justinlittman/bb488bfa86b7b2965ef5b44e408cbd83):

![extended_tweet]({{ site.github.url }}/images/extended-tweets/extended_tweet.png)

A few notes:
* All of the existing fields remain; in particular, the `text` field still exists and is limited to 140 characters.

![text]({{ site.github.url }}/images/extended-tweets/text.png)

* Based on a look at the sample stream, the `extended_tweet` field is not included in all tweets, only those using the extended features.

## Implementation
The latest release of DocNow’s [twarc](https://github.com/DocNow/twarc) already supports extended tweets. Extended tweets can be selected by adding `--tweet_mode extended` to the commandline or setting the [tweet_mode argument](https://github.com/DocNow/twarc/blob/v1.0.10/twarc.py#L87) in Twarc’s constructor.

SFM will be adding support for extended tweets in the forthcoming 1.7 release. (Here’s the [ticket](https://github.com/gwu-libraries/sfm-ui/issues/737).) In addition to incorporating the new version of twarc, we’ll make sure that all parts of the application that extract data from the tweet handle all three flavors (classic, extended REST, and extended streaming).
 
## Try it yourself
To get some extended tweets from the REST API using twarc:

    python twarc.py --tweet_mode extended timeline SocialFeedMgr

To get some extended tweets from the Streaming API using twarc:

    python twarc.py --tweet_mode extended sample | jq 'select(has("extended_tweet"))'

You may need to wait a bit for an extended tweet.