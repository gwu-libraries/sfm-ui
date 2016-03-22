# sfm-ui

[![Build Status](https://travis-ci.org/gwu-libraries/sfm-ui.svg?branch=master)](https://travis-ci.org/gwu-libraries/sfm-ui)

The [new] Social Feed Manager user interface application.

sfm-ui provides a Django app which:

- Allows login with app-local credentials.
- Provides UI interface to set up Collections, Seed Sets, and Seeds
- Provides Django admin views to administer Credentials, Groups, and other model entities.
- Publishes harvest.start messages for flickr SeedSets.  The app schedules harvest.start messages for publication when the user updates an existing, active SeedSet.
- Includes a scheduler which uses [apscheduler](http://apscheduler.readthedocs.org) to schedule publication of harvest.start messages.
- Binds to `harvest.status.*(.*)` messages and creates a Harvest object (visible in the admin views) for each harvest status message received.  The message consumer is started via the `startconsumer` management command.

## Unit tests

     cd sfm
    ./manage.py test --settings=sfm.settings.test_settings

# Social Feed Manager

## Objectives

Social Feed Manager (SFM) empowers social media researchers, students, archivists, librarians, and others to define and collect datasets from social media services. To support this work, SFM presents an easy-to-use, web-based user interface that lets users:

* define collections comprising sets of targeted accounts, keywords, and other search strategies appropriate to different platforms.
* authorize SFM to harvest data from platforms on the user's behalf.
* view collection information and metadata about harvests.
* extract, filter, and export the datasets to formats appropriate to the user's work.

Behind the scenes, SFM uses a set of carefully managed processes to harvest and and store this data, recording its actions in detail.

## Components

* [sfm-ui](https://github.com/gwu-libraries/sfm-ui):  User interface and datastore for collection and harvest information.
* [sfm-flickr-harvester](https://github.com/gwu-libraries/sfm-flickr-harvester):  A harvester for Flickr.
* [sfm-twitter-harvester](https://github.com/gwu-libraries/sfm-twitter-harvester): A harvester for Twitter.
* [sfm-utils](https://github.com/gwu-libraries/sfm-utils): Utilities to support SFM.
* [sfm-docker](https://github.com/gwu-libraries/sfm-docker):  Docker configuration for deploying SFM.
* [sfm-web-harvester](https://github.com/gwu-libraries/sfm-web-harvester):  A harvester for web resources using Heritrix.
* [sfm-weibo-harvester](https://github.com/gwu-libraries/sfm-weibo-harvester):   A harvester for Sina Weibo. 

## Getting started

* Documentation:  [sfm.readthedocs.org](http://sfm.readthedocs.org/en/latest/)
* Discussion:  [sfm-dev](https://groups.google.com/forum/#!forum/sfm-dev)
* Tickets:  sfm-ui is used for [all ticketing](https://github.com/gwu-libraries/sfm-ui/issues).

Tickets / pull requests / discussion are welcome.
