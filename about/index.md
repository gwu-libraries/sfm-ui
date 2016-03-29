---
layout: article
title: "About"
permalink: /about/
date: 2016-03-26
modified: 2016-03-26
excerpt: "About Social Feed Manager"
image:
  feature:
  teaser: teaser.png
  thumb:
share: false
ads: false
---

Social Feed Manager (SFM) empowers social media researchers, students, and cultural heritage institutions 
to define and collect datasets from social media services. Its development is led by a team at [George Washington University Libraries](http://library.gwu.edu), made up of software developers, archivists, and librarians. 

In 2015, we re-evaluated the services and function we had been offering for several years with the [earlier version of SFM](http://social-feed-manager.readthedocs.org) and are focusing our efforts on reshaping the app to meet the needs of use cases we've experienced and anticipate in the future. We are currently re-architecting SFM to support multiple social media platforms and allow users to build collections without the mediation of a librarian or archivist.                                                                                                       

[Project Scope and Objectives](#scope)

[User Stories](/about/user-stories)

[Development Roadmap](/about/roadmap)

[1.0 Release description](/about/1-0-release)

[Project Team](/about/project-team)


## <a name="scope"></a>Project Scope

### Objectives

Social Feed Manager (SFM) empowers social media researchers, students, archivists, librarians,
and others to define and collect datasets from social media services. To support this work,
SFM:

* presents an easy-to-use web-based user interface that lets users define collections
comprising sets of targeted accounts, keywords, and other search strategies appropriate to
different platforms
* lets users authorize SFM to collect data from those accounts, keywords,
searches, and related web resources on those users' behalf
* uses
a set of carefully managed processes to crawl, collect, and store this data, recording its
actions in detail
* makes collected information and metadata about crawls available to users,
who may extract, filter, and export these to formats appropriate to their work.


### Requirements

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


### Out of scope

These objectives are not directly supported by SFM:

* SFM is not a primary access, discovery, publishing, dataset hosting/sharing, analysis, or
  archival platform for collected data. It may provide some baseline statistics, summarization,
  and browsing of collections in support of users and staff in defining, assessing, and exporting
  collections, but access, analysis, and long-term storage are complementary to sfm, rather than
  core functions.
* SFM is not a general-purpose web crawling and archiving application; although it may support
  direct capture of web pages and sites, it is complementary to, rather than a substitute for,
  more established, robust tools like Heritrix.
* SFM is not a "one-click install" application; although its installation is supported through
  automation tools, we assume most who deploy SFM will have some unix system administration
  skills on their team.


### Funding history

* Development of this project has been supported by a grant (#NARDI-14-50017-14) from
  the [National Historical Publications & Records Commission](http://www.archives.gov/nhprc/)
  to George Washington University Libraries from 2014-2017.
* Development of the Sina Weibo harvester is supported by a grant from the [Council on East Asian
  Libraries](http://www.eastasianlib.org/).
* Prior development of SFM under the [previous repository](https://github.com/gwu-libraries/social-feed-manager)
  was supported by a grant (#LG-46-13-0257-13) from the [Institute of Museum and Library Services](http://www.imls.gov/)
  to George Washington University Libraries from 2013-2014.
