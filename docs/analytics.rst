====================
 Analytics with ELK
====================

The ELK (`Elasticsearch <https://www.elastic.co/products/elasticsearch>`_, `Logstash <https://www.elastic.co/products/logstash>`_,
`Kibana <https://www.elastic.co/products/kibana>`_) stack provides a general-purpose analytics framework.

SFM provides an instance of ELK that has been customized for loading, analyzing, visualizing, and querying social
media data. This is a separate, optional container as described below.

The following are important caveats about SFM ELK:

* SFM ELK is only experimental. We have not yet determined the level of development that will be performed in
  the future.
* Only Twitter data is currently supported.
* Approaches for administering and scaling ELK have not been considered.

How to enable a container.
How to perform retroactive load with resendwarccreatedmsgs management command.
Using Kibana.
- Note about timeframe.
- Dashboard > Load Saved Dashboards > Twitter.