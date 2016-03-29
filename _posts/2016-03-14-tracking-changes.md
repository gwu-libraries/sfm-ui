---
layout: article
permalink: /posts/2016-03-14-tracking-changes
title: "Tracking Changes to Harvests in Social Feed Manager"
author: justin_littman 
excerpt: "In her blog post, “Social Media for Good: the Series, Episode 2”, DPC’s Sara Day Thomson explains:
New work also reveals the heightened importance of archived social media datasets that make it possible for researchers to re-use data. In order for this data to be useful..."
---

In her blog post, “Social Media for Good: the Series, Episode 2”, DPC’s Sara Day Thomson explains:

> New work also reveals the heightened importance of archived social media datasets that make it possible for researchers to re-use data. 
> In order for this data to be useful, it must be curated and preserved with sufficient metadata to explain the conditions of its original 
> capture and any subsequent actions taken to refine the data. For instance, a researcher may remove a particular hashtag or account as a 
> study progresses, changing the resulting dataset. Archivists face a new mandate to develop tools and practices that support these conditions for re-use and reproducibility.

The Social Feed Manager team has heard this loud and clear!  The need to keep track of changes to collection criteria (seeds, harvesting options, credentials, etc.) is reflected in our user stories for the new Social Feed Manager and initial support should be included in our next release (version 0.5.0).  You can follow progress by watching the ticket.  (Keep in mind that we are still pre-version 1.0, so SFM is in active development.)

We haven’t work on the UI yet, but this should give you an idea of how this feature works.  First I created a new seed set.  (This is an action that might be performed by a researcher or an archivist.)  In SFM, a seed set is a list of seeds for a harvest, where a seed might be a Twitter handle or a Flickr user.  Since the list is in reverse chronological order, the entry for creating the seed set is second.  Second, I changed the schedule of the harvest.  This is the first entry below.

Seed set changes

Notice that whenever a change is made, the following is recorded:

* Each field and value that is changed. In this example, the schedule was changed.
* Who made this change.  In this example, “justin” made the change.
* When the change was made.
* An optional note describing the reason for the change.

Again, the UI work is still to be done, but you can imagine an (understandable) version of these changes appearing when a user is reviewing a seed set.

Note that this change history is also tied into how we keep track of harvests -- SFM records the exact state of the collection criteria used to perform the harvest.

For those wondering, this is implemented with django-simple-history.

If you have thoughts on this feature, comments are welcome.  In particular, we’re interested in ideas about how to make this information available and useful to researchers, especially in dataset exports.  I can be reached @justin_littman or the whole team at sfm-dev.

(This post originally appeared on the [Scholarly Technology Group’s blog](https://library.gwu.edu/scholarly-technology-group/posts/tracking-changes-harvests-social-feed-manager) on the GW Libraries website.)
