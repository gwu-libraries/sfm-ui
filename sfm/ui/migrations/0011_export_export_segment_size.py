# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0010_auto_20161118_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='export',
            name='export_segment_size',
            field=models.BigIntegerField(default=250000, help_text=b'Number of items per file.', null=True, blank=True, choices=[(100000, b'100,000'), (250000, b'250,000'), (5000000, b'500,000'), (10000000, b'1,000,000'), (None, b'Single file'), (100, b'100')]),
        ),
    ]
