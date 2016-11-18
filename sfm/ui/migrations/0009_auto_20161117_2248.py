# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def fix_uuid(apps, schema_editor):
    Credential = apps.get_model('ui', 'Credential')
    HistoricalCredential = apps.get_model('ui', 'HistoricalCredential')
    for credential in Credential.objects.all():
        for historical_credential in HistoricalCredential.objects.filter(pk=credential.pk):
            if historical_credential.credential_id != credential.credential_id:
                historical_credential.credential_id = credential.credential_id
                historical_credential.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0008_auto_20161114_1638'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(fix_uuid, reverse_code=migrations.RunPython.noop),
    ]
