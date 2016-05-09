# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_auto_20160509_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='stats',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
        ),
        migrations.AddField(
            model_name='historicalcollection',
            name='stats',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
        ),
        migrations.AddField(
            model_name='historicalseedset',
            name='stats',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
        ),
        migrations.AddField(
            model_name='seedset',
            name='stats',
            field=jsonfield.fields.JSONField(default=dict, blank=True),
        ),
    ]
