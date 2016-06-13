---
layout: article
permalink: /posts/pulse-nightclub/
title: "#PulseNightclub"
author: justin_littman
---

It is heartbreaking that our first use of SFM to capture a breaking event was for the shooting at the Pulse Nightclub.  My thoughts go out to the families, the LGBT community, and the people of Orlando.

I first learned about the tragedy at 1pm on June 12.  Upon deciding to collect tweets around this event, I identified some initial seeds based on “Trends” on Twitter.

We don’t yet have a production instance of SFM, so I used a test instance that we have running on AWS. Soon after starting collecting, I had to stop, pull, and restart the ELK, Heritrix, and web harvester containers to make sure they were running the latest code.

As I administered the collection, I took notes of my actions and observations.  The following is a summary drawn from those notes.

## Credentials
Twitter only allows a single stream (filter or sample) to be collected using a set of credentials (API keys) and SFM only allows a user to have one set of Twitter credentials.  While I have multiple Twitter accounts, I already was using my one set of Twitter credentials for an existing filter for the U.S. election.  This forced me to create another SFM account to associate with a different Twitter account.  Fixing this is captured in the following ticket:

[Ticket #317](https://github.com/gwu-libraries/sfm-ui/issues/317): Allow user to have multiple credentials per platform

## Setting up collections
This is the second time I found myself creating a Google Doc to publicly share the collection criteria and seeds.  A public summary page for a collection set would be helpful:

[Ticket #325](https://github.com/gwu-libraries/sfm-ui/issues/325): Optional, public summary page for collection set

## Twitter filter
I created a Twitter filter that tracked “PulseNightClub,PulseShooting,Omar Mateen,ThoughtsAndPrayers,#Orlando”.  (#Orlando was added later based on the Top 10 hashtags report in ELK.)

The Twitter filter ran as expected, creating a new WARC file every half hour.  As of 7:30am on June 13 it had collected 1,625,188 tweets.  On the UI, commas are omitted from the statistics, hence:

[Ticket #318](https://github.com/gwu-libraries/sfm-ui/issues/318): Humanize stats counts

## Twitter search
I created a Twitter search with the query “Pulse OR PulseNightClub OR PulseShooting OR "Omar Mateen" OR gunsense OR terrorism OR islamist OR homophobia.”

My first attempt at creating a query failed because I used “or” instead of “OR”.  This will probably confuse others as well, so:

[Ticket #319](https://github.com/gwu-libraries/sfm-ui/issues/319): Help user with query syntax

The Twitter search harvest did not function as we intended.  For a breaking event, the general strategy is to initiate a filter harvest to collect tweets moving forward and use the search harvest to collect retroactively.  In this case, the search harvest essentially functioned like a stream; it would collect a number of tweets, hit a rate limit, pause and repeat.  The initial search harvest never ended until I killed it after it had collected 1,230,600 tweets.

Unfortunately, the search harvest is not designed to work like a stream.  Rather, it is designed to run for a finite amount of time and conclude.  This produced problems for recording the search in the WARC file and blocked other harvests waiting for the Twitter REST harvester.

[Ticket #319](https://github.com/gwu-libraries/sfm-ui/issues/320): Reconsider Twitter search

## Web harvester
Both the Twitter filter and Twitter stream harvests were configured to extract URLs from the tweets and submit to the web harvester.  The success of the web harvester was mixed; an earlier problem we had encountered with Heritrix encountering a problem towards the end of a crawl re-occurred:
```
2016-06-12 18:41:51.107 WARNING thread-50 com.google.common.cache.LocalCache.processPendingNotifications() Exception thrown by removal listener
java.util.ConcurrentModificationException
and then:
UNREGISTERED FOR KRYO class java.util.LinkedHashSet in class 
```

I had hoped [LBS-2016-02](https://kris-sigur.blogspot.com/2016/05/LBS-2016-02.html?spref=tw) would fix this, but it appears not.  I’ll have to reach out to colleagues in the Heritrix community for assistance.

[Ticket #321](https://github.com/gwu-libraries/sfm-ui/issues/321): Heritrix failing at the end of long crawls

## ELK
The [ELK stack](https://www.elastic.co/products) is a general-purpose framework for exploring data that we have [customized for social media data](http://sfm.readthedocs.io/en/latest/exploring.html). One of the primary uses we intended for ELK was to assist with breaking events.  Before beginning collecting, I configured an instance of an ELK container to be loaded with data from this collection set.  For following #PulseNightclub, charts like the following were extremely useful:

![hashtags viz]({{ site.github.url }}/images/pulse/hashtags_viz.png)

Data is loaded into ELK after the WARC file is created and the data loading takes some amount of time.  Thus, there is a latency.  This latency made it difficult to understand what had already been loaded into ELK.  Thus:

[Ticket #322](https://github.com/gwu-libraries/sfm-ui/issues/322): Provide clarity on what has been loaded into ELK

My experience with ELK also prompted some additional tickets:

[Ticket #323](https://github.com/gwu-libraries/sfm-ui/issues/323): In ELK, normalize hashtag capitalization

[Ticket #324](https://github.com/gwu-libraries/sfm-ui/issues/324): In ELK, add top retweets vizualization

## Monitoring
The biggest weakness in this effort was monitoring the collection process.  We were already reasonably aware of this, as we already have a number of related tickets.  This just reinforced the importance of:

[Ticket #229](https://github.com/gwu-libraries/sfm-ui/issues/229): Preserve logs

[Ticket #303](https://github.com/gwu-libraries/sfm-ui/issues/303): Need mechanism for monitoring harvesters/exporters

[Ticket #310](https://github.com/gwu-libraries/sfm-ui/issues/310): Failure indications in UI for Harvests and Exports

## Moving collections
This collection was created on a test instance of SFM; if we choose to retain this collection we’ll want to move it to our (future) production instance.  Thus:

[Ticket #326](https://github.com/gwu-libraries/sfm-ui/issues/326): Support for import / export of collection sets

## Conclusion
I haven’t discussed with my colleagues whether to retain this collection.  However, my initial inclination is to not do so since it is not within our institution’s collection development policy.  I’ve learned from my work elsewhere that digital collections that are acquired without designated custodians don’t fare well.  Further, there are privacy and ethical dimensions of this collection that require careful consideration.  (If you have thoughts about the disposition of this collection, please share them with us.)

While affirming the overall design of SFM, performing this event capture identified some gaps in SFM’s functionality and adjustments that must be made in existing functionality.  Some of these needs we were already aware of and were on our roadmap; others came to our attention solely through this experience.

Collecting #PulseNightclub will leave us better prepared to capture the next breaking event.  I just hope it isn’t another shooting.