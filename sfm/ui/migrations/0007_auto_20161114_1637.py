# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import uuid


def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model('ui', 'Credential')
    for row in MyModel.objects.all():
        row.credential_id = uuid.uuid4().hex
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_auto_20161114_1637'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
