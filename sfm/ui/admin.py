from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin as a
from ui import models as m
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserCreationForm(UserCreationForm):

    error_message = UserCreationForm.error_messages.update({
        'duplicate_local_id': 'This local_id has already been taken.'
    })

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_local_id(self):
        local_id = self.cleaned_data["local_id"]
        try:
            User.objects.get(local_id=local_id)
        except User.DoesNotExist:
            return local_id
        raise forms.ValidationError(self.error_messages['duplicate_local_id'])


@a.register(User)
class UserAdmin(AuthUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = AuthUserAdmin.fieldsets + (
        (None, {'fields': ('email_frequency',)}),
    )


class Credential(a.ModelAdmin):
    fields = ('user', 'platform', 'name', 'token', 'is_active', 'date_added', 'history_note')
    list_display = ['user', 'platform', 'name', 'is_active', 'date_added']
    list_filter = ['user', 'platform', 'is_active', 'date_added']
    search_fields = ['user', 'platform', 'name', 'is_active', 'date_added']


class HistoricalCredential(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'user', 'platform', 'token', 'is_active', 'date_added')
    list_display = ['user', 'platform', 'token', 'is_active', 'date_added']
    list_filter = ['user', 'platform', 'token', 'is_active', 'date_added']
    search_fields = ['user', 'platform', 'token', 'is_active', 'date_added']


class CollectionSet(a.ModelAdmin):
    fields = ('collection_set_id', 'group', 'name', 'description', 'is_visible',
              'date_added', 'history_note')
    list_display = ['group', 'name', 'description', 'is_visible',
                    'date_added', 'date_updated']
    list_filter = ['group', 'name', 'description', 'is_visible',
                   'date_added', 'date_updated']
    search_fields = ['group', 'name', 'description',
                     'is_visible', 'date_added', 'date_updated']


class HistoricalCollectionSet(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'collection_set_id', 'group', 'name',
              'description', 'is_visible', 'date_added')
    list_display = ['group', 'name', 'description', 'is_visible',
                    'date_added', 'date_updated']
    list_filter = ['group', 'name', 'description', 'is_visible',
                   'date_added', 'date_updated']
    search_fields = ['group', 'name', 'description',
                     'is_visible', 'date_added', 'date_updated']


class Collection(a.ModelAdmin):
    fields = ('collection_id', 'collection_set', 'credential', 'harvest_type', 'name',
              'description', 'is_active', 'schedule_minutes', 'harvest_options',
              'date_added', 'end_date', 'history_note')
    list_display = ['collection_set', 'credential', 'harvest_type', 'name',
                    'description', 'is_active', 'harvest_options',
                    'date_added', 'end_date']
    list_filter = ['collection_set', 'credential', 'harvest_type', 'name',
                   'description', 'is_active', 'harvest_options',
                   'date_added', 'end_date']
    search_fields = ['collection_set', 'credential', 'harvest_type', 'name',
                     'description', 'is_active',
                     'harvest_options', 'date_added', 'end_date']


class HistoricalCollection(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'collection_set', 'credential', 'harvest_type', 'name',
              'description', 'is_active', 'schedule_minutes', 'harvest_options',
              'date_added', 'end_date')
    list_display = ['collection_set', 'credential', 'harvest_type', 'name',
                    'description', 'is_active', 'harvest_options',
                    'date_added', 'end_date']
    list_filter = ['collection_set', 'credential', 'harvest_type', 'name',
                   'description', 'is_active', 'harvest_options',
                   'date_added', 'end_date']
    search_fields = ['collection_set', 'credential', 'harvest_type', 'name',
                     'description', 'is_active',
                     'harvest_options', 'date_added', 'end_date']


class Seed(a.ModelAdmin):
    fields = ('seed_id', 'collection', 'token', 'uid', 'is_active',
              'is_valid', 'date_added', 'history_note')
    list_display = ['collection', 'token', 'uid', 'is_active',
                    'is_valid', 'date_added', 'date_updated']
    list_filter = ['collection', 'token', 'uid', 'is_active',
                   'is_valid', 'date_added', 'date_updated']
    search_fields = ['collection', 'token', 'uid', 'is_active',
                     'is_valid', 'date_added', 'date_updated']


class HistoricalSeed(a.ModelAdmin):
    fields = ('history_user', 'history_date', 'history_note', 'seed_id', 'collection', 'token', 'uid', 'is_active',
              'is_valid', 'date_added')
    list_display = ['collection', 'token', 'uid', 'is_active',
                    'is_valid', 'date_added', 'date_updated']
    list_filter = ['collection', 'token', 'uid', 'is_active',
                   'is_valid', 'date_added', 'date_updated']
    search_fields = ['collection', 'token', 'uid', 'is_active',
                     'is_valid', 'date_added', 'date_updated']


class Harvest(a.ModelAdmin):
    fields = (
       'harvest_type', 'harvest_id', 'historical_collection', 'historical_seeds', 'historical_credential',
       'parent_harvest', 'status', 'date_requested', 'date_started', 'date_ended',
       'infos', 'warnings', 'errors', 'token_updates', 'uids', 'warcs_count', 'warcs_bytes',
       'service', 'host', 'instance')
    list_display = ['harvest_type', 'id', 'harvest_id', 'historical_collection', 'status', 'date_requested',
                    'date_updated']
    list_filter = ['harvest_type', 'status', 'date_requested', 'date_updated']
    search_fields = ['id', 'harvest_id']


class HarvestStat(a.ModelAdmin):
    fields = (
        'harvest', 'harvest_date', 'item', 'count'
    )
    list_display = (
        'harvest', 'harvest_date', 'item', 'count'
    )
    list_filter = ['harvest_date', 'item']
    search_fields = []


class Warc(a.ModelAdmin):
    fields = (
       'warc_id', 'harvest', 'path', 'sha1', 'bytes', 'date_created')
    list_display = ['id', 'warc_id', 'harvest', 'date_created']
    list_filter = ['date_created']
    search_fields = ['id', 'warc_id', 'path']


class Export(a.ModelAdmin):
    fields = (
       'user', 'collection', 'seeds', 'export_id', 'export_type', 'export_format',
       'status', 'path', 'date_requested', 'date_started', 'date_ended', 'dedupe',
       'item_date_start', 'item_date_end', 'harvest_date_start', 'harvest_date_end',
       'infos', 'warnings', 'errors', 'service', 'host', 'instance')
    list_display = ['id', 'user', 'export_type', 'date_requested', 'status']
    list_filter = ['date_requested', 'user', 'export_type', 'status']
    search_fields = ['id', 'export_id', 'path']

a.site.register(m.Credential, Credential)
a.site.register(m.HistoricalCredential, HistoricalCredential)
a.site.register(m.CollectionSet, CollectionSet)
a.site.register(m.HistoricalCollectionSet, HistoricalCollectionSet)
a.site.register(m.Collection, Collection)
a.site.register(m.HistoricalCollection, HistoricalCollection)
a.site.register(m.Seed, Seed)
a.site.register(m.HistoricalSeed, HistoricalSeed)
a.site.register(m.Harvest, Harvest)
a.site.register(m.HarvestStat, HarvestStat)
a.site.register(m.Warc, Warc)
a.site.register(m.Export, Export)
