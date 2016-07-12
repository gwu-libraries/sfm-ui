---
layout: article
title: "Development Roadmap"
permalink: /about/roadmap
date: 2016-03-29
modified: 2016-07-05
share: false
ads: false
---

The current version of Social Feed Manager is 1.0. [Release description]({{ site.github.url }}/about/1-0-release)

(ordering is very rough and will likely change)

### Milestone 1.1 [(full list of tickets on GitHub)](https://github.com/gwu-libraries/sfm-ui/milestones/1.next)
* Improve monitoring of components, including harvests [(Ticket #303)](https://github.com/gwu-libraries/sfm-ui/issues/303)
* UI: general usability improvements and contextual help
* UI: Improve warnings / notifications about seeds, harvests, and exports problems [(Ticket #357](https://github.com/gwu-libraries/sfm-ui/issues/357), [#303)](https://github.com/gwu-libraries/sfm-ui/issues/303)
* UI: Basic branding [(Ticket #257)](https://github.com/gwu-libraries/sfm-ui/issues/257)
* UI: Allow multiple credentials per platform [(Ticket #317)](https://github.com/gwu-libraries/sfm-ui/issues/317)
* UI: Clearer harvest statistics
* Bug fixes for 1.0
* Documentation improvements
* Improvements to export speed
* Harvester: Tumblr
* Exporter: Tumblr

### Future work, medium immediate
* UI: Further branding options
* UI: Refine terms of service / copyright / fair use notifications
* UI: Collection discovery (for future researcher)
* UI: Further improve error handling / display / notification
* Export: Cleanup of export files
* Email updates on harvesting [(Ticket #368)](https://github.com/gwu-libraries/sfm-ui/issues/368)
* UI: Shibboleth integration/auth [(Ticket #31)](https://github.com/gwu-libraries/sfm-ui/issues/31)
* Harvest: Documenting harvest in WarcInfo records 
* Export: Export manifest [(Ticket #123)](https://github.com/gwu-libraries/sfm-ui/issues/123)
* Documentation: Complete documentation on writing a harvester, writing an exporter, and adding platform-specific components to UI.

### Less immediate
* Harvester: Flickr additional API methods
* Collection review support
* Fulltext search (in scope?)
* Improvements to ELK
* Public page showing collection information

### Completed development, up through 1.0 includes:
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
* UI: General improvements to screens and workflow
* UI: Preliminary terms of service / copyright / fair use notification
* Documentation: End-user docs
* Documentation: Review technical docs for completeness

