---
layout: article
permalink: /posts/2018-03-20-twitter-command-line
title: "Command-line tools for wrangling Twitter data"
author: justin_littman 
excerpt: "A Jupyter notebook that demonstrates various command-line tools for manipulating Twitter data."
---

The source of this notebook is [available](https://github.com/gwu-libraries/notebooks/blob/master/20180320-twitter-commandline/Twitter%20command-line.ipynb).

Sure, you could write a script but you can often get the job done from the command-line.

This is an assortment of command-line tools that I use for wrangling Twitter data. Of course, most of these tools and techniques can be used for wrangle other types of data. If you have others, please let me know.

To illustrate the tools, I retrieved the tweets posted by [@gelmanlibrary](https://twitter.com/gelmanlibrary) and [@gwtweets](https://twitter.com/gwtweets) using DocNow's [Twarc](https://github.com/docnow/twarc). Twarc is a command-line tool for retrieving data from Twitter's API.

    twarc timeline gwtweets > gwtweets.jsonl
    twarc timeline gelmanlibrary > gelmanlibrary.jsonl
    
`gwtweets.jsonl` and `gelmanlibrary.jsonl` are line-oriented JSON files, i.e., tweets are in JSON, with one tweet on each line.

*Mac tip: To get Linux-like commands `brew install coreutils`*

## wc
### Count the tweets


```python
!wc -l *.jsonl
```

        3223 gelmanlibrary.jsonl
        3218 gwtweets.jsonl
        6441 total


*wc gotcha: When counting many tweets, wc -l will output a partial total and then reset the count.*

## gzip
Because of the size of the datasets that I deal with, I usually gzip compress the tweets.
### Compress a stream of tweets


```python
!cat gwtweets.jsonl | gzip > gwtweets.jsonl.gz
!cat gelmanlibrary.jsonl | gzip > gelmanlibrary.jsonl.gz
!ls *.jsonl.gz
```

    gelmanlibrary.jsonl.gz	gwtweets.jsonl.gz


### Uncompress to a stream of tweets


```python
!gunzip -c *.jsonl.gz | wc -l
```

    6441


## awk
### Sample tweets
In the following example, I create a 1 in 5 sample.


```python
!gunzip -c *.jsonl.gz | awk 'NR % 5 == 0' > sample.json
!wc -l sample.json
```

    1288 sample.json


## split
### Split tweets into files by number of tweets


```python
!gunzip -c *.jsonl.gz | split --lines=1000 -d --additional-suffix=.jsonl - tweets-
!wc -l tweets-*.jsonl
```

        1000 tweets-00.jsonl
        1000 tweets-01.jsonl
        1000 tweets-02.jsonl
        1000 tweets-03.jsonl
        1000 tweets-04.jsonl
        1000 tweets-05.jsonl
         441 tweets-06.jsonl
        6441 total


## jq
[jq](https://stedolan.github.io/jq/) excels at transforming JSON data. Because jq is such a useful tool for Twitter data, we already have several blog posts dedicated to it:
* [Getting Started Working with Twitter Data Using jq](http://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20160407-twitter-analysis-with-jq/Working-with-twitter-using-jq.ipynb)
* [Recipes for processing Twitter data with jq](http://nbviewer.jupyter.org/github/gwu-libraries/notebooks/blob/master/20161122-twitter-jq-recipes/twitter_jq_recipes.ipynb)

However, here is an example of one of its uses.

### Extract mentions


```python
!gunzip -c *.jsonl.gz | jq -r '.entities.user_mentions[].screen_name' > screen_names.txt
!head -10 screen_names.txt
```

    GWAcadTech
    Azodiac83
    gelmanlibrary
    GWtweets
    GWPeterK
    GWUSpecColl
    GWTextileMuseum
    gelmanlibrary
    GWAcadTech
    gelmanlibrary


## sort
### Sort a list
`-r` reverses the sort order (see the example for uniq).


```python
!gunzip -c *.jsonl.gz | jq -r '.entities.user_mentions[].screen_name' | sort > sorted_screen_names.txt
!head -10 sorted_screen_names.txt
```

    10p
    3PM
    60Minutes
    60Minutes
    60Minutes
    60Minutes
    60Minutes
    6pm
    8
    8nKearns


## uniq
### Get the unique values for a list
The list must be sorted first. Omit `-c` to remove counts.


```python
!gunzip -c *.jsonl.gz | jq -r '.entities.user_mentions[].screen_name' | sort | uniq -c | sort -r > unique_screen_names.txt
!head -10 unique_screen_names.txt
```

        881 gelmanlibrary
        241 GWPeterK
        240 EcklesLibrary
        133 GWtweets
        110 StudentLiaison
        104 GW_MBB
         82 GWDivIT
         81 GWToday
         78 stemworksgw
         75 GW_WBB


## tee
### Read once, write twice
In this example, I write out a lists of tweet ids and user ids.


```bash
%%bash
gunzip -c gwtweets.jsonl.gz | tee >(jq -r '.user.id_str' > gwtweets-user_ids.txt) | jq -r '.id_str' > gwtweets-tweet_ids.txt
head -5 gwtweets-tweet_ids.txt
head -5 gwtweets-user_ids.txt
```

    976161920133816322
    976147556987297794
    976144727610454016
    976141006365253632
    976139936696020993
    28101965
    28101965
    28101965
    28101965
    28101965


## parallel
parallel can really speed up processes that involve multiple files. It is also useful for repeating a task multiple times, substituting in values listed in a file.

`-j` controls the number of parallel processes. You should choose an appropriate number for the number of free CPUs available.

### gzip in parallel


```bash
%%bash
ls -1 tweets-*.jsonl > src.lst
cat src.lst | sed 's/.jsonl/.jsonl.gz/' > dest.lst
parallel -a src.lst -a dest.lst -j 2 --xapply "cat {1} | gzip > {2}"
ls tweets-*.jsonl.gz
```

    tweets-00.jsonl.gz
    tweets-01.jsonl.gz
    tweets-02.jsonl.gz
    tweets-03.jsonl.gz
    tweets-04.jsonl.gz
    tweets-05.jsonl.gz
    tweets-06.jsonl.gz


## json2csv.py
json2csv.py is a utility that is part of Twarc.


```python
!git clone https://github.com/DocNow/twarc.git
!pip install -e twarc
```

    Cloning into 'twarc'...
    remote: Counting objects: 2606, done.[K
    remote: Total 2606 (delta 0), reused 0 (delta 0), pack-reused 2606[K
    Receiving objects: 100% (2606/2606), 659.15 KiB | 3.42 MiB/s, done.
    Resolving deltas: 100% (1648/1648), done.
    Obtaining file:///Users/justinlittman/Data/notebooks/20180320-twitter-commandline/twarc
    Requirement already satisfied: pytest in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from twarc==1.3.9)
    Requirement already satisfied: python-dateutil in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from twarc==1.3.9)
    Requirement already satisfied: requests_oauthlib in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from twarc==1.3.9)
    Requirement already satisfied: pluggy<0.7,>=0.5 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from pytest->twarc==1.3.9)
    Requirement already satisfied: six>=1.10.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from pytest->twarc==1.3.9)
    Requirement already satisfied: setuptools in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from pytest->twarc==1.3.9)
    Requirement already satisfied: py>=1.5.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from pytest->twarc==1.3.9)
    Requirement already satisfied: attrs>=17.2.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from pytest->twarc==1.3.9)
    Requirement already satisfied: oauthlib>=0.6.2 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests_oauthlib->twarc==1.3.9)
    Requirement already satisfied: requests>=2.0.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests_oauthlib->twarc==1.3.9)
    Requirement already satisfied: idna<2.7,>=2.5 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests>=2.0.0->requests_oauthlib->twarc==1.3.9)
    Requirement already satisfied: urllib3<1.23,>=1.21.1 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests>=2.0.0->requests_oauthlib->twarc==1.3.9)
    Requirement already satisfied: chardet<3.1.0,>=3.0.2 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests>=2.0.0->requests_oauthlib->twarc==1.3.9)
    Requirement already satisfied: certifi>=2017.4.17 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from requests>=2.0.0->requests_oauthlib->twarc==1.3.9)
    Installing collected packages: twarc
      Found existing installation: twarc 1.3.9
        Uninstalling twarc-1.3.9:
          Successfully uninstalled twarc-1.3.9
      Running setup.py develop for twarc
    Successfully installed twarc


