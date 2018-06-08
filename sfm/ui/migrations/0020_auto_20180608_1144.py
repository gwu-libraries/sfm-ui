# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0019_auto_20180530_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='link',
            field=models.CharField(help_text=b'Link to a public version of this collection.', max_length=512, verbose_name=b'Public link', blank=True),
        ),
        migrations.AddField(
            model_name='historicalcollection',
            name='link',
            field=models.CharField(help_text=b'Link to a public version of this collection.', max_length=512, verbose_name=b'Public link', blank=True),
        ),
    ]
