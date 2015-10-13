# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seed',
            old_name='platform_token',
            new_name='token',
        ),
        migrations.RenameField(
            model_name='seed',
            old_name='platform_uid',
            new_name='uid',
        ),
        migrations.RenameField(
            model_name='seedset',
            old_name='date_ended',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='seedset',
            old_name='crawl_options',
            new_name='harvest_options',
        ),
        migrations.RenameField(
            model_name='seedset',
            old_name='platform',
            new_name='harvest_type',
        ),
        migrations.RenameField(
            model_name='seedset',
            old_name='date_started',
            new_name='start_date',
        ),
    ]