### Convert JSON tweets to CSV
The `-x` option produces Excel friendly CSV by removing newlines from text fields such as the tweet.


```python
!gunzip -c gwtweets.jsonl.gz | python twarc/utils/json2csv.py -x - > gwtweets.csv
!gunzip -c gelmanlibrary.jsonl.gz | python twarc/utils/json2csv.py -x - > gelmanlibrary.csv
!head -2 gwtweets.csv
```

    id,tweet_url,created_at,parsed_created_at,user_screen_name,text,tweet_type,coordinates,hashtags,media,urls,favorite_count,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id,lang,place,possibly_sensitive,retweet_count,reweet_or_quote_id,retweet_or_quote_screen_name,retweet_or_quote_user_id,source,user_id,user_created_at,user_default_profile_image,user_description,user_favourites_count,user_followers_count,user_friends_count,user_listed_count,user_location,user_name,user_statuses_count,user_time_zone,user_urls,user_verified
    976161920133816322,https://twitter.com/GWtweets/status/976161920133816322,Tue Mar 20 18:21:52 +0000 2018,2018-03-20 18:21:52+00:00,GWtweets,@AnahiHurtado_ @jaketapper 😊,reply,,,,,1,AnahiHurtado_,976161715716087809,822162726424313859,und,,,0,,,,"<a href=""http://twitter.com"" rel=""nofollow"">Twitter Web Client</a>",28101965,Wed Apr 01 13:10:09 +0000 2009,False,"The official Twitter account for the George Washington University, a university actively engaging Washington and the world.",2576,46113,1812,975,"Washington, D.C.",GW University,8689,Eastern Time (US & Canada),http://www.gwu.edu,True    
    
