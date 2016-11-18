# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fix_uuid(apps, schema_editor):
    Credential = apps.get_model('ui', 'Credential')
    HistoricalCredential = apps.get_model('ui', 'HistoricalCredential')
    for credential in Credential.objects.all():
        for historical_credential in HistoricalCredential.objects.filter(id=credential.id):
            if historical_credential.credential_id != credential.credential_id:
                historical_credential.credential_id = credential.credential_id
                historical_credential.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0009_auto_20161117_2248'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(fix_uuid, reverse_code=migrations.RunPython.noop),
    ]
