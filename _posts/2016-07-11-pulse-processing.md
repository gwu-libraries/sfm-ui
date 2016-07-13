---
layout: article
permalink: /posts/2016-07-11-pulse-processing
title: "Extracting URLs from #PulseNightclub for seeding web archiving"
author: justin_littman 
excerpt: "Last week, Internet Archive put out a call for URL nominations for a Pulse Nightclub web collection. This blog post describes how I extracted 200,094 unique URLs from the 4,153,157 tweets we collected around the Pulse Nightclub tragedy."
---

As described in [this blog post](http://gwu-libraries.github.io/sfm-ui/posts/pulse-nightclub/]), we collected 
tweets around the Pulse Nightclub tragedy in Orlando.  Altogether, we collected 4,153,157 tweets between 
June 12 and June 20.

![tweets viz]({{ site.github.url }}/images/pulse_processing/tweet_viz.png)

Last week, Jefferson Bailey from [Internet Archive](https://archive.org/) put out a call for URL nominations for a Pulse Nightclub web collection.

![Bailey tweet]({{ site.github.url }}/images/pulse_processing/bailey_tweet.png)

I decided to extract URLs from the tweets we collected to make nominations for the Pulse Nightclub web collection.  The goal of this blog post is to share the process and tools I used to extract the URLs.

I'm going to get into a fair bit of detail about the process and tools.  This might make it seem like extracting the URLs is complicated, but it's actually quite simple.  If all you want are the commands to execute, skip ahead to the "Serial processing" or "Parallel processing" section.

The outline for the steps to be performed are:

1. Find the WARC files that contain #PulseNightclub tweets. (If you're new to SFM, we store social media data in WARC files. This always us to record *exactly* how the data was collected.)
2. Extract the tweets from each WARC file.
3. Expand any shortened URLs in each tweet.  (Some Twitter users use [URL shorteners](https://en.wikipedia.org/wiki/URL_shortening) to shorten URLs included in tweets.  To normalize the URLs, I’m unshortening them all.)
4. Extract URLs from each tweet.
5. Filter out retweet URLs.  (Retweets include the URL of the original tweet.  We want to exclude these URLs.)
6. Get a count of each URL.
7. Sort the URLs by count.

Before getting into the details, I should note that I used an SFM [processing container](http://sfm.readthedocs.io/en/latest/processing.html#processing-in-container) for this work.  A processing container is a Docker container that provides an Ubuntu environment with a host of SFM and other utilities pre-installed, as well as access to an SFM instance’s social media data.  Processing containers bootstrap working with social media data from the command line.

Here’s how I instantiated the processing container:

    docker run -it --rm --link=ubuntu_sfmuiapp_1:api --link=unshrtn --volumes-from=ubuntu_sfmdata_1:ro --volume=/home/ubuntu/sfm-processing:/sfm-processing gwul/sfm-processing:master

Let me point out a few parts of this command:

* `--volumes-from=ubuntu_sfmdata_1:ro`:  Notice the “ro” for read-only.  Making the source social media data unwritable is one of the (hard) lessons learned from [Archives Unleashed 2.0](http://archivesunleashed.com/).
* `--link=unshrtn`:  This wouldn’t normally be part of the command for instantiating a processing container.  However, it is necessary to link in the unshrtn service as described below.
* `--volume=/home/ubuntu/sfm-processing:/sfm-processing`:  This links in a directory from outside Docker into the processing container.  This is where I will place any scripts or output files to make sure they outlive the processing container and I can reach them from outside Docker.
* `gwul/sfm-processing:master`:  Normally you’d use a specific version (e.g., 1.0.0) instead of “master”.  However, I wanted to test the [10X improvement](https://github.com/gwu-libraries/sfm-ui/issues/340) we just made in extracting tweets from WARCs so I used master.

After executing this command, I am brought to a command prompt inside the processing container.  It’s just like being shelled into any server.

## Tools
Let’s take a look at some of the tools we’ll use:

### `find_warcs.py`: Find the WARC files

The `find_warcs.py` tool returns a list of WARC files for the collection.  This requires the collection id, which is available from the collection detail page in SFM UI.

Actually, you only need a fragment of the collection id:

    find_warcs.py 4e1c

Output:

	/sfm-data/collection_set/76807d1607654b00a6c90e8996d6023f/4e1c8bf97ed0461bb598c0e20e426f0f/2016/06/12/17/3233eab291d64d04a036986e1d3c0e2d-20160612173338922-00000-4083-38d36eefa455-8001.warc.gz /sfm-data/collection_set/76807d1607654b00a6c90e8996d6023f/4e1c8bf97ed0461bb598c0e20e426f0f/2016/06/12/18/b2f9bad5e4f344a48a5749cdc800fa53-20160612180418899-00000-4123-38d36eefa455-8001.warc.gz ...

(Note that long output here and below will be truncated with `...`.)

There are 347 WARCs in the collection.

`find_warcs.py` offers some options to limit the WARCs that are returned, e.g., limiting by harvest date, but we’re not going to use them for this process.

### `twitter_stream_warc_iter.py`:  Extract the tweets from the WARC file

`twitter_stream_warc_iter.py` extracts the tweets from a WARC file.  There are variations of this for other forms of social media, e.g., `flickr_photo_warc_iter.py` for Flickr photos.

For the following command and others in this blog post, I'm going to shorten long filepaths like `/sfm-data/collection_set/76807d1607654b00a6c90e8996d6023f/4e1c8bf97ed0461bb598c0e20e426f0f/2016/06/12/17/3233eab291d64d04a036986e1d3c0e2d-20160612173338922-00000-4083-38d36eefa455-8001.warc.gz` to `/sfm-data/38d36eefa455-8001.warc.gz`.

This extracts the tweets from a single WARC file:

	twitter_stream_warc_iter.py /sfm-data/38d36eefa455-8001.warc.gz

Output:

	{"contributors": null, "truncated": false, "text": "RT @johnlegend: Trump is truly an awful person.  https://t.co/vQp3CQ9Nmv", "is_quote_status": true, "in_reply_to_status_id": null, "id": 742042058588848128, "favorite_count": 0, "entities": {"user_mentions": [{"id": 18228898, "indices": [3, 14], "id_str": "18228898", "screen_name": "johnlegend", "name": "John Legend"}], "symbols": [], "hashtags": [], "urls": [{"url": "https://t.co/vQp3CQ9Nmv", "indices": [49, 72], "expanded_url": "https://twitter.com/deray/status/742039900577402880", "display_url": "twitter.com/deray/status/7\u202 ...

The output of `find_warcs.py` can be piped into `twitter_stream_warc_iter.py`:

	find_warcs.py 4e1c | xargs twitter_stream_warc_iter.py

### `unshorten.py` and the unshrtn service: Expand URLs

[`unshorten.py`](https://github.com/edsu/twarc/blob/master/utils/unshorten.py) is a Twarc utility that finds URLs in tweet metadata, expands them using an unshrtn service, and inserts the unshortened URLs back into the tweet metadata using the “unshortened_url” key.  Here’s an example:

	"urls": [{
		"url": "https://t.co/wL0KEgDpPb",
		"indices": [52, 75],
		"unshortened_url": "https://twitter.com/usatoday/status/741998414582415360",
		"expanded_url": "https://twitter.com/usatoday/status/741998414582415360",
		"display_url": "twitter.com/usatoday/statu\
			u2026 "
	}]

The output of `twitter_stream_warc_iter.py` can be piped into `unshorten.py`:

	twitter_stream_warc_iter.py /sfm-data/38d36eefa455-8001.warc.gz | python /opt/twarc/utils/unshorten.py --unshrtn http://unshrtn:3000

`unshorten.py` depends on an [unshrtn service](https://github.com/edsu/unshrtn), written by [Ed Summers](http://inkdroid.org/).  The unshrtn service will resolve the shortened URL and return the result.  It keeps track of URLs that it has already resolved to make the process more efficient.

The unshrtn service can be run as a Docker container.  Here’s how I built and instantiated the unshrtn Docker container:

	docker build --tag unshrtn:latest .
	docker run -d --name=unshrtn --restart=always -t unshrtn:latest

I encountered a few gotchas using `unshorten.py` / unshrtn service.

First, `unshorten.py` was hardcoded with the URL of the unshrtn service.  Since I wanted to link the unshrtn container into the processing container, I had to [make the URL of the unshrtn service configurable](https://github.com/edsu/twarc/pull/108) in `unshorten.py`.  Thus, when the unshrtn container was linked in (with `--link=unshrtn` in the processing container’s docker run command), `unshorten.py` could be configured to use it (by adding  `--unshrtn http://unshrtn:3000` to the `unshorten.py` command).

Second, the unshrtn service crashed in the middle of my first long run.  To address this, I set the unshrtn container to automatically restart (by adding `--restart=always` to unshrtn’s docker run command) and [added retrying](https://github.com/edsu/twarc/pull/109) to unshorten.py.

### `urls.py`: Extract URLs from tweets
[`urls.py`](https://github.com/edsu/twarc/blob/master/utils/urls.py) is a Twarc utility that extracts URLs from tweet metadata.

    twitter_stream_warc_iter.py /sfm-data/38d36eefa455-8001.warc.gz | python /opt/twarc/utils/urls.py

Output:

	https://twitter.com/realdonaldtrump/status/742034549232766976
	https://twitter.com/breakingnews/status/742041568069193728
	https://twitter.com/Phil_Lewis_/status/742003830276100096
	https://twitter.com/Delo_Taylor/status/742033610438545409
	https://twitter.com/chasestrangio/status/742001494489223168
	…

If an unshortened url is available, `urls.py` will prefer it.

### `grep`: Filtering
The unix `grep` utility can be used to remove Twitter URLs.

	twitter_stream_warc_iter.py /sfm-data/38d36eefa455-8001.warc.gz | python /opt/twarc/utils/urls.py | grep -v https://twitter.com

### `sort` and `uniq`:  Sorting and counting
The unix command line utilities `sort` and `uniq` are used to sort and count the URLs.

`sort` performs a sort of the URLs; `uniq` counts the URLs.  If you combine them, you can count and order the URLs:

	twitter_stream_warc_iter.py /sfm-data/38d36eefa455-8001.warc.gz | python /opt/twarc/utils/urls.py | sort | uniq -c | sort -rn

Output:

	   2247 https://twitter.com/realdonaldtrump/status/742034549232766976
	    935 https://twitter.com/deray/status/742039900577402880
	    414 https://twitter.com/BreakingNews/status/742041568069193728
	    392 https://twitter.com/breakingnews/status/742041568069193728
	    341 https://twitter.com/usatoday/status/741998414582415360
	    314 https://twitter.com/injo/status/742042270183100416
	...

## Serial processing

All of these commands can be put together to perform a serial URL extract.  (This means that processing is performed one WARC, one tweet at a time.)

	find_warcs.py 4e1c | xargs twitter_stream_warc_iter.py | python /opt/twarc/utils/unshorten.py  --unshrtn http://unshrtn:3000 | python /opt/twarc/utils/urls.py | grep -v https://twitter.com | sort | uniq -c | sort -rn

However, I never ran this command.  I wanted to take full advantage of the burly server I was running on to do the processing in parallel.

## Parallel processing

Based on some testing with a smaller set of WARC files, I found parallel processing more than 2X as fast.  (This is dependent on the resources of the server; your results may vary.)  Here are the steps for processing in parallel using the unix [parallel](https://www.gnu.org/software/parallel/) utility:

Create list of source files and temporary destination files:

	find_warcs.py 4e1c | tr ' ' '\n' >source.lst
	cat source.lst | xargs basename -a | sed 's/.warc.gz/.txt/' > dest.lst

Extract URLs, unshorten, filter, and sort in parallel.  The output from each WARC is put in a separate temporary destination file.

	parallel -a source.lst -a dest.lst  --xapply “twitter_stream_warc_iter.py {1} | python unshorten.py --unshrtn http://unshrtn:3000 | python /opt/twarc/utils/urls.py | grep -v https://twitter.com | sort > {2}”

Merge the temporary destination files and count:

	cat dest.lst | xargs sort -m | uniq -c | sort -rn

Parallel processing took a little over 3 hours.  Here’s the complete output of 200,094 unique URLs:  [https://gist.github.com/justinlittman/3595b402b5e6c656a1cae6f7ef2edeff](https://gist.github.com/justinlittman/3595b402b5e6c656a1cae6f7ef2edeff)

This work was inspired by Ian Milligan, Nick Ruest, and Jimmy Lin's [“Content Selection and Curation for Web Archiving:
The Gatekeepers vs. the Masses”](http://dl.acm.org/citation.cfm?doid=2910896.2910913). They argue that Twitter data can be mined for seeds for constructing web archives to complement seeds proposed by librarians, archivists, and other “information gatekeepers.”

A few other threads worth pursuing:

* Why is https://trumprally.org/ the top URL (with 33,417 occurrences)?
* Twitter data is rampant with spam.  Can the quality of the URL list be improved by waiting some period of time (one week, a month?) and removing deleted tweets?  My understanding is that Twitter removes spam tweets retroactively.
* For comparison, perform this analysis with [Twarcbase](https://lintool.github.io/warcbase-docs/Spark-Twitter-Analysis/).
