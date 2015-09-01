from django.contrib import admin as a
from ui import models as m
# Register your models here.


class Collection(a.ModelAdmin):
    fields = ('user_group', 'name', 'description', 'date_created',
              'date_updated', 'date_added', 'is_visible', 'is_active', 'stats')
    list_display = ['user_group', 'name', 'description', 'date_created',
                    'date_updated', 'date_added', 'is_visible', 'is_active',
                    'stats']
    list_filter = ['user_group', 'name', 'description', 'date_created',
                   'date_updated', 'date_added', 'is_visible', 'is_active',
                   'stats']
    search_fields = ['user_group', 'name', 'description', 'date_created',
                     'date_updated', 'date_added', 'is_visible', 'is_active',
                     'stats']

a.site.register(m.Collection, Collection)
