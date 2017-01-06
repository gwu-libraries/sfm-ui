# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0013_auto_20161216_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_sample', b'Twitter sample'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline'), (b'weibo_search', b'Weibo search'), (b'tumblr_blog_posts', b'Tumblr blog posts')]),
        ),
        migrations.AlterField(
            model_name='historicalcollection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_sample', b'Twitter sample'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline'), (b'weibo_search', b'Weibo search'), (b'tumblr_blog_posts', b'Tumblr blog posts')]),
        ),
    ]
