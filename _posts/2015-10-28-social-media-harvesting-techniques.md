---
layout: article
permalink: /posts/social-media-harvesting-techniques/
title: "Social Media Harvesting Techniques"
author: justin_littman
---

[Social Feed Manager](http://go.gwu.edu/sfm) (SFM) is a tool developed by the Scholarly Technology Group for harvesting social media to support research and build archives. As part of enhancements to SFM being performed under a grant from the [National Historical Publications and Records Commission](http://www.archives.gov/nhprc/) (NHPRC), we are adding support for writing social media to [Web ARChive](https://en.wikipedia.org/wiki/Web_ARChive) (WARC) files. Using WARCs is part of our strategy of more closely aligning social media harvesting with web harvesting. (This bears further discussion; more on this coming.) This blog entry describes two techniques for retrieving social media records from the application programming interfaces (APIs) of social media platforms and writing to WARCs. These techniques are based on Python, though these or similar approaches are applicable to other programming languages.

## Background on social media APIs

Many social media platforms provide APIs to allow retrieval of social media records. Examples of such APIs include the [Twitter REST API](https://dev.twitter.com/rest/public), the [Flickr API](https://www.flickr.com/services/api/), and the [Tumblr API](https://www.tumblr.com/docs/en/api/v2). These APIs use HTTP as the communications protocol and provide the records in a machine readable formats such as JSON. Compared to harvesting HTML from the social media platform’s website, harvesting social media from APIs offers some advantages:

* The APIs are more stable. The creators of the APIs understand that when they change the API, they will be breaking consumers of the API. (Want notification when an API changes? Give [API Changelog](https://www.apichangelog.com/) a try.)
* The APIs provide social media records in formats that are intended for machine processing.
* The APIs sometimes provide access to data that is not available from the platform’s website. For example, the following shows the record for a tweet retrieved fro	m Twitter’s REST API:

		{
	    "created_at": "Tue Jun 02 13:22:55 +0000 2015",
	    "id": 605726286741434400,
		    "id_str": "605726286741434368",
		    "text": "At LC for @archemail today:  Thinking about overlap between email archiving, web archiving, and social media archiving.",
		    "source": "Twitter Web Client",
		    "truncated": false,
		    "in_reply_to_status_id": null,
		    "in_reply_to_status_id_str": null,
		    "in_reply_to_user_id": null,
		    "in_reply_to_user_id_str": null,
		    "in_reply_to_screen_name": null,
		    "user": {
		        "id": 481186914,
		        "id_str": "481186914",
		        "name": "Justin Littman",
		        "screen_name": "justin_littman",
		        "location": "",
		        "description": "",
		        "url": null,
		        "entities": {
		            "description": {
		                "urls": []
			            }
			        },
		        "protected": false,
		        "followers_count": 45,
		        "friends_count": 47,
		        "listed_count": 5,
		        "created_at": "Thu Feb 02 12:19:18 +0000 2012",
		        "favourites_count": 34,
		        "utc_offset": -14400,
		        "time_zone": "Eastern Time (US & Canada)",
		        "geo_enabled": true,
		        "verified": false,
		        "statuses_count": 72,
		        "lang": "en",
		        "contributors_enabled": false,
		        "is_translator": false,
		        "is_translation_enabled": false,
		        "profile_background_color": "C0DEED",
		        "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png",
		        "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png",
		        "profile_background_tile": false,
		        "profile_image_url": "http://pbs.twimg.com/profile_images/496478011533713408/GjecBUNj_normal.jpeg",
		        "profile_image_url_https": "https://pbs.twimg.com/profile_images/496478011533713408/GjecBUNj_normal.jpeg",
		        "profile_link_color": "0084B4",
		        "profile_sidebar_border_color": "C0DEED",
		        "profile_sidebar_fill_color": "DDEEF6",
		        "profile_text_color": "333333",
		        "profile_use_background_image": true,
		        "has_extended_profile": false,
		        "default_profile": true,
		        "default_profile_image": false,
		        "following": false,
		        "follow_request_sent": false,
		        "notifications": false
			    },
		    "geo": null,
		    "coordinates": null,
		    "place": {
		        "id": "01fbe706f872cb32",
		        "url": "https://api.twitter.com/1.1/geo/id/01fbe706f872cb32.json",
		        "place_type": "city",
		        "name": "Washington",
		        "full_name": "Washington, DC",
		        "country_code": "US",
		        "country": "United States",
		        "contained_within": [],
		        "bounding_box": {
		            "type": "Polygon",
		            "coordinates": [
			                [
			                    [
		                        -77.119401,
		                        38.801826
			                    ],
			                    [
		                        -76.909396,
		                        38.801826
			                    ],
			                    [
		                        -76.909396,
		                        38.9953797
			                    ],
			                    [
		                        -77.119401,
		                        38.9953797
			                    ]
			                ]
			            ]
			        },
		        "attributes": {}
			    },
		    "contributors": null,
		    "is_quote_status": false,
		    "retweet_count": 0,
		    "favorite_count": 0,
		    "entities": {
		        "hashtags": [],
		        "symbols": [],
		        "user_mentions": [],
		        "urls": []
			    },
		    "favorited": false,
		    "retweeted": false,
		    "lang": "en"
			}

and how the same tweet appears on Twitter’s website:

![A sample tweet](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202015-10-14%20at%201.37.53%20PM.png)

It is worth emphasizing that retrieving social media records from an API are just HTTP transactions, just like the HTTP transactions between a web browser and a website or a web crawler and a website.

(The one exception worth noting is [Twitter’s Streaming APIs](https://dev.twitter.com/streaming/overview). While these APIs do use HTTP, the HTTP connection is kept open while additional data is added to the HTTP response over a long period of time. Thus, this API is unique in that the HTTP response may last for minutes, hours, or days rather than the normal milliseconds or seconds and the HTTP response may be significantly larger in size than the typical HTTP response from a social media API. This will require special handling and is outside the scope for this discussion, though ultimately requires consideration.)
 
To simplify interacting with social media APIs, developers have created API libraries. An API library is for a specific programming language and social media platform and makes it easier to interact with the API by handling authentication, rate limiting, HTTP communication, and other low-level details. In turn, API libraries use other libraries such as an HTTP client for HTTP communication or an OAuth library for authentication. Examples of Python API libraries include [Twarc](https://github.com/edsu/twarc) or [Tweepy](http://www.tweepy.org/) for Twitter, [Python Flickr API Kit](https://stuvel.eu/flickrapi) for Flickr, and [PyTumblr](https://github.com/tumblr/pytumblr) for Tumblr. Rather than having to re-implement all of these low-level details, ideally a social media harvester will use existing API libraries.
 
## Background on WARCs

WARCs allow for recording an entire HTTP transaction between an HTTP client and an HTTP server. A typical transaction consists of the client issuing a request message and the server replying with a response message. These are recorded in the WARC as a request record and response record pair. In a WARC, each record is composed of a record header containing some named metadata fields and a record body containing the HTTP message. In turn, each HTTP message is composed of a message header and a message body. Here is an example request record for GWU’s homepage:
 
		WARC/1.0
		WARC-Type: request
		Content-Type: application/http;msgtype=request
		WARC-Date: 2015-10-14T18:01:10Z
		WARC-Record-ID: 
		WARC-Target-URI: http://www.gwu.edu/
		WARC-IP-Address: 128.164.1.16
		WARC-Block-Digest: sha1:A7SJCNM5DLPJCLQMGJOXD7XDWWFQRDGH
		WARC-Payload-Digest: sha1:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ
		Content-Length: 69
		WARC-Warcinfo-ID: 

		GET / HTTP/1.1
		User-Agent: Wpull/1.2.1 (gzip)
		Host: www.gwu.edu

and a response record:

		WARC/1.0
		WARC-Type: response
		Content-Type: application/http;msgtype=response
		WARC-Date: 2015-10-14T18:01:10Z
		WARC-Record-ID: 
		WARC-Target-URI: http://www.gwu.edu/
		WARC-IP-Address: 128.164.1.16
		WARC-Concurrent-To: 
		WARC-Block-Digest: sha1:FAGHJPTSB4TIHWBMNPAIXM6IRS7EMOHS
		WARC-Payload-Digest: sha1:D2OLR4C4UASIRNSGJCNQMK5XBQ6RAWGV
		Content-Length: 79609
		WARC-Warcinfo-ID: 

		HTTP/1.1 200 OK
		Server: Apache/2.2.15 (Oracle)
		X-Powered-By: PHP/5.3.3
		Expires: Sun, 19 Nov 1978 05:00:00 GMT
		Last-Modified: Wed, 14 Oct 2015 03:33:00 GMT
		Cache-Control: no-cache, must-revalidate, post-check=0, pre-check=0
		ETag: "1444793580"
		Content-Language: en
		X-Generator: Drupal 7 (http://drupal.org)
		Link: ; rel="image_src",; rel="canonical",; rel="shortlink"
		Content-Type: text/html; charset=utf-8
		Transfer-Encoding: chunked
		Date: Wed, 14 Oct 2015 18:01:11 GMT
		X-Varnish: 982060864 981086065
		Age: 52090
		Via: 1.1 varnish
		Connection: keep-alive
		X-Cache: Hit from web1
		Set-Cookie: NSC_dnt_qspe_tey_80=ffffffff83ac15c345525d5f4f58455e445a4a423660;expires=Wed, 14-Oct-2015 18:31:11 GMT;path=/;httponly

		b3a
		<!DOCTYPE html>
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" version="XHTML+RDFa 1.0" dir="ltr"
		  xmlns:og="http://ogp.me/ns#"
		  xmlns:fb="http://www.facebook.com/2008/fbml"
		  xmlns:content="http://purl.org/rss/1.0/modules/content/"
		  xmlns:dc="http://purl.org/dc/terms/"
		  xmlns:foaf="http://xmlns.com/foaf/0.1/"
		  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
		  xmlns:sioc="http://rdfs.org/sioc/ns#"
		  xmlns:sioct="http://rdfs.org/sioc/types#"
		  xmlns:skos="http://www.w3.org/2004/02/skos/core#"
		  xmlns:xsd="http://www.w3.org/2001/XMLSchema#">

		<head profile="http://www.w3.org/1999/xhtml/vocab">
		<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
		  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		[A whole bunch of HTML skipped here]
		</body>
		</html>

(This was recorded using [Wpull](https://github.com/chfoo/wpull): `wpull http://www.gwu.edu --warc-file warc_example --no-warc-compression`)

Putting together this discussion of social media APIs and WARCs, we'll describe techniques for harvesting social media records using existing API libraries and record the HTTP transactions in WARCs.

## The first technique

The first technique is to attempt to record the HTTP transaction as handled by the HTTP client used by the API library. While there are a number of higher-level clients in Python (e.g., [requests](http://docs.python-requests.org/en/latest/)), the underlying HTTP protocol client is generally httplib. Unfortunately, httplib does not provide ready access to the entire HTTP message, just the message body. However, when the debug level of httplib is set to 1, httplib writes the message header to standard output (stdout). For example:

		>>> import httplib
		>>> conn = httplib.HTTPConnection("www.gwu.edu")
		>>> conn.set_debuglevel(1)
		>>> conn.request("GET", "/")
		send: 'GET / HTTP/1.1\r\nHost: www.gwu.edu\r\nAccept-Encoding: identity\r\n\r\n'
		>>> resp = conn.getresponse()
		reply: 'HTTP/1.1 200 OK\r\n'
		header: Server: Apache/2.2.15 (Oracle)
		header: X-Powered-By: PHP/5.3.3
		header: Expires: Sun, 19 Nov 1978 05:00:00 GMT
		header: Last-Modified: Wed, 14 Oct 2015 03:33:00 GMT
		header: Cache-Control: no-cache, must-revalidate, post-check=0, pre-check=0
		header: ETag: "1444793580"
		header: Content-Language: en
		header: X-Generator: Drupal 7 (http://drupal.org)
		header: Link: ; rel="image_src",; rel="canonical",; rel="shortlink"
		header: Content-Type: text/html; charset=utf-8
		header: Transfer-Encoding: chunked
		header: Date: Wed, 14 Oct 2015 18:16:54 GMT
		header: X-Varnish: 982091814 981086065
		header: Age: 53034
		header: Via: 1.1 varnish
		header: Connection: keep-alive
		header: X-Cache: Hit from web1
		header: Set-Cookie: NSC_dnt_qspe_tey_80=ffffffff83ac15c345525d5f4f58455e445a4a423660;expires=Wed, 14-Oct-2015 18:46:54 GMT;path=/;httponly

By capturing this debugging output, the HTTP message can be reconstructed and recorded in the appropriate WARC records. We use Internet Archive’s [WARC library](https://github.com/internetarchive/warc) for writing to WARCs. Here’s a gist showing some code that uses the Python Flickr API Kit to retrieve the record for a photo from Flickr’s API and record in a WARC: [https://gist.github.com/justinlittman/a46ab82f456423a71e39](https://gist.github.com/justinlittman/a46ab82f456423a71e39). (The resulting WARC is also provided in the gist.)

Advantages of this technique:

* Complete control over writing the WARC, including WARC record headers and deduplication strategy.

Disadvantages of this technique:

* Reconstructs the HTTP message instead of recording directly as passed over the network.
* Fragile, since depends on debugging output of httplib. There is no guarantee that this debugging output will remain unchanged in the future.
* Often requires hacking the API library to get access to the HTTP client.

## The second technique

The second approach was suggested by [Ed Summers](http://inkdroid.org/). In this approach, an HTTP proxy records the HTTP transaction. In a proxying setup, the HTTP client makes its request to the proxy. The proxy in turn relays the request to the HTTP server. It receives the response from the server and relays it back to the client. By acting as a “man in the middle”, the proxy has access to the entire HTTP transaction.

Internet Archive’s [warcprox](https://github.com/internetarchive/warcprox) is an HTTP proxy that writes the recorded HTTP transactions to WARCs. Among other applications, warcprox is used in Ilya Kreymer’s [webrecorder.io](https://webrecorder.io/), which records the HTTP transactions from a user browsing the web. In our case, warcprox will record the HTTP transactions between the API library and the social media platform’s server.

This gist demonstrates using the Python Flickr API Kit to retrieve the record for a photo from Flickr’s API and recording it using warcprox: [https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed
](https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed)

Advantages:

* Records the HTTP transaction directly without having to reconstruct it. (As evidence of this look at [https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed#file-technique2-warc-L40](https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed#file-technique2-warc-L40). That gobbledygook is the gzipped HTTP message body, which should be expected because the Content-Encoding header is given as “gzip” at [https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed#file-technique2-warc-L34](https://gist.github.com/justinlittman/0b3d76ca0465a9d914ed#file-technique2-warc-L34).)
* Can be used with social media harvesters written in any language, not just Python.

Disadvantages:

* Depends on the API library supporting the configuration of a proxy or requires hacking the API library to get access to the HTTP client to configure proxying.
* Does not provide control over the WARC, especially the ability to write WARC record headers. (WARC record headers allow storing additional metadata in the WARC.)
* Requires running proxy as a separate process from the harvester.

STG is continuing to experiment with and refine these two approaches. Thoughts on these approaches or suggestions for other techniques would be appreciated and we welcome any [discussion](https://groups.google.com/forum/#!forum/sfm-dev) of social media harvesting in general.

(This post was originally posted on the [Scholarly Technology Group's blog](https://library.gwu.edu/scholarly-technology-group/posts/social-media-harvesting-techniques) on the GW Libraries website.) 
