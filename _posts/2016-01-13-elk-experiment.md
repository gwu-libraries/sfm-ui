---
layout: article
permalink: /posts/elk-experiment/
title: "An Experiment with Social Feed Manager and the ELK Stack"
author: justin_littman
---

The latest in our social media harvesting experiments for the [Social Feed Manager](https://github.com/gwu-libraries/sfm-ui) project involves analysis, discovery, and visualization of social media content. An analytics service may help satisfy two needs:

1. For the collection creator, being able to evaluate the content that is being collected so as to adjust the collection criteria. For example, for Twitter a collection creator may discover additional hashtags to collect. Since a collection creator may be collecting a rapidly evolving event, this requires near real-time analysis.
2. For the researcher, being able to analyze the content. Though many researchers will need to export the social media content for use with other tools, having available some sort of an analytics service may meet the needs of some researchers and may lower the barrier to performing social media research.
We also wanted to test the extensibility of the SFM architecture to make sure that additional services can be readily added.

The ELK (Elasticsearch, Logstash, Kibana) stack was selected for this experiment. It was selected primarily on the intuition that it was a good fit, rather than an analysis of its features or a comparison against other options. For those not familiar with this stack, Kibana is the discovery and visualization interface, Elasticsearch is the data store, and Logstash loads Elasticsearch with data. We’ll refer to our own implementation as SFM-ELK.

In SFM infrastructure, harvesters, such as the Twitter harvester, invoke the APIs of social media platforms and record the results in WARC files. Harvesters publish warc_created messages to a message queue whenever a WARC file is created. This provides the critical hook for SFM-ELK to perform loading -- a message consumer application listens for warc_created messages. When it receives a warc_created message, it:

1. Invokes the appropriate WARC iterator (e.g., TwitterRestWarcIter) to read the WARC file and output the social media records as line-oriented JSON.
2. Pipes this to jq, which filters the JSON. Most types of social media records contain extraneous metadata which do not need to be indexed in Elasticsearch. Logstash supports various mechanisms for filtering and transforming loaded data, but jq proved better for JSON data.
3. Pipes this into Logstash, which loads it into Elasticsearch.
Once properly loaded into Elasticsearch, the data is available for discovery and visualization using Kibana. Note that additional data is loaded as new WARC files are created.

For the purposes of this experiment, data harvested from Twitter’s search API using the search terms "gwu" and "gelman" was used.

While understanding the full power and flexibility of Kibana involves a significant learning curve, some of the functionality is readily usable. For example, to discover the tweets mentioning GWU’s President Knapp, enter “knapp” in the search box on the Discover screen:

![Search on "knapp"](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%209.52.03%20AM.png)

or to find tweets posted by @gelmanlibrary:

![Search on tweets by @gelmanlibrary](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%209.54.47%20AM.png)

Kibana allows you to easily adjust the timeframe of any discovery or visualization:

![Change search timeframe](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%209.56.58%20AM.png)

To demonstrate the sort of visualizations that might be useful for a collection creator or researcher, we created a Twitter dashboard:

![Twitter dashboard](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%209.59.44%20AM.png)

Here’s each of those visualizations in a more readable size:

![Tweet rate visualization](https://library.gwu.edu/scholarly-technology-group/posts/experiment-social-feed-manager-and-elk-stack)

![Top URLs visualization](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%2010.01.38%20AM.png)

![Top hashtags visualization](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%2010.01.51%20AM.png)

![Top user mentions visualization](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%2010.02.08%20AM.png)

![Top tweeters visualization](https://library.gwu.edu/sites/default/files/news-events/Screen%20Shot%202016-01-13%20at%2010.02.22%20AM.png)

Note that the dashboard is periodically refreshed as new data is added.

As should be evident, this experiment barely scratches the surface of the capabilities of the ELK stack, or more generally, the potential of adding an analytics service to Social Feed Manager.  The code for SFM-ELK is available at https://github.com/gwu-libraries/sfm-elk. Instructions are provided to bring up a Docker environment so that you can give it a try yourself. Keep in mind that this is only a proof-of-concept and it is not currently in scope of SFM development.

If any of this is of interest to you or your organization, collaborators are welcome.

P.S.  It was [just announced](https://www.arhu.umd.edu/news/documenting-now-archiving-social-media-generations-come) that Washington University in St. Louis, the Maryland Institute for Technology in the Humanities (MITH) at the University of Maryland, and the University of California, Riverside were awarded a Mellon grant for a project titled "Documenting the Now: Supporting Scholarly Use and Preservation of Social Media Content." Since there’s a clear need to support researchers' and archivists' needs for good analytical tools, we look forward to their work. Follow the project at [@documentnow](https://twitter.com/documentnow).

(This post was originally posted on the [Scholarly Technology Group's blog](https://library.gwu.edu/scholarly-technology-group/posts/experiment-social-feed-manager-and-elk-stack) on the GW Libraries website.) 
