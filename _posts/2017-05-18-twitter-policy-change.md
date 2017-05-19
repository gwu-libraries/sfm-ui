---
layout: article
permalink: /posts/2017-05-18-twitter-policy-change
title: "Implications of changes in Twitter’s Developer Policy"
author: justin_littman 
excerpt: "On May 18, Twitter announced changes to its Developer Policy that has significant impacts for researchers and archivists. The goal of this blog post is to describe the change and its implications."
---

Because of the prominent role that Twitter plays in the social, political, and cultural discourse of contemporary society, activity on Twitter has increasingly become the subject of research across a wide array of disciplines and the focus of collecting by archival organizations concerned with preserving the historical record. On May 17 Twitter announced a changed in their [Developer Policy](https://dev.twitter.com/overview/terms/agreement-and-policy) to go in effect on June 18 that significantly impacts both of those activities. The goal of this blog post is to describe the change and its implications.

For both research and archival purposes, the primary mechanism for collecting Twitter data are [Twitter’s APIs]( https://dev.twitter.com/overview/api). Twitter’s APIs support the efficient collection of large numbers of tweets in a format that is amenable to computational analysis and archiving. Collecting Twitter data is governed by the technical affordances of the API and the Developer Policy.

A key feature of the technical affordances of Twitter’s APIs is that they provide very limited ability to collect tweets from the past (viz., the last 3,200 tweets from a user’s timeline and the last 7-9 days via search). Rather, Twitter’s APIs require that tweet collection be performed contemporaneous to the tweet activity. For archiving, this means that tweets must be collected now if they are to be available in the future. Similarly, tweets that are collected in the present for research cannot be collected again in the future.

Here’s an example: At GW Libraries, we collected Twitter data related to the 2016 U.S. election with [Social Feed Manager]( https://gwu-libraries.github.io/sfm-ui/). Some of datasets we collected include:
* Candidates and key election hashtags (Twitter filter)
* Democratic candidates (Twitter user timelines)
* First presidential debate (Twitter filter)
* GOP Convention (Twitter filter)

Overall, this collection contains 280 million tweets. As has been noted elsewhere, writing the history of the 2016 U.S. election will be incomplete without the Twitter data.

The implications of the technical affordances of Twitter’s APIs is that both archival organizations and researchers have the need to share Twitter datasets. For archival organizations it is the only mechanism to acquire a Twitter datasets that it didn’t originally collect, to complete a collecting with "holes," or to compare collections. (Collecting Twitter data by archival organizations is an emerging activity. See the [DocNow catalog](http://www.docnow.io/catalog/). Similarly, for quality research, that research must be reproducible. In addition to documenting the research methodology and sharing any code used for analysis, reproducible research requires access to the dataset, which means that dataset must be shared between researchers.

Ideally, researchers and archivists would just be able to exchange Twitter datasets. However, Twitter’s Developer Policy limits the sharing of Twitter datasets. Prior to May 18, in section F (Be a Good Partner to Twitter), this policy stated:

> 2. If you provide Content to third parties, including downloadable datasets of Content or an API that returns Content, you will only distribute or allow download of Tweet IDs and/or User IDs.

> a. You may, however, provide export via non-automated means (e.g., download of spreadsheets or PDF files, or use of a "save as" button) of up to 50,000 public Tweets and/or User Objects per user of your Service, per day.

> b. Any Content provided to third parties via non-automated file download remains subject to this Policy.

Thus, researchers and archivists were required to share datasets of tweet ids, rather than the tweets themselves. Twitter’s API allows retrieving a tweet from the tweet id (known as "hydrating" a tweet). While [rate limits](https://dev.twitter.com/rest/public/rate-limiting) on Twitter’s API make this is a slow process, there are tools to make it easy (e.g., [Hydrator](https://github.com/DocNow/hydrator)). One aspect of this approach is that if a tweet has been deleted or protected, it cannot not be retrieved by tweet id. While making for imperfect sharing of datasets, this gave authors some measure of control over their tweets.

In conformance with this policy, researchers and archivists posted datasets of tweet ids on data repositories and Github. Here’s our [Women’s March collection]( https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/5ZVMOR) on Harvard’s Dataverse and the [tweet ids]( http://dfreelon.org/2017/01/03/beyond-the-hashtags-twitter-data/) that support the seminal research paper, "[Beyond the Hashtags: #Ferguson, #Blacklivesmatter, and the Online Struggle for Offline Justice](http://cmsimpact.org/resource/beyond-hashtags-ferguson-blacklivesmatter-online-struggle-offline-justice/)".

The policy that goes into effect on June 18 significantly limits this:

> 2. If you provide Content to third parties, including downloadable datasets of Content or an API that returns Content, you will only distribute or allow download of Tweet IDs, Direct Message IDs, and/or User IDs.

> a. You may, however, provide export via non-automated means (e.g., download of spreadsheets or PDF files, or use of a "save as" button) of up to 50,000 public Tweet Objects and/or User Objects per user of your Service, per day.

> b. Any Content provided to third parties remains subject to this Policy, and those third parties must agree to the Twitter Terms of Service, Privacy Policy, Developer Agreement, and Developer Policy before receiving such downloads.

>    a. You may not distribute more than 1,500,000 Tweet IDs to any entity (inclusive of multiple individual users associated with a single entity) within any given 30 day period, without the express written permission of Twitter.
>    b. You may not distribute Tweet IDs for the purposes of (a) enabling any entity to store and analyze Tweets for a period exceeding 30 days without the express written permission of Twitter, or (b) enabling any entity to circumvent any other limitations or restrictions on the distribution of Twitter Content as contained in this Policy, the Twitter Developer Agreement, or any other agreement with Twitter.

Whereas previously the sharing of tweet ids was unlimited, it is now limited to 1.5 million per month per organization. While some archival and research datasets fall below this threshold, 1.5 million is not a large number of tweets. Here’s the size of some of our collections:
* U.S. election: 280 million tweets
* U.S. government: 6 million tweets
* U.S. congress: 1.5 million tweets
* News organizations: 14 million tweets
* Healthcare: 32 million tweets
* Make America Great Again: 21 million tweets
* Immigration and travel ban executive order: 17 million tweets

Further, the sites which researchers and archivists use to share Twitter datasets (e.g., Github, Dataverse) have no mechanism for restricting the distribution of datasets as is required by this policy.

Some additional questions raised by this policy:
* If I post a Twitter dataset on Github or Dataverse, are those organizations bound by or have responsibilities under this policy?
* What does "You may not distribute Tweet IDs for the purposes of (a) enabling any entity to store and analyze Tweets for a period exceeding 30 days" mean?

What I’ve left out so far is one additional way that Twitter datasets can be acquired: purchasing from a Twitter data provider such as [Gnip]( https://gnip.com/) or [DiscoverText]( https://discovertext.com/). While making sense for some research, in general purchasing data is outside the means of most researchers (and certainly archival organizations). Further, I believe that purchased datasets have significant limitations on how they can be shared (though I’m not familiar with the exact terms).

Thus, it is evident that the change in Twitter’s Developer policy has severe implications for both Twitter research and archiving. Ed Summers has [already called for these communities to start a discussion with Twitter]( https://twitter.com/edsu/status/865154800253640704) about this policy change. I’d second this call.
