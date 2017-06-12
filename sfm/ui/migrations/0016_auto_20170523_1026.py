# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0015_auto_20170426_0803'),
    ]

    operations = [
        migrations.RenameField('Collection', 'is_active', 'is_on'),
        migrations.RenameField('HistoricalCollection', 'is_active', 'is_on')
    ]
