---
layout: article
title: "About"
permalink: /about/
date: 2016-03-26
modified: 2018-05-23
excerpt: "About Social Feed Manager"
image:
  feature:
  teaser: teaser.png
  thumb:
share: false
ads: false
---

{% include toc.html %}

## Contact us

Email: sfm@gwu.edu

Twitter: [@SocialFeedMgr](http://twitter.com/SocialFeedMgr)
 
GitHub: [Report an issue or see current milestone work](https://github.com/gwu-libraries/sfm-ui/issues) 

Members of the [project team]({{ site.github.url }}/about/project-team) speak regularly about SFM at [conferences]({{ site.github.url }}/resources/) and welcome the opportunity to talk in person. 

## About the project and software
Social Feed Manager (SFM) empowers social media researchers, students, and cultural heritage institutions 
to define and collect datasets from social media services. Its development is led by a [project team]({{ site.github.url }}/about/project-team) at [George Washington University Libraries](http://library.gwu.edu), made up of software developers, archivists, and librarians. 

[Overview of Social Feed Manager]({{ site.github.url }}/about/overview)

The Social Feed Manager software aims to achieve the following:

* present an easy-to-use web-based user interface that lets users define collections
comprising sets of targeted accounts, keywords, and other search strategies appropriate to
different social media platforms
* let users authorize SFM to collect data from those accounts, keywords,
and searches on those users' behalf
* use
a set of carefully managed processes to harvest, collect, and store this data, recording its
actions in detail
* make collected information and metadata about harvests available to users,
who may extract, filter, and export these to formats appropriate to their work.

SFM is designed around these key requirements:

* Individual users must be able to create and export collections with a minimum of training and
  staff intervention.
* Staff must be able to install, maintain, and support SFM based on a concise, clear set of
  documentation and automated management tools.
* Developers must be able to add support for additional social media platforms by implementing
  code that follows a concise, clear set of documented design conventions.
* Access to and use of social media data is subject to distinct terms of service offered by each
  platform; SFM will only support methods that fall clearly within these terms of service, such
  as using only supported API methods and respecting API rate limits.

These objectives are not directly supported by SFM:

* SFM is not a primary access, discovery, publishing, dataset hosting/sharing, analysis, or
  archival platform for collected data. It may provide some baseline statistics, summarization,
  and browsing of collections in support of users and staff in defining, assessing, and exporting
  collections, but access, analysis, and long-term storage are complementary to SFM, rather than
  core functions.
* SFM is not a general-purpose web crawling and archiving application; it is complementary to, rather 
  than a substitute for, more established, robust tools like Heritrix.
* SFM is not a "one-click install" application; although its installation is supported through
  automation tools, we assume most who deploy SFM will have some unix system administration
  skills on their team.


## Funding history

* Development of this project has been supported by a grant (#NARDI-14-50017-14) from
  the [National Historical Publications & Records Commission](http://www.archives.gov/nhprc/)
  to George Washington University Libraries from 2014-2017.
* Development of the Sina Weibo harvester was supported by a grant from the [Council on East Asian
  Libraries](http://www.eastasianlib.org/).
* Prior development of SFM under the [previous repository](https://github.com/gwu-libraries/social-feed-manager)
  was supported by a grant (#LG-46-13-0257-13) from the [Institute of Museum and Library Services](http://www.imls.gov/)
  to George Washington University Libraries from 2013-2014.

