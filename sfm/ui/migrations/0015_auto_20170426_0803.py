# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0014_auto_20170113_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_sample', b'Twitter sample'), (b'tumblr_blog_posts', b'Tumblr blog posts'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline')]),
        ),
        migrations.AlterField(
            model_name='harvest',
            name='status',
            field=models.CharField(default=b'requested', max_length=20, choices=[(b'requested', b'Requested'), (b'completed success', b'Success'), (b'completed failure', b'Completed with errors'), (b'running', b'Running'), (b'stop requested', b'Stop requested'), (b'stopping', b'Stopping'), (b'voided', b'Voided'), (b'skipped', b'Skipped'), (b'paused', b'Paused')]),
        ),
        migrations.AlterField(
            model_name='historicalcollection',
            name='harvest_type',
            field=models.CharField(max_length=255, choices=[(b'twitter_user_timeline', b'Twitter user timeline'), (b'twitter_search', b'Twitter search'), (b'twitter_filter', b'Twitter filter'), (b'twitter_sample', b'Twitter sample'), (b'tumblr_blog_posts', b'Tumblr blog posts'), (b'flickr_user', b'Flickr user'), (b'weibo_timeline', b'Weibo timeline')]),
        ),
    ]
