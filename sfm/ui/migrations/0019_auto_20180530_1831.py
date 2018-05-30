# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0018_auto_20171005_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='export',
            name='export_format',
            field=models.CharField(default=b'xlsx', max_length=10, choices=[(b'xlsx', b'Excel (XLSX)'), (b'csv', b'Comma separated values (CSV)'), (b'tsv', b'Tab separated values (TSV)'), (b'json_full', b'Full JSON'), (b'json', b'JSON of limited fields'), (b'dehydrate', b'Text file of identifiers (dehydrate)')]),
        ),
        migrations.AlterField(
            model_name='export',
            name='export_segment_size',
            field=models.BigIntegerField(default=250000, null=True, blank=True, choices=[(100000, b'100,000'), (250000, b'250,000'), (500000, b'500,000'), (100000, b'1,000,000'), (None, b'Single file')]),
        ),
    ]
