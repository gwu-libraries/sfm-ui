# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='export',
            name='export_format',
            field=models.CharField(default=b'csv', max_length=10, choices=[(b'csv', b'Comma separated values (CSV)'), (b'tsv', b'Tab separated values (TSV)'), (b'html', b'HTML'), (b'xlsx', b'Excel (XLSX)'), (b'json', b'JSON of limited fields'), (b'json_full', b'Full JSON'), (b'dehydrate', b'Text file of identifiers (dehydrate)')]),
        ),
    ]
