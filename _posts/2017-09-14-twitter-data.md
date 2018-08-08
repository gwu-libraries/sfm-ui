---
layout: article
permalink: /posts/2017-09-14-twitter-data
title: "Where to get Twitter data for academic research"
categories: top
author: justin_littman 
excerpt: "Justin Littman explains the options for acquiring Twitter data for academic research."
---

It has been my experience that faculty, students, and other researchers have no shortage of compelling research questions that require Twitter data. However, many face an immediate barrier in understanding the options for acquiring that data. The purpose of this blog post is to describe the options for getting Twitter data for academic research in the hopes of lowering at least that initial barrier.

Just as the research to be performed is varied, so are the requirements for Twitter data. These include:
* Are historical tweets needed? Or current tweets?
* How many tweets are needed?
* Is a complete dataset needed (i.e., every tweet that meets criteria) or is an incomplete or sampled dataset acceptable?

In addition, other relevant factors of the research include:
* Does the researcher have funding to acquire Twitter data?
* Does the researcher need to share the Twitter dataset as part of publication / reproducible research?
* What are the technical skills of the researcher?
* How will the researcher be performing analysis? With her own tools? Or would analytic tools for Twitter data be beneficial?

These factors will determine the most appropriate means of acquiring a Twitter dataset.

There are 4 primary ways of acquiring Twitter data (and I’m not including “cutting and pasting” from the Twitter website!):
* Retrieve from the Twitter public API.
* Find an existing Twitter dataset.
* Purchase from Twitter.
* Access or purchase from a Twitter service provider.

Let’s explore each of these.

### 1. Retrieve from the Twitter public API 
API is short for “Application Programming Interface” and in this case is a way for software to access the Twitter platform (as opposed to the Twitter website, which is how humans access Twitter). While supporting a large number of functions for interacting with Twitter, the API functions most relevant for acquiring a Twitter dataset include:
* Retrieving tweets from a user timeline (i.e., the list of tweets posted by an account)
* Searching tweets
* Filtering real-time tweets (i.e., the tweets as they are passing through the Twitter platform upon posting)

