---
layout: home 
permalink: /
title: "Home"
image:
  feature: blue-bg.png
---

<div class="tiles">
  <div class="tile"><h2>Latest Posts</h2></div>
  {% for post in site.posts %}
	{% include post-grid.html %}
  {% endfor %}
  <div class="tile"><p><img src="{{ site.github.url }}/images/nhprc-logo.png" width="100" alt="NHPRC logo" align="left">Social Feed Manager is supported by a grant from the
  <a href="http://www.archives.gov/nhprc/">National Historical Publications & Records Commission</a></p>
  </div>
</div><!-- /.tiles -->
