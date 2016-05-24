# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_auto_20160516_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='HarvestStat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('harvest_date', models.DateField()),
                ('item', models.CharField(max_length=255)),
                ('count', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='harvest',
            name='date_started',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalseedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(30, b'Every 30 minutes'), (60, b'Every hour'), (240, b'Every 4 hours'), (720, b'Every 12 hours'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
        migrations.AlterField(
            model_name='seedset',
            name='schedule_minutes',
            field=models.PositiveIntegerField(default=10080, null=True, verbose_name=b'schedule', choices=[(30, b'Every 30 minutes'), (60, b'Every hour'), (240, b'Every 4 hours'), (720, b'Every 12 hours'), (1440, b'Every day'), (10080, b'Every week'), (40320, b'Every 4 weeks'), (5, b'Every 5 minutes')]),
        ),
        migrations.AddField(
            model_name='harveststat',
            name='harvest',
            field=models.ForeignKey(related_name='harvest_stats', to='ui.Harvest'),
        ),
        migrations.AlterUniqueTogether(
            name='harveststat',
            unique_together=set([('harvest', 'harvest_date', 'item')]),
        ),
    ]
