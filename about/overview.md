---
layout: article
title: "Overview of Social Feed Manager"
permalink: /about/overview
date: 2016-06-10
modified: 2016-06-10
excerpt: ""
share: false
ads: false
---

Social Feed Manager is a web application which allows users to create collections of data from social media platforms, 
including Twitter, Flickr, and Sina Weibo. It is open source software and connects to the platforms' public APIs to harvest data.  
In addition to harvesting social media data, it can also harvest web resources such as images and web pages that are linked from the social media.

Researchers, librarians, archivists, and students can use SFM to:


*  Gather datasets tailored to specific research questions
*  Build collections for future research. This might include:
  *  collecting "at risk" social media data around a particular event or topic
  *  filling gaps in special collections
  *  archiving the social media activity of their institution

For both of these cases, SFM documents the steps in collecting in order to support valid, reproducible research and the needs of archives.

Using SFM, an institution can provide social media collecting as a service to members of its community.

Who is Social Feed Manager for?
-------------------------------
SFM is intended for use by researchers, students, librarians, archivists.  It documents the various steps in collecting in order to support valid, reproducible research.

SFM is intended to be run by an institution such as a library, although nothing prevents it from being run by an individual. SFM can manage collections created by many users, across multiple social media platforms.

How might I use SFM?
--------------------
You can use SFM to collect social media data:

### Define and organize collections.

![collection set page with list of collections]({{ site.github.url }}/images/overview/collection_set_multi.png)

### Add collections with various harvest types

![list of collection harvest types]({{ site.github.url }}/images/overview/collection_types.png)

### Add seeds and monitor harvests

![list of seeds]({{ site.github.url }}/images/overview/seeds.png)

![list of harvests]({{ site.github.url }}/images/overview/harvests.png)

### Turn it on.  SFM will harvest the data on an on-going basis or according to the schedule you specify.

![collection turned on]({{ site.github.url }}/images/overview/collection.png)

### To make use of social media data:

Export a collection to a spreadsheet.

![export create screen]({{ site.github.url }}/images/overview/export_page.png)

![spreadsheet screenshot]({{ site.github.url }}/images/overview/excel.png)

*  Feed data into your own processing pipeline.
*  Explore data with Elasticsearch/Logstash/Kibana (ELK).

![Kibana]({{ site.github.url }}/images/overview/kibana.png)

What sort of expertise is needed to use SFM?
--------------------------------------------
No specific expertise is needed to use SFM, but it is helpful to read the SFM documentation and be familiar with social media APIs.

What sort of technical expertise is needed to get SFM running?
--------------------------------------------------------------
SFM requires some level of expertise to run.  Instructions are providing for running in any environment that supports Docker.  Instructions are also provided for Amazon Web Services (AWS).

What is the state of the software?
----------------------------------
The first version of SFM was released in June 2016.  While it is suitable for production, it should be considered immature.  Development is active and ongoing.


Social Feed Manager is supported by a grant from the National Historical Publications & Records Commission. 
