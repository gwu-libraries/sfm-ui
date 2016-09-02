# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0002_auto_20160720_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_frequency',
            field=models.CharField(default=b'daily', max_length=10, choices=[(b'daily', b'Daily'), (b'weekly', b'Weekly'), (b'monthly', b'Monthly'), (b'none', b'None')]),
        ),
        migrations.AlterField(
            model_name='collection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_sample', b'Twitter sample'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline'), (b'tumblr_blog_posts', b'Tumblr blog posts')]),
        ),
        migrations.AlterField(
            model_name='credential',
            name='platform',
            field=models.CharField(help_text=b'Platform name', max_length=255, choices=[(b'twitter', b'Twitter'), (b'flickr', b'Flickr'), (b'weibo', b'Weibo'), (b'tumblr', b'Tumblr')]),
        ),
        migrations.AlterField(
            model_name='historicalcollection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_sample', b'Twitter sample'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline'), (b'tumblr_blog_posts', b'Tumblr blog posts')]),
        ),
        migrations.AlterField(
            model_name='historicalcredential',
            name='platform',
            field=models.CharField(help_text=b'Platform name', max_length=255, choices=[(b'twitter', b'Twitter'), (b'flickr', b'Flickr'), (b'weibo', b'Weibo'), (b'tumblr', b'Tumblr')]),
        ),
    ]
