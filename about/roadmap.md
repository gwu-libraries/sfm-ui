---
layout: article
title: "Development Roadmap"
permalink: /about/roadmap
date: 2016-03-29
modified: 2016-03-29
share: false
ads: false
---

(as of February 2016)

## Pre-release 1.0

### Completed development includes:
* Models for collections, seedsets, seeds, credentials, harvests, users, and groups
* Support for harvesting to WARCs
* Harvester: Twitter filter
* Harvester: Twitter search
* Harvester: Flickr user
* Docker deployment
* Schedule and publish harvest request messages
* Update harvest based on harvest response messages
* Initial collection and seedset pages
* Documentation on installation/configuration and development
* Initial documentation on writing a harvester
* Messaging specification for harvesting

### Milestone 0.5
* UI: Complete collection, seedset, seeds pages
* UI: Request export of seedset
* UI: Preliminary credentials pages
* UI: Record and display changes to collections, seedsets, seeds, and credentials (audit log)
* UI: Record and display change notes
* UI: Display basic harvest information (next harvest, last harvest, last status)
* UI: Models for warcs
* UI: Create warc model objects based on warc created messages.
* UI: Expose REST API to allow exporters to query warc model.
* Exporter: Flickr

### Milestone 0.6
* UI: Preliminary terms of service / copyright / fair use notification
* UI: Export notification and retrieval of export by user
* UI: Starting/stopping stream harvests
* Exporter: Twitter
* Documentation: End-user docs
* Documentation: Review technical docs for completeness
* Documentation: Messaging specification for export
* UI: Contextual help
* Harvester: Web (may push to next milestone)

See [1.0 release description]({{ site.github.url }}/1-0-release)

## Post-release 1.0
(ordering is very rough and will likely change)

### Most immediate
* Harvester: Weibo (by July 2016)
* Harvester: Twitter usertimeline and sample stream
* Exporter: Weibo (by Summer 2016)
* UI: Branding
* UI: Validating seeds

### Medium immediate
* UI: Complete terms of service / copyright / fair use notification
* UI: Collection discovery (for future researcher)
* UI: Error handling / display / notification
* UI: Harvest statistics
* Export: Cleanup of export files
* Email updates on harvesting
* UI: Shibboleth integration/auth
* Harvest: Documenting harvest in WarcInfo records (depends on consultant?)
* Export: Export manifest (depends on consultant?)
* Documentation: Complete documentation on writing a harvester, writing an exporter, and adding platform-specific components to UI.

### Less immediate
* Harvester: Tumblr
* Exporter: Tumblr
* Harvester: Flickr additional API methods
* Collection review support
* Fulltext search (in scope?)


