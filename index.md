---
layout: home 
permalink: /
title: "Home"
image:
  feature: blue-bg.png
---
<div class="tiles">
  <div class="tile"><p>Social Feed Manager is open source software for libraries, archives, cultural heritage institutions and research organizations. It empowers those communities' researchers, faculty, students, and archivists to define and create collections of data from social media platforms. Social Feed Manager will harvest from Twitter, Tumblr, Flickr, and Sina Weibo and is extensible for other platforms.  In addition to collecting data from those platforms' APIs, it will collect linked web pages and media.</p></div> 
  <div class="tile"><h2>Latest Posts</h2></div>
  {% for post in site.posts %}
	{% include post-grid.html %}
  {% endfor %}
  <div class="tile"><p><img src="{{ site.github.url }}/images/nhprc-logo.png" width="100" alt="NHPRC logo" align="left">Social Feed Manager is supported by a grant from the
  <a href="http://www.archives.gov/nhprc/">National Historical Publications & Records Commission</a></p>
  </div>
</div><!-- /.tiles -->
