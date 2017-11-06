---
layout: article
permalink: /posts/2017-11-04-digital-registry
title: "Suspended U.S. government Twitter accounts"
author: justin_littman 
excerpt: "In which I look at suspended Twitter accounts listed in the U.S. Digital Registry, including some recently tweeting in Russian."
---

At GW Libraries, we collect the tweets of roughly 3000 U.S. government agencies using Social Feed Manager. This originated with our involvement in the [End of Term project](http://eotarchive.cdlib.org/), a collaborative effort to capture the web presence of the federal government at the end of each presidential term. However, given the affordances of Twitter (viz., the ability to collect historical tweets is extremely limited), we decided to continue collecting the tweets on an ongoing basis.

When collecting a large number of Twitter accounts, the list of accounts requires occasional maintenance, as sometimes Twitter accounts are deleted or protected. It’s understandable how U.S. government accounts would be expected to change over time as agencies and initiatives change. However, when I was doing maintenance earlier today, I noticed something odd: a number of the accounts were [suspended](https://support.twitter.com/articles/15790), not deleted or protected.

Curious, I exported the tweets from some of the suspended accounts. Really odd -- the tweets were in Russian.

Then I checked back in the [U.S. Digital Registry](https://usdigitalregistry.digitalgov.gov/). The U.S. Digital Registry is supposed to be the authoritative list of the official U.S. government social media accounts. I’m going to quote here, because the irony is almost unbearable:

>Whether for access to emergency, financial or education public services, users need to trust they are engaging with official U.S. government digital accounts.

>The U.S. Digital Registry serves as the authoritative resource for agencies, citizens and developers to confirm the official status of social media and public-facing collaboration accounts, mobile apps and mobile websites, and help prevent exploitation from unofficial sources, phishing scams or malicious entities.

Time for a bit of sleuthing. I downloaded and cleaned up the list of Twitter accounts from the U.S. Digital Registry and then called the [GET users/show](https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-show) method from Twitter’s API. If the call returns an HTTP status code of 403 (Forbidden) then the account is suspended. Here are the suspended accounts that I found:

* CBPNorthEast
* ProjectBlueBtn
* usfwsinternatl
* fedfooddrive
* NASA_SDO_edu
* NASAHumanHealth
* myafn_sports
* afnradio
* npcpao
* vussddg95
* _ NEDU _
* democracyis
* BruceWharton
* EconEngage
* AmbCorbin
* TTBgov
* NSF_ERE
* nasa_sdo_edu
* FederalCloud
* ACSMonterrey
* EisenhowerNews
* DoDLiveMil
* AFPS_Articles
* usasearch
* vasanfrancisco
* GSAR4CAR
* USEmbassyBah
* EconEngage
* MRC_OSG

The easiest way to see what had happened to these accounts is to look in the [Internet Archive](https://archive.org/). While we have collected tweets from some of these accounts, (1) [Twitter’s policies](https://developer.twitter.com/en/developer-terms/agreement-and-policy.html) won’t let me share them publicly and (2) the Internet Archive’s captures go back further. Note that the Internet Archive captures the web pages of the accounts from Twitter's website, while Social Feed Manager captures the tweets from Twitter's API as JSON. Think of them as complementary approaches for archiving social media platforms.

Here’s some examples:

@ConnectStateGov
* On May 16, 2013, a legit government account: [https://web.archive.org/web/20130516122409/https://twitter.com/connectstategov](https://web.archive.org/web/20130516122409/https://twitter.com/connectstategov)
* On Oct. 14, 2014, tweeting in Russian: [https://web.archive.org/web/20141014121748/https://twitter.com/ConnectStateGov](https://web.archive.org/web/20141014121748/https://twitter.com/ConnectStateGov)
* On Dec. 17, 2016, suspended: [https://web.archive.org/web/20161217013601/https://twitter.com/ConnectStateGov](https://web.archive.org/web/20161217013601/https://twitter.com/ConnectStateGov)

@ProjectBlueBtn
* On January 6, 2015, a legit government account: [https://web.archive.org/web/20150106030356/https://twitter.com/ProjectBlueBtn](https://web.archive.org/web/20150106030356/https://twitter.com/ProjectBlueBtn)
* On January 25, 2017, tweeting in Russian: [https://web.archive.org/web/20170125163049/https://twitter.com/ProjectBlueBtn](https://web.archive.org/web/20170125163049/https://twitter.com/ProjectBlueBtn)

The last tweet I have for this account was January 20, but from our records it appears to have been suspended around November 1.

![ProjectBluePln legit]({{ site.github.url }}/images/digital-registry/projectbluebtn-legit.png)

![ProjectBluePln Russian]({{ site.github.url }}/images/digital-registry/projectbluebtn-russian.png)

@USFWSInternatl
* On January 4, 2015, a legit government account: [https://web.archive.org/web/20150604042316/https://twitter.com/USFWSInternatl](https://web.archive.org/web/20150604042316/https://twitter.com/USFWSInternatl)
* On January 12, 2017, an “egg” account: [https://web.archive.org/web/20170112184706/https://twitter.com/USFWSInternatl](https://web.archive.org/web/20170112184706/https://twitter.com/USFWSInternatl)

@NASA_SDO_Edu
* On Sept 25, 2017, a legit government account: [https://web.archive.org/web/20160811014527/https://twitter.com/NASA_SDO_Edu](https://web.archive.org/web/20160811014527/https://twitter.com/NASA_SDO_Edu)

In fact, the web page for [SDO Outreach](https://sdo.gsfc.nasa.gov/epo/educators/) still has a widget to display the Twitter feed of the now suspended account.

Here are my guesses as what is going on:
* Other users have “taken over” the screen names of deleted U.S. government accounts.
* Perhaps Twitter is accidentally suspending some U.S. government Twitter accounts.
* Perhaps Twitter is reporting some accounts as being suspended that were actually deleted.

This all begs further investigation, or at least more than I can give it on a Saturday evening. In addition to looking more closely at the accounts listed above, it would be worth scrutinizing the complete U.S. Digital Registry Twitter list for other screen names that have been taken over, but not yet detected and suspended by Twitter.

Still, there are some immediate take-aways:

* While the U.S. Digital Registry is a very important service for promoting trust and transparency in the U.S. government and invaluable for those of us attempting to archive the web presence of the U.S. government, it desperately needs a scrubbing and quality control processes put into place.
* The U.S. government needs to take full advantage of verified status on Twitter (i.e., the blue check), perhaps even requiring it.
* Twitter needs to deal with the problem of recycled screen names. A person or organization should be able to delete an account without the fear of being impersonated. In particular, for organizations such as government agencies, this is critical.
