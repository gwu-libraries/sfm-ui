---
layout: article
permalink: /posts/2017-12-13-web-social-media-archiving
title: "Web archiving and/or/vs social media API archiving"
author: justin_littman 
excerpt: "In which I discuss the differences between collecting social media via web capture and APIs."
---

Yesterday morning I participated in the tools demo at "[Digital Blackness in the Archive: A Documenting the Now Symposium](http://www.docnow.io/meetings/stl-2017/)." During the breakout I had the opportunity to chat with a number of fellow participants about social media data. In a handful of those discussions, I answered questions about the difference between social media collected from a social media platform’s APIs and social media collected via web capture. Inspired by this, I thought I would write it up in this post.

I’m simplifying a bit here, but there are two mechanisms for interacting with social media platforms. The first is via the website. The website delivers social media content as HTML (and CSS and JS and other) for rendering via browsers. The second is via their APIs (short for "Application Programming Interfaces"). The API delivers social media content as structured text (generally JSON) for consumption by software (such as an app on your phone).

Web archives collect social media content from the website by (again, simplifying) either pretending to be a browser or using a real browser, making a request for web pages, and recording all of the files that the website returns. These files can then be played back to re-enact the experience of using the website at the time the capture occurred. Rhizome’s [WebRecorder](https://webrecorder.io/) and Internet Archive’s [Archive-It](https://archive-it.org/) are examples of tools/services that perform web capture; Rhizome’s [Webrecorder Player for Desktop](https://github.com/webrecorder/webrecorderplayer-electron) and Internet Archive’s [Wayback Machine](http://web.archive.org/) are examples of tools that perform playback.

Social media archives collect social media content from the API by making calls to the API and recording the returned data. These files are just data; there is no playback. DocNow’s [Twarc](https://github.com/docnow/twarc) and our [Social Feed Manager](http://go.gwu.edu/sfm) are examples of social media API collecting tools.

For comparison, here is live tweet embedded in this post:

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Here&#39;s the tools I talked about at <a href="https://twitter.com/hashtag/BlackDigArchive?src=hash&amp;ref_src=twsrc%5Etfw">#BlackDigArchive</a> tools demo: <a href="https://twitter.com/SocialFeedMgr?ref_src=twsrc%5Etfw">@SocialFeedMgr</a> <a href="https://t.co/IO9lrkXWMT">https://t.co/IO9lrkXWMT</a>, TweetSets <a href="https://t.co/zbiMpkEB5X">https://t.co/zbiMpkEB5X</a>, F(b)arc <a href="https://t.co/umpXwip3sm">https://t.co/umpXwip3sm</a></p>&mdash; Justin Littman (@justin_littman) <a href="https://twitter.com/justin_littman/status/940614634163326976?ref_src=twsrc%5Etfw">December 12, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


That same tweet archived by the Internet Archive is: [http://web.archive.org/web/20171213144402/https://twitter.com/justin_littman/status/940614634163326976](http://web.archive.org/web/20171213144402/https://twitter.com/justin_littman/status/940614634163326976). (Notice the imperfect re-creation of the original tweet.)

And here’s the same tweet retrieved from Twitter’s API with Twarc: [https://gist.github.com/justinlittman/219f21f3cf9d763405985875c7802048](https://gist.github.com/justinlittman/219f21f3cf9d763405985875c7802048)

Web archives and social media API archives should be thought of as complementary. However, if your primary interest is in the experience of a social media platform, i.e., the "look and feel", then web capture will be more useful. If your primary interest is in social media as data, e.g., to apply computational techniques, then API-collected social media will be more useful.

There are some additional distinctions that are worth noting:

* APIs allow some forms of broad collecting that aren’t possible/easy with web capture. For example, with the Twitter API it is possible to capture tweets by hashtag or term.
* Each social media API is different and therefore requires different software. In general, the same web capture technique can be used with a web array of websites.
* APIs and websites may expose different metadata/data. For example, there is some tweet metadata that is available from the Twitter API, but not the website.
* Social media APIs and websites are often governed by different terms or policies.
* Social media websites are constantly being tweaked; APIs change infrequently and changes are announced in advance.
* Not all social media platforms provide a public API; in some cases, the API is only reserved for business partners.

One final word on web capture: For individual use or use with social media sites, I always recommend Rhizome’s tools. Because of their origins in capturing online art, they have invested significant effort in accurate capture and playback. Also, their approach is especially well suited for social media sites, which rely heavily on scripting which confounds other web capture approaches. For institutional use, Internet Archive’s ArchiveIt service is the go-to.
