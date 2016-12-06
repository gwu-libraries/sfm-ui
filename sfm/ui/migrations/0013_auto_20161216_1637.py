# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0012_auto_20161207_1008'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='seed',
            unique_together=set([('collection', 'uid', 'token')]),
        ),
    ]
