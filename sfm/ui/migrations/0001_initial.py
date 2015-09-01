# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name1', models.CharField(max_length=25)),
                ('name2', models.CharField(max_length=25)),
                ('name3', models.CharField(max_length=25)),
                ('name4', models.CharField(max_length=25)),
                ('name5', models.CharField(max_length=25)),
                ('name6', models.CharField(max_length=25)),
                ('name7', models.CharField(max_length=25)),
            ],
        ),
    ]