*Tip when loading a tweet CSV into Excel*: If you open up a tweet CSV with Excel, it will mishandle tweet and user ids. For example, 976161920133816322 will become 976161920133816000.

To correctly import tweet CSV into Excel, select Data > Get External Data > Import File. When given the option of selecting the data type for fields, select text for all id fields.

## csvkit
[csvkit](http://csvkit.readthedocs.io) supports a wide variety of operations for filtering and transforming CSV files. Here are a few highlights.


```python
!pip install csvkit
```

    Requirement already satisfied: csvkit in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages
    Requirement already satisfied: agate>=1.6.1 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from csvkit)
    Requirement already satisfied: agate-sql>=0.5.3 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from csvkit)
    Requirement already satisfied: six>=1.6.1 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from csvkit)
    Requirement already satisfied: agate-dbf>=0.2.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from csvkit)
    Requirement already satisfied: agate-excel>=0.2.2 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from csvkit)
    Requirement already satisfied: leather>=0.3.2 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: parsedatetime>=2.1 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: python-slugify>=1.2.1 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: pytimeparse>=1.1.5 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: Babel>=2.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: isodate>=0.5.4 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate>=1.6.1->csvkit)
    Requirement already satisfied: sqlalchemy>=1.0.8 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate-sql>=0.5.3->csvkit)
    Requirement already satisfied: dbfread>=2.0.5 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate-dbf>=0.2.0->csvkit)
    Requirement already satisfied: xlrd>=0.9.4 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate-excel>=0.2.2->csvkit)
    Requirement already satisfied: openpyxl>=2.3.0 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from agate-excel>=0.2.2->csvkit)
    Requirement already satisfied: future in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from parsedatetime>=2.1->agate>=1.6.1->csvkit)
    Requirement already satisfied: Unidecode>=0.04.16 in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from python-slugify>=1.2.1->agate>=1.6.1->csvkit)
    Requirement already satisfied: pytz>=0a in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from Babel>=2.0->agate>=1.6.1->csvkit)
    Requirement already satisfied: jdcal in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from openpyxl>=2.3.0->agate-excel>=0.2.2->csvkit)
    Requirement already satisfied: et-xmlfile in /Users/justinlittman/Data/notebooks/ENV/lib/python3.6/site-packages (from openpyxl>=2.3.0->agate-excel>=0.2.2->csvkit)


### Select columns


```python
!csvcut -c id,created_at,text gelmanlibrary.csv > gelmanlibrary_cut.csv
!head -3 gelmanlibrary_cut.csv
```

    id,created_at,text
    974067184249995265,Wed Mar 14 23:38:08 +0000 2018,"RT @GWAcadTech: The Instructional Technology Lab is available for support, including appointments and walk-in hours https://t.co/veLDwGcbWo…"
    973974487384363008,Wed Mar 14 17:29:48 +0000 2018,SO MANY #GWU people here to learn about GW Box today!   Attend one of our free productivity tools workshops this week at 1pm. Thu: Getting More Out Of Spreadsheets Fri: Google Forms https://t.co/hk8MfUMeit  All the cool kids are doing it. https://t.co/Gsiib3ZSZ5


### Merge CSVs


```python
!csvstack gelmanlibrary.csv gwtweets.csv > merged.csv
!wc -l *.csv
```

       3224 gelmanlibrary.csv
       3224 gelmanlibrary_cut.csv
         82 gelmanlibrary_replies_to.csv
       3219 gwtweets.csv
       6442 merged.csv
      16191 total


### Filter CSVs
Here I'm finding all of the tweets that are replies and getting the tweets to which they are replies.


