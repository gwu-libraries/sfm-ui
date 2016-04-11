---
layout: article
permalink: /posts/2016-04-05-weibo-api-guide
title: "Weibo API Guide"
excerpt: "A smooth guide for programmers and researchers who intend to use Weibo's API. I am writing this guide to support the Social Feed Manager project."
author: victor_tan
tags: [weibo, API, guide, sfm]
---
	
This is a smooth guide for programmers and researchers who intend to use Weibo's API. Since the current official documents haven't updated for a long time, I am writing this guide to support the [Social Feed Manager](http://go.gwu.edu/sfm) project. 

> I highly recommend you to ask someone with Chinese background if you feel stuck when following this guide. Please make sure you can access to Weibo without any problems. Otherwise,it would be a little hard to complete all the sections.


## Sign up a Weibo Account
The goal of this section is to get a `username` and `password` of weibo account.If you already have, please go to the next [section](#set-up-a-web-application).

### 1.1 Access to [weibo.com](http://www.weibo.com/)
At the US areas, the weibo.com will be redirected to the the us.weibo.com. The page is as follows:

![weibo index]({{ site.github.url }}/images/weibo/weibo_index.png)

### 1.2 Sign up for Free
Click the `开通微博(Open an Account)` button on the top-right menu, and the page could be like this:

![weibo signup]({{ site.github.url }}/images/weibo/weibo_signup.png)

It has two ways to fill in the form: `Use Email` and `Use Mobile Phone` , but both of them need your phone number to verify the information. This guide will follow the `Use Mobile Phone`. The page is showing below:

![weibo signup mobile]({{ site.url }}/images/weibo/weibo_signup_mobile.png)

Choose the area code for your phone number, after completing all the fields, click the `Orange` button and go to the next step.

### 1.3 Update Information
In this step, you need to provide your basic information. For the gender,`男` (on the left) means male and `女` (on the right) means female.

![weibo update info]({{ site.url }}/images/weibo/weibo_update_info.png)

Click the `Orange` button to continue.

### 1.4 Select Interests
Choose at least one of the interests on the pages,click the `Orange` button enter into the Weibo world.

![weibo interests]({{ site.url }}/images/weibo/weibo_interests.png)

### 1.5 Weibo World
If all the steps above go well, you are now in the weibo world.

![weibo interests]({{ site.url }}/images/weibo/weibo_world.png)

> If you want to log in next time, just go to [weibo.com](http://www.weibo.com/), click the `登录微博(Sign in)` button and sign in with your phone number and password.

## Set up a Web Application
The goal of this section is to obtain the following three items:

* App Key
* App Secret
* Redirect URI
If you already have all of them, please go to the next [section](#get-access-token).

### 2.1 Access to [open.weibo.com](http://open.weibo.com/)
Assume you have nothing wrong with the networking, you could see the page as follow:

![weibo app]({{ site.url }}/images/weibo/weibo_app.png)

Click the `登录(Login)` button on the top-right and sign in with your phone number (add `001` before your number if not works) and password.

### 2.2 Fill in Basic Information
If successfully, click the Avatar on the top-right of the screen, and then click the `编辑开发者信息(Update Information)` which is the first option in the menu that pops.

![weibo basic info]({{ site.url }}/images/weibo/weibo_basic_info.png)

And then, you will go the the basic information pages,it could be like this:

![weibo fill basic]({{ site.url }}/images/weibo/weibo_fill_basic.png)

> You can use your browser like Chrome to translate all the fields to your own comfortable language.

Some of fields in English:

* 开发这类型: Type of account, and '个人' means personal, '公司' means company)
* 开发者名称: Developer's name
* 所在地区: Your location, if you are not in China, just choose 海外(Overseas) and 美国(U.S.)
* 紧急联系人姓名: Emergency contact name
* 紧急联系人电话: Emergency Contact Phone

For the `Emergency contact name` and `Emergency contact phone`, you can simply fill in your own phone number. After finishing all the fields correctly which will mark green on the right. Click the `确认(OK)` button and you could see a confirmation message with a request to send confirmation email, then click the `确认(OK)` button again.

![weibo confirm email]({{ site.url }}/images/weibo/weibo_confirm_email.png)

On the next page, it will notice whether the confirm email has been sent successfully. After five seconds, you will be redirected to the home page. Now, you need to sign in your email account to confirm the information.

### 2.3 Make a Confirmation
Log in your email account and check the email sending from `weibo_app@vip.sina.com`, the email could like this:

![weibo confirm link]({{ site.url }}/images/weibo/weibo_confirm_link.png)

### 2.4 Create a web application
If all the above go smoothly, then click the `微连接(Microjoining)` on the menu bar.

![weibo menu app]({{ site.url }}/images/weibo/weibo_menu_app.png)

Next, you could see a page with types of applications. What most people would choose is `网页应用(Web Application)`.

![weibo app type]({{ site.url }}/images/weibo/weibo_app_type.png)

You will need to provide the `应用名称(Application Name)` which must be unique in the next page. When you done, click the `创建(Create)` button.

![weibo app create]({{ site.url }}/images/weibo/weibo_app_create.png)

If successfully, you will be redirected to the application manager page. Now, the `App Key` and `App Secret` will show on this page. To set a `Redirect URI`, just click the `高级信息(Advanced Information)` in the sub-menu.

![weibo app done]({{ site.url }}/images/weibo/weibo_app_done.png)

Then, locate a bar starting with the words OAuth2.0 `接权设置(OAuth2.0 Authorization Setting)`, and click the button `编辑(Edit)` on the right side of the bar.

![weibo uri set1]({{ site.url }}/images/weibo/weibo_uri_set_1.png)

Finally, you should fill in the two empty fields with any valid URL address. In most cases, it does not matter what you input. Click the green `提交(Submit)` button when you done.

![weibo uri set2]({{ site.url }}/images/weibo/weibo_uri_set_2.png)

If you complete all the sections above, you could have the `App Key`, `App Secret` and `Redirect URI`.

## Get Access Token
In this section, we need to get an `Access Token` to use most basic API. The Weibo API is kind of REST web services. For the details of using API,please refer to the [Weibo API Documents](http://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI). There are two steps for the Access Token process, for more details about OAuth2, please go to the [OAuth2 Documents](http://open.weibo.com/wiki/OAuth/en).

### 3.1 Get an Authentication Code
To obtain an authentication code, you need to use the [Authorization Service](http://open.weibo.com/wiki/Oauth2/authorize). For your convenience, just provide the information below and leave the `Response type` as the default value.


<form  action="https://api.weibo.com/oauth2/authorize" method="get" target="_blank">
    <label for="client_id">App Key</label>
    <input type="text" id="client_id"  name="client_id" value="">
    
    <label for="redirect_uri">Redirect URL</label>
    <input type="text" id="redirect_uri" name="redirect_uri" value="">
    
    <label for="restype" >Response type</label>
    <input type="text" id="restype" name="restype" value="code">
    
    <input type="submit" value="Submit">
</form>


With the correct information, a new page would be like this:

![weibo auth btn]({{ site.url }}/images/weibo/weibo_auth_btn.png)

Click the red `授权(Authorize)` button, and you will be redirected to the URL you have set. Copy the code in the URL to go to next step.

![weibo auth code]({{ site.url }}/images/weibo/weibo_auth_code.png)

If you have logged out the session in the previous steps, it might require you sign in your weibo account again.

### 3.2 Obtain the Access Token
To complete the final step, you could use the [Access Token Service](http://open.weibo.com/wiki/OAuth2/access_token). The `Authentication Code` comes from last step, and leave the `Grant Type` as the default value.


<form  action="https://api.weibo.com/oauth2/access_token" method="post" target="_blank">
    <label for="client_id">App Key</label>
    <input type="text" id="client_id"  name="client_id" value="">
    
    <label for="client_secret" >App Secret</label>
    <input type="text" id="client_secret" name="client_secret" value="">

    <label for="redirect_uri">Redirect URL</label>
    <input type="text" id="redirect_uri" name="redirect_uri" value="">

    <label for="grant_type" >Grant Type</label>
    <input type="text" id="grant_type" name="grant_type" value="authorization_code">

    <label for="code">Authentication Code</label>
    <input type="text" id="code"  name="code" value="">

    <input type="submit" value="Submit">
</form>

			  

If correctly, the service will return a JSON format message in a new page.

{% highlight json %}
{"access_token":"2.00biaj5GctqIhB2da047b0c47yeUcB","remind_in":"157679999","expires_in":157679999,"uid":"5862294965"}
{% endhighlight %}

The `Access Token` above would be `2.00biaj5GctqIhB2da047b0c47yeUcB`, it can last for a long time.

Right now, you have completed all the related steps. If you are interested in the API demo, please follow the next section.

> If you get some unexpected errors in above two steps, please get a new `Authentication Code` and try again!

## API Examples
In this section, I wish you can understand the following examples.

[Public Timeline](http://open.weibo.com/wiki/2/statuses/public_timeline): Return the latest public Weibos.

Give the `Access Token` in previous section, and click the Submit button.


<form  action="https://api.weibo.com/2/statuses/public_timeline.json" method="get" target="_blank">
    <label for="access_token" >Access Token</label>
    <input type="text" id="access_token" name="access_token" value="">
    <input type="submit" value="Submit">
</form>


Congratulations! Now, you are a qualified Weibo API programmer. I hope this guide would be helpful for your future life! If you have any questions, please feel free to contact with [Yecheng Tan](http://library.gwu.edu/users/ychtan).

## Reference

* [Practical guide for using Sina Weibo's API](https://www.cs.cmu.edu/~lingwang/weiboguide/)
* [So Simple Theme](https://mmistakes.github.io/so-simple-theme/)
