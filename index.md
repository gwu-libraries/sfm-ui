---
layout: home 
permalink: /
title: "Home"
image:
  feature: blue-bg.png
---
<div class="tiles">
  <div class="tile"><p>Social Feed Manager is open source software for libraries, archives, cultural heritage institutions and research organizations. It empowers those communities' researchers, faculty, students, and archivists to define and create collections of data from social media platforms. Social Feed Manager harvests from Twitter, Flickr, Sina Weibo, and Tumblr (coming soon), is extensible for other platforms, and can also collect embedded and linked media and web pages.</p>
  <p>For more information see <a href="{{ site.github.url }}/about/overview">Overview of Social Feed Manager</a> and the <a href="https://sfm.readthedocs.org">documentation</a>.</p> 

  <p>Members of the GW community who wish to access Twitter data will find more information at <a href="https://library.gwu.edu/scholarly-technology-group/social-feed-manager">GW Libraries.</a></p></div> 
  <div class="tile"><h2>Latest Posts</h2></div>
  {% for post in site.posts %}
	{% include post-grid.html %}
  {% endfor %}
  <div class="tile"><p><img src="{{ site.github.url }}/images/nhprc-logo.png" width="100" alt="NHPRC logo" align="left">Social Feed Manager is supported by a grant from the
  <a href="http://www.archives.gov/nhprc/">National Historical Publications & Records Commission</a></p>
  </div>
</div><!-- /.tiles -->
