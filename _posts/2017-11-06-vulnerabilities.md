---
layout: article
permalink: /posts/2017-11-06-vulnerabilities
title: "Vulnerabilities in the U.S. Digital Registry, Twitter, and the Internet Archive"
author: justin_littman 
excerpt: "In which I demonstrate vulnerabilities in the U.S. Digital Registry, Twitter, and the Internet Archive to manipulate web history."
---

The [U.S. Digital Registry](https://usdigitalregistry.digitalgov.gov/) is the authoritative list of the official U.S. government social media accounts. One of the [stated purposes](https://medium.com/@GeneralServicesAdministration/new-u-s-digital-registry-authenticates-official-public-service-accounts-1f8120d67976) of the U.S. Digital Registry is to "support cyber-security by deterring fake accounts that spread misinformation".

![U.S. Digital Registry]({{ site.github.url }}/images/vulnerabilities/digital_registry.png)


As discussed in the [previous post]({{ site.github.url }}/posts/2017-11-04-digital-registry), the U.S. Digital Registry contains 29 suspended Twitter accounts. However, not discussed in that last post is that it contains 100 deleted accounts. Here are a few of those accounts:

* ArmyWTC
* VA_OIT_PD
* USAITA_ExecDir
* ID_PanhandleNF
* hhsnewmedia
* CSBostonMA
* techatstate
* energycodes
* VA_EES_Social
* NIHRadio
* VAHVHCS
* WichitaVAMC
* USGSTNMRes
* USEmbCameroon
* usembassyteg
* USEmbassyRiyadh

In Twitter, you can claim the screen name of a deleted account (you cannot claim the screen name of a suspended account). I chose to claim the screen name @USEmbassyRiyadh.

![Account rename]({{ site.github.url }}/images/vulnerabilities/account_rename.png)

Again, @USEmbassyRiyadh is listed by the U.S. Digital Registry as an official government account:

![U.S. Digital Registry for @USEmbassyRiyadh]({{ site.github.url }}/images/vulnerabilities/USEmbassyRiyahd-digital_registry.png)

Clicking on this link goes to [https://twitter.com/USEmbassyRiyadh](https://twitter.com/USEmbassyRiyadh).

To make my imposter account convincing it had to look like the previous, deleted, official account. For this, I turned to the [Internet Archive](https://archive.org), which has [numerous captures of the account](http://web.archive.org/web/*/http://twitter.com/USEmbassyRiyadh). Here's the capture from December 15, 2016:
 
![USEmbassyRiyadh in IA real]({{ site.github.url }}/images/vulnerabilities/USEmbassyRiyadh-IA-real.png)
 
 I gave the imposter account the same banner image, profile image, name, location, bio, and website of the official @USEmbassyRiyadh account.
 
 
 There are some aspects of the official account that I could have duplicated such as the tweets, following, followers, likes, and moments (which would have taken some work). Duplicating the verified status and the Twitter join date would be more problematic.
 
 And then I tweeted as the @USEmbassyRiyadh. Here's the fake account:

![@USEmbassyRiyadh]({{ site.github.url }}/images/vulnerabilities/USEmbassyRiyadh-fake.png)

While I chose to tweet a quote from Wilford Brimley, my tweets could have been more insidious. Anyone checking the U.S. Digital Registry would have found my fake account listed as official. And anyone checking the Internet Archive would have found my account looked similar to previous captures of the account.
 
 The final step was to add the imposter page to the Internet Archive. For this, I used Internet Archive's "Save Page Now" function to request that http://twitter.com/USEmbassyRiyadh be saved.

![Save Now]({{ site.github.url }}/images/vulnerabilities/IA_save_now.png)
 
![Capturing to Internet Archive]({{ site.github.url }}/images/vulnerabilities/IA_capture.png)
 
 And here's the captured page:
 
 ![USEmbassyRiyadh in IA fake]({{ site.github.url }}/images/vulnerabilities/USEmbassyRiyadh-IA-fake.png)
 
 (No, I don't know why the Internet Archive captures Twitter pages using different languages, in this case, Norwegian.)
 
 Since the imposter account and the official, deleted account have the same URL the captures are displayed together in the Internet Archive's Wayback Machine.
 
 ![USEmbassyRiyadh in IA]({{ site.github.url }}/images/vulnerabilities/USEmbassyRiyadh-IA.png)
 
 Without close scrutiny, it is not evident that the most recent capture is fake. (This "attack" was inspired by Lerner, Kohno, and Roesner's "[Rewriting History: Changing the Archived Web from the Present](https://repository.wellesley.edu/cgi/viewcontent.cgi?referer=https://t.co/h80k4hb5lG&httpsredir=1&article=1158&context=scholarship)).
 
 While I have to admit a tad bit of ethical queasiness about this exercise, I felt it was justified to demonstrate that a Twitter account that is allegedly representative of the U.S. government can be faked and then recorded in the best historical record of web history that we have. I would suggest that the implications for our trust in official information from the U.S. government, Twitter as a communications platform, and the Internet Archive as the historical record are significant.
 
 I repeat my suggestions from the previous post and add some additional:
 * The U.S. Digital Registry should be scrubbed and quality control processes put into place.
 * The Registry should maintain a record of deleted Twitter accounts.
 * The Registry should record and share the user ids of Twitter accounts, in addition to the screen names.
 * U.S. government Twitter accounts should all be verified.
 * Twitter should not allow the screen names of deleted account to be re-used.
 * Twitter should display the user ids of accounts on the web page. This would make it easier to identify when an account is being faked.
 * The Internet Archive should supplement its web captures of Twitter accounts with data collected from Twitter's API, since the data retrieved from the API contains more information than is displayed on the web page. Perhaps for each Twitter account and tweet that is captured, the same Twitter account and tweet could be retrieved from Twitter's API.

Some additional notes:
* I provided a copy of this blog post to Digital.gov and the Internet Archive in advance of publishing.
  * Digital.gov is planning to "host a government-wide sprint to invite all agencies to review and update their accounts," so expect improvements to be forthcoming.
  * Internet Archive reports that they are aware of the bug with capturing Twitter in different languages and will be fixing.
* I returned my Twitter account to its original state and no longer have the screen name @USEmbassyRiyadh.
* Thanks to Laura Wrubel for reviewing this post and making suggestions.
