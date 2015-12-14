# sfm-ui

The [new] Social Feed Manager user interface application.

sfm-ui provides a Django app which:

- Allows login with app-local credentials.
- Provides UI interface to set up Collections, Seed Sets, and Seeds
- Provides Django admin views to administer Credentials, Groups, and other model entities.
- Publishes harvest.start messages for flickr SeedSets.  The app schedules harvest.start messages for publication when the user updates an existing, active SeedSet.
- Includes a scheduler which uses [apscheduler](http://apscheduler.readthedocs.org) to schedule publication of harvest.start messages.
- Binds to `harvest.status.*(.*)` messages and creates a Harvest object (visible in the admin views) for each harvest status message received.  The message consumer is started via the `startconsumer` management command.
