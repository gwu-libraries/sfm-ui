# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0017_auto_20170523_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='visibility',
            field=models.CharField(default=b'default', help_text=b'Who else can view and export from this collection. Select "All other users" to share with all Social Feed Manager users.', max_length=255, choices=[(b'default', b'Group only'), (b'local', b'All other users')]),
        ),
        migrations.AddField(
            model_name='historicalcollection',
            name='visibility',
            field=models.CharField(default=b'default', help_text=b'Who else can view and export from this collection. Select "All other users" to share with all Social Feed Manager users.', max_length=255, choices=[(b'default', b'Group only'), (b'local', b'All other users')]),
        ),
    ]
