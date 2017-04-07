---
layout: article
permalink: /posts/2017-04-07-geographic-collecting
title: "Collecting by Geographic Location"
author: yonah_bromberg_gaber
excerpt: "SFM provides the opportunity to collect useful metadata about the geographic
location of tweets provided by the Twitter API."
---

# Collecting by Geographic Location

Social Feed Manager collects useful metadata about the geographic location of tweets provided by
the Twitter API. SFM also includes the functionality to collect posts based on
the sole criteria of where they are located.

You can collect by geographic location using Twitter Search and Twitter
Filter collections. Here we’ll discuss best practices in setting up collections
using geographic location, based on the documentation for the
Twitter [Search](https://dev.twitter.com/rest/public/search
"Twitter Search docs") and [Filter](https://dev.twitter.com/streaming/reference/post/statuses/filter
"Twitter Filter docs")
APIs and practical experience collecting by geographic location.

*(Note the mark of “Washington, D.C.” at the bottom of the tweet. This post had
“Place” identified, but not geographic coordinates).*

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Looking forward to tomorrow&#39;s conversation on social media research with faculty across <a href="https://twitter.com/hashtag/gwu?src=hash">#gwu</a> departments <a href="https://t.co/se0z7IYlUY">https://t.co/se0z7IYlUY</a></p>&mdash; Social Feed Manager (@SocialFeedMgr) <a href="https://twitter.com/SocialFeedMgr/status/846356497122693120">March 27, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

SFM collects two different types of metadata related to geographic location:
coordinates and place. Coordinates are the actual geographic coordinates of
where a person is located, usually identified by a mobile device’s location
software. Place is a location selected by the user when posting the tweet,
using descriptive data for identification, like a city or neighborhood name.
Coordinates are sometimes automatically provided based on place and place is
sometimes automatically provided based on the coordinates. For more information
see Twitter documentation about [Place](https://dev.twitter.com/overview/api/places
"Twitter Place docs").

*(This snippet of the JSON file for the above tweet shows the different pieces
of location data. Note that the tweet wasn’t geolocated with coordinates, but
instead had “Place” identified as Washington, D.C., which is identified as a
box polygon of coordinates).*

```javascript
"source": "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>",
	"retweeted": false,
	"coordinates": null,

"place": {
		"full_name": "Washington, DC",
		"url": "https://api.twitter.com/1.1/geo/id/01fbe706f872cb32.json",
		"country": "United States",
		"place_type": "city",
		"bounding_box": {
			"type": "Polygon",
			"coordinates": [
				[
					[-77.119401, 38.801826],
					[-76.909396, 38.801826],
					[-76.909396, 38.9953797],
					[-77.119401, 38.9953797]
				]
			]
		},
		"contained_within": [],
		"country_code": "US",
		"attributes": {},
		"id": "01fbe706f872cb32",
		"name": "Washington"
	}
```

There are two SFM collection types that can include geographic location as a
criterion: Twitter Filter and Twitter Search. They function similarly, but
require different entries.

For a Twitter Filter, a bounding box is used with geographic coordinates used
to define it. The Northeast and Southwest corners are selected to determine the
box, and tweets geolocated within that box are collected, as well as tweets in
the surrounding area based on overlapping named areas (see Bounding Boxes below).

We used Google Maps to find coordinates by finding the geographic location of
the coordinate we needed and right-clicking on the spot, selecting “What’s
here?” which provides a geographic coordinate.

Degrees in decimal format rather than with minutes are used (e.g. -77.15 rather
than 77°9”). The order is somewhat counterintuitive, and uses Southwest corner,
Northeast, with the coordinates reversed to East-West, North-South, so that it
looks like this:

WW,SS,EE,NN (WW is westernmost coordinate, SS is southernmost, etc.)

-77.15,38.8,-76.9,39.0 (This bounds D.C.)

For a Twitter Search, a bounding circle is used by giving the center of the
circle and a radius, so that it looks like this:

NN,SS,Rmi (NN is longitude, SS is latitude, R is radius in miles).

38.894471,-77.036731,7mi (This circumscribes D.C.)

See "Bounding Boxes" below for more information on how tweets are collected
corresponding to these boxes.

## Considerations

There are caveats to using geographic location successfully:

+ Based on our sampling, more than 98% of users don’t allow their tweets to be
  geotagged. Geotagging is opt-in, so location is only recorded when users want
	to publish their location. You should determine whether the users’ tweets you want
  to collect are from users that would publish their location. You can take a
  look at this table, analyzed from a Twitter Sample taken over three days in
  November 2017. Note that there is a good chance that people would be more
  likely to geotag a tweet in a place of interest.

