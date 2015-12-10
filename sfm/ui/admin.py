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


class Credential(a.ModelAdmin):
    fields = ('user', 'platform', 'token', 'is_active', 'date_added')
    list_display = ['user', 'platform', 'token', 'is_active', 'date_added']
    list_filter = ['user', 'platform', 'token', 'is_active', 'date_added']
    search_fields = ['user', 'platform', 'token', 'is_active', 'date_added']


class Collection(a.ModelAdmin):
    fields = ('group', 'name', 'description', 'is_active', 'is_visible',
              'stats', 'date_added')
    list_display = ['group', 'name', 'description', 'is_active', 'is_visible',
                    'stats', 'date_added', 'date_updated']
    list_filter = ['group', 'name', 'description', 'is_active', 'is_visible',
                   'stats', 'date_added', 'date_updated']
    search_fields = ['group', 'name', 'description', 'is_active',
                     'is_visible', 'stats', 'date_added', 'date_updated']


class SeedSet(a.ModelAdmin):
    fields = ('collection', 'credential', 'harvest_type', 'name',
              'description', 'is_active', 'schedule', 'harvest_options',
              'max_count', 'stats', 'date_added', 'start_date', 'end_date')
    list_display = ['collection', 'credential', 'harvest_type', 'name',
                    'description', 'is_active', 'schedule', 'harvest_options',
                    'max_count', 'stats', 'date_added', 'start_date',
                    'end_date']
    list_filter = ['collection', 'credential', 'harvest_type', 'name',
                   'description', 'is_active', 'schedule', 'harvest_options',
                   'max_count', 'stats', 'date_added', 'start_date',
                   'end_date']
    search_fields = ['collection', 'credential', 'harvest_type', 'name',
                     'description', 'is_active', 'schedule',
                     'harvest_options', 'max_count', 'stats', 'date_added',
                     'start_date', 'end_date']


class Seed(a.ModelAdmin):
    fields = ('seed_set', 'token', 'uid', 'is_active',
              'is_valid', 'stats', 'date_added')
    list_display = ['seed_set', 'token', 'uid', 'is_active',
                    'is_valid', 'stats', 'date_added', 'date_updated']
    list_filter = ['seed_set', 'token', 'uid', 'is_active',
                   'is_valid', 'stats', 'date_added', 'date_updated']
    search_fields = ['seed_set', 'token', 'uid', 'is_active',
                     'is_valid', 'stats', 'date_added', 'date_updated']

a.site.register(m.Credential, Credential)
a.site.register(m.Collection, Collection)
a.site.register(m.SeedSet, SeedSet)
a.site.register(m.Seed, Seed)
