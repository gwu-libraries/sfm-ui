# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='name6',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='name4',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='name5',
            new_name='date_updated',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='name1',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='collection',
            old_name='name2',
            new_name='user_group',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='name3',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='name7',
        ),
        migrations.AddField(
            model_name='collection',
            name='description',
            field=models.CharField(default='test', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='stats',
            field=models.CharField(default='test', max_length=225),
            preserve_default=False,
        ),
    ]
