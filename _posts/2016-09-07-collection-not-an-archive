---
layout: article
permalink: /posts/2016-09-07-collection-not-an-archive
title: "When is a Collection not an Archive?"
author: christie_peterson
excerpt: ""
---

Collecting Twitter content via the API affords archivists significant advantages
over other methods of capturing this data, but doing so in order to preserve and
broadly disseminate a historical record (i.e., creating an archive as most of us
would recognize it) requires violating the contractual conditions by which
Twitter currently provides access to that API. Such is the conclusion that
myself and many of my colleagues working on Social Feed Manager have discussed
and worked towards over the last year.

This is
[well-known](https://medium.com/on-archivy/on-forgetting-e01a2b95272#.w4fiw2wim)
to those of us who are actively involved in the development of tools to make it
easier to collect data sets from the API, but as those tools mature, it deserves
additional consideration and discussion among the larger community of archivists
who are using them. What I am writing out here is not original; it is the
product of over a year of active and sometimes heated discussions with my
colleagues here at GW and beyond. It is a synthesis of those discussions and I
am indebted to everyone who has engaged in them. However, I am writing this here
because I want to bring these issues to the attention of the wider group of
archivists who may not have been engaged in or following earlier discussions and
news stories relevant to this topic.

Disclaimer: I am not a lawyer, and I am certainly not your lawyer (and I am
definitely not GW's lawyer). This discussion involves interpretation of a
contract and an assessment of legal risks, which are things you should consider
discussing with your own attorney. I do not intend to be giving legal advice
here. Instead, I merely wish to highlight what I and many of my colleagues see
as some of the archival implications of a plain-English interpretation of the
contract that applies to users of the Twitter API.

Twitter's [Developer Policy](https://dev.twitter.com/overview/terms/policy)
provides rules and guidelines for developers who interact with Twitter's
ecosystem of applications, services, website, web pages and content ("Twitter
Services"). What does this policy actually say? In [section F ("Be a Good
Partner to
Twitter"](https://dev.twitter.com/overview/terms/policy#6.Update_Be_a_Good_Partner_to_Twitter),
item 2 reads:

>     2\. If you provide Content to third parties, including downloadable datasets of
> Content or an API that returns Content, you will only distribute or allow
> download of Tweet IDs and/or User IDs.
>
>        a\. You may, however, provide export via non-automated means (e.g., download of spreadsheets or PDF files, or use of a
> "save as" button) of up to 50,000 public Tweets and/or User Objects per user of
> your Service, per day.
>
>        b\. Any Content provided to third parties via non-automated
file download remains subject to this Policy.

Some have interpreted "third parties" to mean anyone outside one's own
institution. Under this interpretation, sharing the full content obtained via
the API with people at one's own institution would be allowed, but all others
could only be provided with lists of Tweet IDs and User IDs, which are opaque
identifiers linked to individual tweets and users. Recipients of such a list
would then have to "rehydrate" it, or run it against the current Twitter API,
which will return content only for those tweets or users that are still publicly
available on Twitter, as well as updated metadata, such as the number of likes
and retweets, rather than the state of the Tweet at the time of capture.

But what about clause a, which allows download of up to 50,000 public Tweets?
The key is the term "public". Elsewhere in the Developer Policy, Twitter is
pretty explicit that it expects services to "surface" tweets only as they
currently exist on Twitter. Under [Section B ("Maintain the Integrity of
Twitter's
Products")](https://dev.twitter.com/overview/terms/policy#2.Update_Maintain_the_Integrity_of_Twitter%E2%80%99s),
item 6 reads:

> 6\. Only surface Twitter activity as it surfaced on Twitter. For example, your
> Service should execute the unlike and delete actions by removing all relevant
> Content, not by publicly displaying to other users that the Tweet is no longer
> liked or has been deleted.

Along similar lines, item 3 under [Section C ("Respect Users' Control and
Privacy")](https://dev.twitter.com/overview/terms/policy#3.Update_Respect_Users_Control_and_Privacy)
reads:

> 3\. Take all reasonable efforts to do the following, provided that when requested
> by Twitter, you must promptly take such actions:
>    a. Delete Content that Twitter reports as deleted or expired;
>    b. Change treatment of Content that Twitter reports is subject to changed sharing options (e.g., become protected);
>    c. and Modify Content that Twitter reports has been modified.

These rules make perfect sense when applied to most applications that use the
Twitter API, like [TweetDeck](https://tweetdeck.twitter.com/): the tweets that a
Twitter user sees through that application should be the same tweets they'd see
by visiting the Twitter website directly. They are, however, diametrically
opposed to the archival purpose -- at its core, what is an archive other than a
source of content that isn't readily available elsewhere?

This is exactly the issue that
[Politwoops](http://politwoops.sunlightfoundation.com/), a website that bills
itself as "an archive of the public statements deleted by U.S. politicians," ran
into last year, when Twitter shut down its access to the API. A [statement
issued by
Twitter](http://web.archive.org/web/20150605005627/http://tktk.gawker.com/twitter-just-killed-politwoops-1708842376)
at the time read, in part:

> We strongly support Sunlight's mission of increasing transparency in politics
> and using civic tech and open data to hold government accountable to
> constituents, but preserving deleted Tweets violates our developer agreement.
> Honoring the expectation of user privacy for all accounts is a priority for us,
> whether the user is anonymous or a member of Congress.

Ultimately, after private negotiations, Twitter reversed its decision and
reinstated Politwoops' API access, essentially on the grounds that [the website
was providing a public good that outweighed politicians' expectations of Twitter
account
privacy](https://blog.twitter.com/2015/holding-public-officials-accountable-with-twitter-and-politwoops).

Ethically, archivists are bound to respect and uphold certain expectations of
privacy. However, not all content that disappears from Twitter poses a threat to
personal privacy, and archivists must balance individual expectations of privacy
against the potential public good of preservation. As Ed Summers wrote in his
[seminal
essay](https://medium.com/on-archivy/on-forgetting-e01a2b95272#.si5x7mmdm) on
this topic:

> As any archivist will tell you, forgetting is an essential and unavoidable part
> of the archive. Forgetting is the why of an archive. Negotiating what is to be
> remembered and by whom is the principal concern of the archive.

Allow me to insert here an example from my own work in this area. Several years
ago, my predecessor as GW university archivist, Bergis Jules, set up a
collection in the earlier version of Social Feed Manager to capture content
posted from GW-related Twitter accounts. I recently revisited this list of
Twitter handles to migrate it to the new version of SFM and update it along the
way. Out of 240 handles, exactly three had been deleted or made private in the
interim: @GWDCBound, @gwgreeklife and @gwfoodforce, all apparently institutional
GW accounts. What had been lost was not material that individuals or student
organizations had deleted out of concern for their privacy, but content that the
institution had deleted because it was no longer current. In other words,
exactly the content that the archives was intended to preserve.

Archivists have at least three options in front of us right now:

1. Follow the Twitter developer agreement to the letter, and only preserve or
provide access to Tweet IDs, which must be rehydrated in accordance with what is
currently available on Twitter. As archivists, many of the members of our team,
myself included, find this option untenable over the long-term, and the
collections so created not valuable enough to be worth the resources required
collect and maintain them in the vast majority of cases. This is the case where
a "collection" is not actually an "archive" because it lacks the promise of
long-term preservation and access.
2. Ignore the agreement, and use the API to create collections with the intention
of providing access to the full content either now or in the future. This is
probably the most expedient option, but one that I'm not sure all organizations
(or their legal counsel) would support if they fully understood it. How many
organizations are in positions to create and maintain digital collections whose
legal status may be questionable for the foreseeable future?
3. Engage as a profession with Twitter to negotiate an exemption to its developer
agreement for libraries and archives similar to [Section 108 of the U.S.
Copyright Act](http://www.section108.gov/about.html). As professional
archivists, we have principles, purposes, and experience on our side to make a
compelling argument for why such an exemption should be made, and why we are the
ones for whom it should be made. This option is one that has frequently come up
in our team meetings, but more often in the abstract than the actionable. I'm
not sure who exactly could take on this negotiation -- perhaps a professional
organization, such as ALA or SAA; maybe a large archive with a vested interest
in the topic; or maybe an ad-hoc organization of smaller archives. I am sure
that it's time we started talking about it. History is disappearing while we
wait.
