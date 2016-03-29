---
layout: article
title: "1.0 Release Description"
permalink: /about/1-0-release
date: 2016-03-29
modified: 2016-03-29
share: false
ads: false
---

## 1.0 should include:

### Harvesters from two platforms
* twitter-filter
* twitter-search 
* flickr-user

### Data models
* Models for collections, seedsets, seeds, credentials, harvests, users, and groups
* Models for warcs

### User interface for creating collections
* Create a collection, define a seedset, define seeds
* Preliminary credentials pages, non-platform-specific (enter JSON; more information via help)
* Display basic harvest information (next harvest, last harvest, last status)
* Start and stop stream collection 

### Exporting collected data
* Request export of seedsets from Twitter and Flickr (minimal parameters)
* Notification of export availability and ability to retrieve
* Create warc model objects based on warc created messages.
* Expose REST API to allow exporters to query warc model.
* Basic Terms of Service notification with export

### Audit/Change log
* Infrastructure to record changes initiated by user
* Record and display changes to collections, seedsets, seeds, and credentials
* Record and display notes about changes entered by collection builder

### Documentation
* End-user documentation (http://sfm.readthedocs.org)
* Technical documentation for installation and use
* In-app contextual help (basic)