| Category                      | Number of Tweets | Percentage of Total  |
| --------------------------------------------- |:----------:| -----:|
| Total tweets                                  | 11,094,106 | 100%  |
| Tweets that have Coordinates	                | 31,454     | 0.28% |
| Tweets that have Place                        | 204,442    | 1.84% |
| Tweets that have both Coordinates AND Place   | 31,282     | 0.28% |
| Tweets that have Coordinates OR Place         | 204,614    | 1.84% |
| Tweets that have only Coordinates (w/o Place) | 172        | 0.00% |
| Tweets that have only Place (w/o Coordinates) | 173,160    | 1.56% |

+ Location data is not evenly distributed. A [2015 study for the ICWSM Workshop](http://www.aaai.org/ocs/index.php/ICWSM/ICWSM15/paper/download/10662/10551
  "Population Bias in Geotagged Tweets") showed that geotagged tweets don’t occur
  evenly based on population. Geotagged tweets are more likely to occur in
	unpopulated tourist destinations (the National Mall, Disney World) and less
	likely to occur in certain heavily populated areas with restrictions, like
	prisons. In more residential areas, rates of geotagging are affected by a
	number of factors including:  
  + Age (more geotagged tweets come from areas with younger populations)
  + Higher income
  + Urban areas
  + Race, with data biased towards Hispanic/Latino and Black populations
+ A wide variety of posts may come from a specific location. If you’re trying
  to collect tweets from bankers on Wall Street by collecting the geographic
  area of Wall Street, you’ll also end up with tweets from tourists and local
  residents. You may use additional search terms to minimize this, however…
+ Predicting what other search terms will be fruitful is difficult. This is
  particularly important if you want to attempt any form of completeness; if
  you add additional search terms, you will be limited to tweets that match
  those search terms. In the Wall Street banker example, you can’t assume that
  every banker is using the same hashtags or keywords.
+ There are significant privacy concerns. While SFM does not collect from
  protected accounts, collecting all tweets in a certain area may be considered
  an invasion of privacy. You should use discretion in collecting. For example,
  collecting every tweet on a college campus or from a specific neighborhood
  would probably be considered out of bounds, while collecting tweets from the
  main stadium during the Olympics would probably be acceptable.
+ Choosing a location can be difficult, depending on the research question. On
  the one hand, you want to make sure to include the entire area that you want;
  on the other hand, you don’t want to overload your data with too many
  irrelevant posts. See below for an example.
+ Additionally, when using a filter geographic collection, tweets that are
  tagged for a location similar to where your box is located will also be
  collected. See the “Bounding Boxes” section for an explanation.

All this being said (and it really is quite a lot), there are also plenty of
great uses for location filtering, particularly for specific events or landmarks.

## Bounding Boxes

We’ve run a few collections based on geographic location, and through trial and
error learned what considerations to include when collecting using bounding boxes.

<iframe src="https://www.google.com/maps/d/u/0/embed?mid=1V8ipT2mBuK--Xa99iV937b8rGNk" width="640" height="480"></iframe>

*(Map 1)*

The first was of the 2017 Inauguration and the Women’s March following the next
day, using the National Mall and surrounding areas as our collection area (see
Map 1). Specifically, we used the box bounded by Eye St. North, 2nd St. East,
E St. South, and 24th St. West (which includes the White House, Capitol Complex,
National Mall to the Lincoln Memorial, and all National Mall metro stations).
Because of tagged locations in Washington, D.C., we also collected some that
were not within the bounding box, as well as some tweets from within the
bounding box that had a location set but not using GPS coordinates. In Map 1,
this would mean that we targeted tweets in the purple box but likely collected
any tweet geolocated to the light blue polygon of Washington, D.C.

It should also be noted that the bounding box used turned out not to be ideal;
the anarchist J20 riot that occurred including arrests happened on L St., North
of our bounding box (the red marker in Map 1), leaving the possibility open that
tweets about that specific protest were not included (although likely they were
collected since they were in the greater Washington, D.C. polygon).

As a second example to understand how bounding boxes and polygons interact,
look at Map 2, which is a simulation.

<iframe src="https://www.google.com/maps/d/u/0/embed?mid=1lX5dHAiipfU66InnhM1gk9xWyoQ" width="640" height="480"></iframe>

*(Map 2)*

With a desire to collect tweets from around Mount Rushmore, we might choose to
collect from all of Black Elk Park, and the bounding box reflects that. However,
you may notice that the bounding box includes the polygon of Rapid City, and so
any tweet from Rapid City may also be collected. Additionally, since the polygon
of Black Hills Forest includes Black Elk Park, the collection might also collect
any tweets from within the forest area, including at Wind Cave National Park.
Thus every tweet within a polygon in Map 2 would most likely be collected. The
tweet by Hermosa, however, would not be collected, even though it might be a
tweet including a picture from Mount Rushmore, published as the user leaves
the area.

Note that some of these tweets may not include a geographic coordinate location,
but simply self-identify their location.
