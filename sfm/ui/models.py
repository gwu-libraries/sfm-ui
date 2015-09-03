from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class User(AbstractUser):

    local_id = models.CharField(max_length=255, blank=True, default='',
                                help_text='Local identifier')


class Credential(models.Model):

    user = models.ForeignKey(User, related_name='credentials')
    platform = models.CharField(max_length=255, blank=True,
                                help_text='Platform name')
    token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)


@python_2_unicode_compatible
class Collection(models.Model):

    group = models.ForeignKey(Group, related_name='collections')
    name = models.CharField(max_length=255, blank=False,
                            help_text='Collection name')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Collection %s "%s">' % (self.id, self.name)


@python_2_unicode_compatible
class SeedSet(models.Model):

    collection = models.ForeignKey(Collection, related_name='seed_sets')
    credential = models.ForeignKey(Credential, related_name='seed_sets')
    platform = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    schedule = models.CharField(max_length=255, blank=True)
    crawl_options = models.TextField(blank=True)
    max_count = models.PositiveIntegerField(default=0)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_started = models.DateTimeField(default=timezone.now)
    date_ended = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<SeedSet %s "%s">' % (self.id, self.name)


@python_2_unicode_compatible
class Seed(models.Model):

    seed_set = models.ForeignKey(SeedSet, related_name='seeds')
    platform_token = models.TextField(blank=True)
    platform_uid = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Seed %s "%s">' % (self.id, self.token)


class Harvest(models.Model):

    seed_set = models.ForeignKey(SeedSet, related_name='harvests')
    stats = models.TextField(blank=True)
    date_started = models.DateTimeField(default=timezone.now)
    date_ended = models.DateTimeField(default=timezone.now)


class Media(models.Model):

    harvest = models.ForeignKey(Harvest, related_name='media')
    size = models.PositiveIntegerField(default=0, help_text='Size (bytes)')
    host = models.CharField(max_length=255, blank=True)
    path = models.TextField(blank=True)
