---
layout: article
title: "Development Roadmap"
permalink: /about/roadmap
date: 2016-03-29
modified: 2016-03-29
share: false
ads: false
---

(as of May 2016)

## Pre-release 1.0
(see [milestone release notes](https://github.com/gwu-libraries/sfm-ui/releases))

### Completed development, up through milestone 0.6.0, includes:
* Models for collections, seedsets, seeds, credentials, harvests, users, and groups
* Support for harvesting to WARCs
* Harvester: Twitter filter
* Harvester: Twitter search
* Harvester: Twitter usertimeline and sample stream
* Harvester: Flickr user
* Harvester: Web 
* Harvester: Sina Weibo
* Docker deployment
* Schedule and publish harvest request messages
* Update harvest based on harvest response messages
* Initial collection and seedset pages
* Messaging specification for harvesting
* UI: Complete collection, seedset, seeds pages
* UI: Request export of seedset
* UI: Preliminary credentials pages
* UI: Record and display changes to collections, seedsets, seeds, and credentials (audit log)
* UI: Record and display change notes
* UI: Display basic harvest information (next harvest, last harvest, last status)
* UI: Models for warcs
* UI: Create warc model objects based on warc created messages.
* UI: Expose REST API to allow exporters to query warc model.
* UI: Preliminary terms of service / copyright / fair use notification
* UI: Export notification and retrieval of export by user
* UI: Starting/stopping stream harvests
* UI: Basic harvest statistics
* Exporter: Twitter
* Exporter: Flickr
* Exporter: Weibo
* Documentation on installation/configuration and development
* Documentation: Messaging specification for export
* Initial documentation on writing a harvester

### Milestone 0.6.1
* Changing naming of Collection and SeedSet to Collection Set and Collection. This terminology better describes harvesters that do not require seeds, such as 
 the Twitter sample stream and filter stream.

### Milestone 0.6.2
* UI: General improvements to screens and workflow
* UI: Preliminary terms of service / copyright / fair use notification
* UI: Contextual help
* Documentation: End-user docs
* Documentation: Review technical docs for completeness

See [1.0 release description]({{ site.github.url }}/about/1-0-release)

## Post-release 1.0
(ordering is very rough and will likely change)

### Most immediate
* UI: Branding
* UI: Validating seeds

### Medium immediate
* UI: Complete terms of service / copyright / fair use notification
* UI: Collection discovery (for future researcher)
* UI: Error handling / display / notification
* UI: Refine harvest statistics
* Export: Cleanup of export files
* Email updates on harvesting
* UI: Shibboleth integration/auth
* Harvest: Documenting harvest in WarcInfo records 
* Export: Export manifest 
* Documentation: Complete documentation on writing a harvester, writing an exporter, and adding platform-specific components to UI.

### Less immediate
* Harvester: Tumblr
* Exporter: Tumblr
* Harvester: Flickr additional API methods
* Collection review support
* Fulltext search (in scope?)


