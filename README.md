# sfm-ui / Social Feed Manager

[![Build Status](https://travis-ci.org/gwu-libraries/sfm-ui.svg?branch=master)](https://travis-ci.org/gwu-libraries/sfm-ui)

Social Feed Manager (SFM) harvests social media data from multiple platforms' public APIs to help archivists,
librarians, and researchers to build social media collections. [More information about the project itself.](http://gwu-libraries.github.io/sfm-ui)
This is a re-architected version of an [earlier Social Feed Manager](https://github.com/gwu-libraries/social-feed-manager)
which has been in use at GWU Libraries since 2012.

## Overview
Social Feed Manager allows users to:
* define collections comprising sets of targeted accounts, keywords, and other search strategies appropriate to different platforms.
* authorize SFM to harvest data from platforms on the user's behalf.
* view collection information and metadata about harvests.
* extract, filter, and export the datasets to formats appropriate to the user's work.

## Repositories
The full Social Feed Manager is made up of several component repositories:

* [sfm-ui](https://github.com/gwu-libraries/sfm-ui): (this repo) User interface and datastore for collection and harvest information. 
* [sfm-flickr-harvester](https://github.com/gwu-libraries/sfm-flickr-harvester):  A harvester for Flickr.
* [sfm-twitter-harvester](https://github.com/gwu-libraries/sfm-twitter-harvester): A harvester for Twitter.
* [sfm-weibo-harvester](https://github.com/gwu-libraries/sfm-weibo-harvester):   A harvester for Sina Weibo.
* [sfm-tumblr-harvester](https://github.com/gwu-libraries/sfm-tumblr-harvester):   A harvester for Tumblr.
* [sfm-web-harvester](https://github.com/gwu-libraries/sfm-web-harvester):  A harvester for web resources using Heritrix.
* [sfm-utils](https://github.com/gwu-libraries/sfm-utils): Utilities to support SFM.
* [sfm-docker](https://github.com/gwu-libraries/sfm-docker):  Docker configuration for deploying SFM.
* [sfm-elk](https://github.com/gwu-libraries/sfm-elk): Proof-of-concept analytics dashboard using the ELK stack.

## sfm-ui is a Django app which: 

- Provides a user interface to set up Collection Sets, Collections, and Seeds
- Provides Django admin views to administer Credentials, Groups, and other model entities.
- Publishes harvest.start messages for flickr collections.  The app schedules harvest.start messages for publication when the user updates an existing, active Collection.
- Includes a scheduler which uses [apscheduler](http://apscheduler.readthedocs.org) to schedule publication of harvest.start messages.
- Binds to `harvest.status.*(.*)` messages and creates a Harvest object (visible in the admin views) for each harvest status message received.  The message consumer is started via the `startconsumer` management command.

Behind the scenes, SFM uses a set of carefully managed processes to harvest and and store this data, recording its actions in detail.

## Getting started

* Documentation:  [http://sfm.readthedocs.org](http://sfm.readthedocs.org/en/latest/)
* Full project information: [http://gwu-libraries.github.com/sfm-ui](http://gwu-libraries.github.com/sfm-ui)
* Project updates: Follow [@SocialFeedMgr](https://twitter.com/SocialFeedMgr) on Twitter
* Discussion:  [sfm-dev](https://groups.google.com/forum/#!forum/sfm-dev)
* Tickets:  sfm-ui is used for [all ticketing](https://github.com/gwu-libraries/sfm-ui/issues).

Tickets / pull requests / discussion are welcome.

## Unit tests
  `cd sfm`
  
  `./manage.py test --settings=sfm.settings.test_settings`


Social Feed Manager is supported by a grant from the [National Historical Publications & Records Commission](http://www.archives.gov/nhprc/).