```python
!csvgrep -c tweet_type -m reply gelmanlibrary.csv | csvcut -c id,in_reply_to_status_id > replies_to_in_reply_to.csv
!head -5 replies_to_in_reply_to.csv
```

    id,in_reply_to_status_id
    970826158907514880,970825298471215105
    960266436827602948,960265847108526081
    938232259173322752,938231696012562432
    938136395352289281,938135859211186176


### Join reply tweets and the tweets that are replied to
Here I'm joining some @gelmanlibrary replies to the tweets that they are a reply to.

The @gelmanlibrary reply will be on the left; the tweet that is being replied to will be on the right (with field names appended with "2").

Be careful not to use csvjoin on large CSVs.


```python
!csvjoin -c in_reply_to_status_id,id gelmanlibrary.csv gelmanlibrary_replies_to.csv > gelmanlibrary_with_replies_to.csv
!head -2 gelmanlibrary_with_replies_to.csv
```

    id,tweet_url,created_at,parsed_created_at,user_screen_name,text,tweet_type,coordinates,hashtags,media,urls,favorite_count,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id,lang,place,possibly_sensitive,retweet_count,reweet_or_quote_id,retweet_or_quote_screen_name,retweet_or_quote_user_id,source,user_id,user_created_at,user_default_profile_image,user_description,user_favourites_count,user_followers_count,user_friends_count,user_listed_count,user_location,user_name,user_statuses_count,user_time_zone,user_urls,user_verified,tweet_url2,created_at2,parsed_created_at2,user_screen_name2,text2,tweet_type2,coordinates2,hashtags2,media2,urls2,favorite_count2,in_reply_to_screen_name2,in_reply_to_status_id2,in_reply_to_user_id2,lang2,place2,possibly_sensitive2,retweet_count2,reweet_or_quote_id2,retweet_or_quote_screen_name2,retweet_or_quote_user_id2,source2,user_id2,user_created_at2,user_default_profile_image2,user_description2,user_favourites_count2,user_followers_count2,user_friends_count2,user_listed_count2,user_location2,user_name2,user_statuses_count2,user_time_zone2,user_urls2,user_verified2
    558708573853974528,https://twitter.com/gelmanlibrary/status/558708573853974528,Fri Jan 23 19:31:18 +0000 2015,2015-01-23 19:31:18+00:00,gelmanlibrary,Loving the hashtag for this class: #3WeeksofGeek How can you not want to get in on that action? http://t.co/qVsLmjmRpl @LizSetto @kal58,reply,,3WeeksofGeek,,http://fanpilgrimage.wordpress.com,1,lizsetto,558704312709558273,848710944,en,,False,0,,,,"<a href=""http://twitter.com"" rel=""nofollow"">Twitter Web Client</a>",9710852,Fri Oct 26 14:31:42 +0000 2007,False,The heart of the George Washington University,329,4023,2623,99,"Foggy Bottom, Washington, DC",gelmanlibrary,5385,Eastern Time (US & Canada),http://library.gwu.edu/,False,https://twitter.com/lizsetto/status/558704312709558273,Fri Jan 23 19:14:23 +0000 2015,2015-01-23 19:14:23+00:00,lizsetto,"Thanks for the digital sign,@gelmanlibrary! Learn more &amp; then sign up for #3WeeksOfGeek at http://t.co/hytwTvfvuh! http://t.co/JtBURjs6aZ",original,,3WeeksOfGeek,https://twitter.com/LizSetto/status/558704312709558273/photo/1,http://fanpilgrimage.wordpress.com,1,,,,en,,False,1,,,,"<a href=""http://www.apple.com"" rel=""nofollow"">iOS</a>",848710944,Thu Sep 27 05:37:12 +0000 2012,False,"Librarian, homemaker, friend of animals. 🌈✨",5133,490,640,15,"Somerville, MA",Liz Settoducato,2565,Pacific Time (US & Canada),,False


## twarc utilities
In addition to json2csv.py, Twarc includes a number of other useful tweet utilities ([docs](https://github.com/docnow/twarc#utilities) and [complete list of scripts](https://github.com/DocNow/twarc/tree/master/utils)).

Here are some of my favorites.

### tweet_compliance.py
Supports [tweet compliance](https://developer.twitter.com/en/docs/tweets/compliance/overview) by retrieving the most current versions of tweets or removing unavailable (deleted or protected)
tweets.

Also useful for splitting out deleted tweets.

### deduplicate.py
Not surpringly, deduplicates tweets. For a retweet, `--extract-retweets` will return the retweet and source tweet (i.e., the tweet that is retweeted). This is useful for extracting all of the tweets in a dataset.

### deletes.py
Attempts to determine why a tweet was deleted, e.g., tweet deleted, user protected, retweet deleted.

### unshrtn.py
Unshortens URLs contained in tweets and adds them to the tweet.
