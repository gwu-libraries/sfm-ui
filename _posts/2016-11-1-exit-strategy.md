---
layout: article
permalink: /posts/2016-11-1-exit-strategy
title: "Your SFM (content) exit strategy"
author: justin_littman 
excerpt: "This blog post describes how to get your content OUT of SFM."
---

![Tweet from Spellbound Blog]({{ site.github.url }}/images/exit-strategy/tweet.png)

[https://twitter.com/spellboundblog/status/791273073722945537](https://twitter.com/spellboundblog/status/791273073722945537)

This blog post describes how to get your content OUT of SFM.  While there are an assortment of reasons for doing this, probably the two most prominent are (1) wanting to move the content into a preservation or repository environment or (2) wanting to move it between SFM instances.

To be clear, SFM is not intended to be a preservation or repository system.  Further, we fully expect that the content collected with SFM will outlive the SFM software.  (Let’s be honest: software comes and goes.)  Thus, supporting an exit strategy is a fundamental feature of SFM.  Further, it aligns well with our focus on recording the provenance of the collected social media data.  (See our working paper, [Provenance of a Tweet](https://scholarspace.library.gwu.edu/files/h128nd689)).


And to further clarify, in this post we are not talking about a user [exporting a social media dataset to a spreadsheet / structured text](http://sfm.readthedocs.io/en/latest/quickstart.html#exports) or [from the command line](http://sfm.readthedocs.io/en/latest/processing.html).  This is currently supported by SFM, and we are planning to do [further work on providing an export manifest](https://github.com/gwu-libraries/sfm-ui/issues/123) containing provenance metadata aimed at the researcher wanting documentation on the dataset.  Rather, the subject of this post is how an administrator might move an entire collection of social media data.

Getting your content out of SFM is simple:

    cp -r /sfm-data/collection_set/* <your destination>.


That is, all you need to do is copy the files on disk.

This example shows copying all of the collection sets for an SFM instance. You can also copy individual collection sets or collections. The directory structure is `/sfm-data/collection_set/<collection set id>/<collection ids>`, e.g., `/sfm-data/collection_set/d7c2dc6e9675467d9d19b3f06e0c2f60/d29f5630c9184b6486197647c4dc0529`.  (The collection set and collection ids are UUIDs.)

This is possible because each collection directory contains all of the data and metadata for the collection; that is, a collection is portable.

Let’s consider what you’ll find in a collection directory.  First, you will find WARC files for the harvested social media and web resources.  These are arranged hierarchically by date, e.g., `2016/10/28/14/
437dd76ff71a4fe685f7f0e0270e5291-20161028140713894-00000-64-d57f4363ab4a-8000.warc.gz`.

Second, you find a records directory.  This contains JSON serializations of the database records for:  the collection; the collection set that the collection is part of; the collection’s seeds, harvests, and WARCs; and any associated users, groups, and credentials.  It also contains JSON serializations of the database records for the history of changes to the collection, collection set, seeds, and credentials.  (These are the files below prefixed with historical_.)  Here’s the list of the files you’ll find in the records directory of a collection:

* collection_set.json
* info.json
* warcs.json
* historical_seeds.json
* users.json
* harvest_stats.json
* collection.json
* groups.json
* seeds.json
* historical_collection.json
* historical_credentials.json
* credentials.json
* historical_collection_set.json
* harvests.json


And here’s an example of the JSON serialization of the collection record:

	[
	{
	    "fields": {
	        "credential": [
	            "16d7433e612843ad87a4cca4cc8a3461"
	        ],
	        "harvest_type": "twitter_user_timeline",
	        "description": "Twitter user timelines from Democratic candidates and the Democratic Party. These are official accounts only.",
	        "end_date": null,
	        "date_updated": "2016-10-29T01:52:21.281Z",
	        "collection_set": [
	            "997d3ed7e8f047b6a35384c8a951fc90"
	        ],
	        "is_active": true,
	        "history_note": "",
	        "schedule_minutes": 10080,
	        "harvest_options": "{\"media\": false, \"incremental\": true, \"web_resources\": false}",
	        "date_added": "2016-10-29T01:51:46.986Z",
	        "collection_id": "3a4beac3f2ce4cd3be5c43c2a9e8a766",
	        "name": "Democratic user timelines"
	    },
	    "model": "ui.collection"
	}
	]

Notice that these records are fairly self-explanatory and map clearly to [the SFM code](https://github.com/gwu-libraries/sfm-ui/blob/master/sfm/ui/models.py). However, they definitely would benefit from additional documentation.

These records are updated on a nightly basis, though an update can also be triggered using a management command.

Lastly, you’ll find a README file.  Here’s an example README for a collection:

	This is a collection created with Social Feed Manager.

	Collection name: Democratic user timelines
	Collection id: 3a4beac3f2ce4cd3be5c43c2a9e8a766
	Harvest type: Twitter user timeline
	Collection description: Twitter user timelines from Democratic candidates and the Democratic Party. These are official accounts only.

	This collection is part of collection set 2016 Election (collection set id 997d3ed7e8f047b6a35384c8a951fc90).

	JSON records that fully describe this collection and its contents can be found in the records directory. These records
	can be used to import the collection into Social Feed Manager.

	WARC files are located in subdirectories of this directory, organized by date.

	Updated on Oct. 29, 2016, 1:59 a.m.


There is also a README for the collection set, located in the collection set directory.  Here’s an example:

	This is a collection set created with Social Feed Manager.

	Collection set name: 2016 Election
	Collection set id: 997d3ed7e8f047b6a35384c8a951fc90
	Collection set description: Social media around the 2016 U.S. presidential election, including the primary.

	This collection set contains the following collections:
	* Republican user timelines (collection id 00f7ff2c35334418aa5b417b9a69c87c)
	* Democratic user timelines (collection id 3a4beac3f2ce4cd3be5c43c2a9e8a766)

	Each of these collections contains a README.txt.

	Updated on Oct. 29, 2016, 1:59 a.m.

As previously mentioned, one of the intended uses of collection portability is to support moving collections between SFM instances. To move a collection, all you need to do is move the files and issue a management command on the destination SFM instance.  The records will be loaded into the database and the collection will be fully available from the destination SFM instance.  All of the data and metadata will be entirely intact.

This feature is forthcoming in [version 1.3](https://github.com/gwu-libraries/sfm-ui/milestone/14). In the meantime, you can read the [documentation](http://sfm.readthedocs.io/en/latest/portability.html) and give us your feedback on this exit strategy.

![Tweet from agoodlibrarian]({{ site.github.url }}/images/exit-strategy/tweet2.png)

[https://twitter.com/agoodlibrarian/status/793141902061084672](https://twitter.com/agoodlibrarian/status/793141902061084672)