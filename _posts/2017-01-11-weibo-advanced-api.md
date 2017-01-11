---
layout: article
permalink: /posts/2017-01-11-weibo-advanced-api
title: "Weibo Advanced API"
excerpt: "This is a continuation for Weibo API guide. This part focuses on address issues on Weibo advanced API."
author: victor_tan
tags: [weibo, API, Advanced, sfm]
---
	
This is a continuation for [Weibo API guide]({{ site.github.url }}/posts/2016-04-26-weibo-api-guide) . This part focuses on address issues on Weibo advanced API. 
If you haven't go through the previous one, please take a look at it first.


## 1. Weibo Advanced API
All the advanced API marked as `高(Advanced)` in the  [Weibo API](http://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI) page. 
For example, [timeline_batch](http://open.weibo.com/wiki/2/statuses/timeline_batch) and [search/topics](http://open.weibo.com/wiki/2/search/topics).

## 2. How to Apply Weibo Advanced API

If you want to get access to these APIs, there are some basic rules as the [official guide](http://open.weibo.com/wiki/%E9%AB%98%E7%BA%A7%E6%8E%A5%E5%8F%A3%E7%94%B3%E8%AF%B7) says.

* Approved APP on Weibo open platform.
* Follow the platform policy and agreement.
* No illegal records of your APP.

Except these basic rules, I highly recommend you make the user of your APP reach some level. The number of the user depends on which API you are trying to apply.
If all goes well, just follow the section of `How to apply` in the official guide. Weibo will response to your application in one or two business day.
If approved, just follow [this section]({{ site.github.url }}/posts/2016-04-26-weibo-api-guide#get-access-token) to re-generate your access token.

## 3. Access Weibo Search in SFM
[Social Feed Manager]({{ site.github.url }}) provide a optional feature of Weibo search. As the API doc says it only return the latest 200 weibos related to the given topic.
To build a collection of Weibo search is much like the steps of Twitter search. The post only provide guide related to the credential issue.

### 3.1 Get Temporary Access Token
Usually, SFM will provide an instance including Weibo search at GW Libraries network. It supports authorization work to the approved SFM APP at open Weibo platform. 
You can get a temporary access token which last for 30 days when you complete giving authorization work to SFM. Here shows how it work.

Go to SFM credential page and click `Connect Weibo Account`.
![weibo connect btn]({{ site.github.url }}/images/weibo/weibo_connect.png)

Next page would be like this:
![weibo auth login]({{ site.github.url }}/images/weibo/weibo_auth_login.png)

Giving your username and password, click red `登录(Login)` button and then click the red `授权(Authorize)` button in next page.
Finally, you will be redirect to the access token page.
![weibo sfm access]({{ site.github.url }}/images/weibo/weibo_sfm_token.png)

With above access token, you can build your own Weibo search collection. By the way, the access token will expire in 30 days.

## 4. Reference

* [Weibo Advance API Apply](http://open.weibo.com/wiki/%E9%AB%98%E7%BA%A7%E6%8E%A5%E5%8F%A3%E7%94%B3%E8%AF%B7)
* [Weibo API](http://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI)
