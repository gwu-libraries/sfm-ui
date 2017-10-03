---
layout: article
permalink: /posts/2017-10-03-blacktivist
title: "Searching for @Blacktivist (fake account) in the archive"
author: justin_littman 
excerpt: "In which I go searching for tweets related to the Russian government-linked fake Twitter account, @Blacktivist."
---

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Can&#39;t wait for historians to discover the deleted tweets hidden in my musty old digital archive.</p>&mdash; Karl Blumenthal 🌹 (@landlibrarian) <a href="https://twitter.com/landlibrarian/status/889294609678991360?ref_src=twsrc%5Etfw">July 24, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

On September 28th, it was [disclosed]( http://money.cnn.com/2017/09/28/media/blacktivist-russia-facebook-twitter/index.html) that the Russian government was behind a social media campaign to heighten racial tensions during the 2016 U.S. presidential campaign. The campaign, on both Facebook and Twitter used the handle "Blacktivist".

Bergis Jules, University & Political Papers Archivist at University of California Riverside and community lead of the [DocNow](http://www.docnow.io/) project, and Catie Bailard, 
Associate Professor of Media and Public Affairs in George Washington University's School of Media & Public Affairs, independently inquired whether we had any tweets related to Blacktivist in our [2016 U.S. presidential election Twitter collection](http://dx.doi.org/10.7910/DVN/PDI7IN). One part of this collection, collected from Twitter’s filter stream API with Social Feed Manager contains 250 million tweets that have the terms "election2016", "election", "clinton", "kaine", "trump", or "pence" or mention @realDonaldTrump, @HillaryClinton, @TimKaine, and @Mike_Pence. Collecting the tweets occurred between July 13, 2016 and November 10, 2016. The collection also contains 30 million additional tweets focused on particular events such as the debates or conventions or collected from the timelines of candidates and parties. So I set out to find tweets related to Blacktivist in our archive.

To speed up the search, I looked through the tweets in parallel, passing them through a utility called jq to find tweets that contained the term “Blacktivist” or were posted by @Blacktivist:
	
	    parallel -a source.lst -a dest.lst --xapply "twitter_stream_warc_iter.py {1} | jq -c 'select((.text | test(\"blacktivist\"; \"i\")) or (.user.screen_name | test(\"blacktivist\"; \"i\")))' > {2}"

The result was 87 tweets, contained in [this spreadsheet]({{ site.github.url }}/resources/blacktivist.csv). As you can see, this includes some tweets that are probably not directly related to @Blacktivist.

In keeping with [Twitter’s Developer Policy](https://developer.twitter.com/en/developer-terms/agreement-and-policy), we don’t publicly share tweets, especially deleted tweets. However, given the unique nature of these tweets I am making an exception.

If you’re interested in searching our U.S. presidential election collection, check out [TweetSets](https://tweetsets.library.gwu.edu/). I’m in the process of loading it with all 250 million tweets and expect it to take several days, if I don’t encounter any technical difficulties. Once loaded, you will be able to search the tweets and export the tweet ids of matching tweets.