While you can write your own software for accessing the [Twitter API](https://developer.twitter.com/en/docs), a number of tools already exist. They are quite varied in their capabilities and require different levels of technical skills and infrastructure. These include:
* Software libraries (e.g., [Tweepy](http://www.tweepy.org/) for Python and [rtweet](https://github.com/mkearney/rtweet) for R)
* Command line tools (e.g., [Twarc](https://github.com/docnow/twarc))
* Web applications (e.g., [DMI-TCAT](https://github.com/digitalmethodsinitiative/dmi-tcat) and our very own [Social Feed Manager](http://go.gwu.edu/sfm))
* Plugins for popular analytic packages (e.g., [NVIVO](http://www.qsrinternational.com/product), [NodeXL](http://www.smrfoundation.org/nodexl/) for Excel, and [TAGS](https://tags.hawksey.info/) for Google Sheets)

Some of these tools are focused on retrieving tweets from the API, while others will also do analysis of the Twitter data. For a more complete list, see the [Social Media Research Toolkit](http://socialmediadata.org/social-media-research-toolkit/) from the Social Media Lab at Ted Rogers School of Management, Ryerson University.

Note when selecting a tool that some may only support part of the Twitter API for retrieving tweets, most commonly, search. Further, some tools may be designed to support one-time retrieval from the Twitter API, while others support retrieval on an ongoing basis. (For example, Social Feed Manager allows you to specify a schedule for recurring data collection.)

What all of these tools share in common is that they use Twitter’s public API. The Twitter public API has a number of limitations that you should be aware of:
* Access to historical tweets is extremely limited. You can retrieve the last 3,200 tweets from a user timeline and search the last 7-9 days of tweets.
* Access to current tweets is limited. Depending on how broad your filter is, the API may not return all tweets.
* Twitter may sample or otherwise not provide a complete set of tweets in searches.  

### 2. Find an existing Twitter dataset
One way to overcome the limitations of Twitter’s public API for retrieving historical tweets is to find a dataset that has already been collected and satisfies your research requirements. For example, here at GW Libraries we have proactively built collections on a number of topics including Congress, the federal government, and news organizations.

Twitter’s [Developer Policy](https://dev.twitter.com/overview/terms/agreement-and-policy) (which you agree to when you get keys for the Twitter API) places limits on the sharing of datasets. If you are sharing datasets of tweets, you can only publicly share the ids of the tweets, not the tweets themselves. Another party that wants to use the dataset has to retrieve the complete tweet from the Twitter API based on the tweet id (“hydrating”). Any tweets which have been deleted or become protected will not be available.

DocNow’s [Hydrator](https://github.com/DocNow/hydrator) is a useful tool for retrieving tweets from the Twitter API based on tweet id. Note that Twitter places rate limits on hydrating (as it does on most API functions) so this may take some amount of time depending on the size of the dataset.

A number of individuals and organizations have publicly posted Twitter datasets, e.g., in a dataset repository or on a website. For example, we posted our 280 million tweet [dataset from the 2016 U.S. presidential election](http://dx.doi.org/10.7910/DVN/PDI7IN) on Harvard’s Dataverse. Deen Freelon has published the 40 million tweet [dataset for the “Beyond the Hashtags: #Ferguson, #Blacklivesmatter, and the Online Struggle for Offline Justice” report](http://dfreelon.org/2017/01/03/beyond-the-hashtags-twitter-data/) on his website. The [DocNow Catalog](http://www.docnow.io/catalog/) provides a listing of publicly available Twitter datasets.

Twitter’s Developer Policy is generally interpreted as allowing sharing of tweets locally, i.e., within an academic institution. For example, we share the datasets we have collected at GW Libraries with members of the GW research community (but when sharing outside the GW community, we only share the tweet ids). However, only a small number of institutions proactively collect Twitter data -- your library is a good place to inquire.

Another option for acquiring an existing Twitter dataset is [TweetSets](https://tweetsets.library.gwu.edu/), a web application that I’ve developed. TweetSets allows you to create your own dataset by querying and limiting an existing dataset. For example, you can create a dataset that only contains original tweets with the term “trump” from the Women’s March dataset. If you are local, TweetSets will allow you to download the complete tweet; otherwise, just the tweet ids can be downloaded. Currently, TweetSets includes nearly a half billion tweets.

### 3.  Purchase from Twitter
You can purchase historical Twitter data directly from Twitter, using the [Historical PowerTrack](https://developer.twitter.com/en/docs/tweets/batch-historical/overview) enterprise product.
 
 Historical Twitter data was previously available from Gnip, a data service provider purchased by Twitter. Gnip has now been folded into Twitter. The way this used to work is that you provided a set of query terms and other limiters and a Gnip sales rep replied with a cost estimate. With recent changes, the process is less clear.
 
 For filtering tweets, the Historical Powertrack offers a number of enhancements over the public Twitter API. This includes [additional filter operators](https://developer.twitter.com/en/docs/tweets/rules-and-filtering/overview/all-operators) and tweet enhancements (e.g., profile location and unshortened URLs).
  
  When considering purchasing tweets, you should be aware that it is not likely to be a trivial amount of money. The cost depends on both the length of the time period and the number of tweets; often, the cost is driven by the length of the time period, so shorter periods are more affordable. The cost may be feasible for some research projects, especially if the cost can be written into a grant. Further, I am not familiar with the conditions placed on the uses / sharing of the purchased dataset. Nonetheless, this is likely to be as complete a dataset as it is possible to get.

### 4. Access or purchase from a Twitter service provider
A number of commercial and academic organizations act as Twitter service providers, usually for a fee. These services provide: 
* Access to Twitter data
* Value-added services for the Twitter data, such as coding, classification, analysis, or data enhancement. If you are not using your own tools for analysis, these value-added services may be extremely useful for your research (or they may be used in combination with your own tools).

Twitter data options available from a service provider generally include one or more of the following types (available at different costs):
* Data from the public Twitter APIs. This obviously comes with the limitations described previously with the public Twitter APIs, but will be less costly than the other Twitter data options.
* Data from the enterprise Twitter APIs, which have access to all historical tweets. Like purchasing data directly from Twitter, the cost will depend on factors such as the number of tweets and the length of the time period. [DiscoverText](https://discovertext.com/) offers this type of data acquisition.
* Datasets built by querying against an existing set of historical tweets. The service provider will have an arrangement with Twitter that will provide them with access to the “firehose” of all tweets to build this collection. [Crimson Hexagon](https://www.crimsonhexagon.com/) offers this type of data acquisition.

Twitter service providers generally provide reliable access to the APIs, with redundancy and backfill. This means that you will not miss tweets because of network problems or other issues that might occur when using a tool to access the APIs yourself. Note, also, that some service providers can provide data from other social media platforms, such as Facebook.

Despite what the sales representative may tell you, most Twitter service providers’ offerings focus on marketing and business intelligence, not academic research. The notable exception is DiscoverText, which is focused primarily on supporting academic researchers. DiscoverText allows you to acquire data from the public Twitter Search API; purchase historical tweets through the Twitter data access tool, Sifter; or upload other types of textual data. [Sifter](http://sifter.texifter.com) provides free cost estimates and has a lower entry price point ($32.50) than purchasing from Twitter. Within the DiscoverText platform, tweets can be searched, filtered, de-duplicated, coded, and classified (using machine learning), along with a host of other functionality. Key for academics are features for measuring inter-coder reliability and adjudicating annotator disagreements.

Crimson Hexagon focuses on marketing, but also supports academic research. [Soda Analytics](https://www.sodanalytics.com/) is a new entry in the academic field.

Note that some academic institutions have licenses to Twitter service providers; check with your department or a data services librarian.

There are some limitations of Twitter service providers that you should be aware of. Whether these limitations are significant will depend on your research requirements.

First, when considering a Twitter service provider, it is important to know whether you are able to export your dataset from the service provider’s platform. (All should allow you to export reports or analysis.) For most platforms, export is limited to 50,000 tweets per day. If you need the raw data to perform your own analysis or for data sharing, this may be an important consideration.

Second, while the value-added services offered by a Twitter service provider may be very powerful and not require technical skill to use, they are generally a “black box”. So, for example, if a service provider performs bot detection, you may not know which bot detection algorithm is being used.

### Conclusion
As should now be evident, the combination of Twitter’s restrictions on sharing data and the affordances of Twitter’s public API makes acquiring a Twitter dataset for academic research not entirely straight-forward. Hopefully this guide has provided enough of a description of the landscape for Twitter data that you can move forward with your research.

[Comments](https://gwu-libraries.github.io/sfm-ui/contact) on this guide and [questions](https://gwu-libraries.github.io/sfm-ui/contact) about Twitter data are welcome.
