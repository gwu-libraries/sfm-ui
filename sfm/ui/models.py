from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField
from simple_history.models import HistoricalRecords
import django.db.models.options as options

# This adds an additional meta field
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (u'diff_fields',)


class User(AbstractUser):

    local_id = models.CharField(max_length=255, blank=True, default='',
                                help_text='Local identifier')


def history_save(self, *args, **kw):
    """
    A save method that skips creating a historical record if none of the
    diff fields have changed.
    """
    is_changed = False
    if self.pk is not None:
        orig = self.__class__.objects.get(pk=self.pk)
        is_changed = False
        for field in self.__class__._meta.diff_fields:
            if getattr(orig, field) != getattr(self, field):
                is_changed = True
                break

    else:
        is_changed = True

    if is_changed:
        return super(self.__class__, self).save(*args, **kw)
    else:
        self.skip_history_when_saving = True
        try:
            ret = super(self.__class__, self).save(*args, **kw)
        finally:
            del self.skip_history_when_saving
        return ret


class Credential(models.Model):
    PLATFORM_CHOICES = [
        ('twitter', 'twitter'),
        ('flickr', 'flickr'),
        ('weibo', 'weibo'),
        ('tumblr', 'tumblr')
    ]
    user = models.ForeignKey(User, related_name='credentials')
    platform = models.CharField(max_length=255, choices=PLATFORM_CHOICES)
    token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history_note = models.TextField(blank=True)
    history = HistoricalRecords()

    class Meta:
        diff_fields = ("platform", "token", "is_active")

    def __str__(self):
        return '<Credential %s "%s">' % (self.id, self.platform)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)


@python_2_unicode_compatible
class Collection(models.Model):

    group = models.ForeignKey(Group, related_name='collections')
    name = models.CharField(max_length=255, blank=False,
                            verbose_name='Collection name')
    description = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    history_note = models.TextField(blank=True)

    class Meta:
        diff_fields = ("group", "name", "description")

    def __str__(self):
        return '<Collection %s "%s">' % (self.id, self.name)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)



@python_2_unicode_compatible
class SeedSet(models.Model):
    SCHEDULE_CHOICES = [
        (60, 'Every hour'),
        (60 * 24, 'Every day'),
        (60 * 24 * 7, 'Every week'),
        (60 * 24 * 7 * 4, 'Every 4 weeks')
    ]
    HARVEST_CHOICES = [
        ('twitter_search', 'Twitter search'),
        ('twitter_filter', 'Twitter filter'),
        ('flickr_user', 'Flickr user')
    ]
    collection = models.ForeignKey(Collection, related_name='seed_sets')
    credential = models.ForeignKey(Credential, related_name='seed_sets')
    harvest_type = models.CharField(max_length=255, choices=HARVEST_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    schedule_minutes = models.PositiveIntegerField(default=60 * 24 * 7, choices=SCHEDULE_CHOICES,
                                                   verbose_name="schedule")
    harvest_options = models.TextField(blank=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(blank=True,
                                      null=True,
                                      help_text="If blank, will start now.")
    end_date = models.DateTimeField(blank=True,
                                    null=True,
                                    help_text="If blank, will continue until stopped.")
    history = HistoricalRecords()
    history_note = models.TextField(blank=True)

    class Meta:
        diff_fields = (
            "collection", "credential", "harvest_type", "name", "description", "is_active", "schedule_minutes",
            "harvest_options", "start_date", "end_date")

    def __str__(self):
        return '<SeedSet %s "%s">' % (self.id, self.name)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)


@python_2_unicode_compatible
class Seed(models.Model):

    seed_set = models.ForeignKey(SeedSet, related_name='seeds')
    token = models.TextField(blank=True)
    uid = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
    stats = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    history_note = models.TextField(blank=True)

    class Meta:
        diff_fields = ("token", "uid", "is_active")

    def __str__(self):
        return '<Seed %s "%s">' % (self.id, self.token)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)


class Harvest(models.Model):
    REQUESTED = "requested"
    SUCCESS = "completed success"
    FAILURE = "completed failure"
    RUNNING = "running"
    STATUS_CHOICES = (
        (REQUESTED, REQUESTED),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
        (RUNNING, RUNNING)
    )
    historical_seed_set = models.ForeignKey(HistoricalSeedSet, related_name='historical_harvests')
    historical_credential = models.ForeignKey(HistoricalCredential, related_name='historical_harvests')
    historical_seeds = models.ManyToManyField(HistoricalSeed, related_name='historical_harvests')
    harvest_id = models.CharField(max_length=255, blank=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    date_requested = models.DateTimeField(blank=True, default=timezone.now)
    date_started = models.DateTimeField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    stats = JSONField(blank=True)
    infos = JSONField(blank=True)
    warnings = JSONField(blank=True)
    errors = JSONField(blank=True)
    token_updates = JSONField(blank=True)
    uids = JSONField(blank=True)
    warcs_count = models.PositiveIntegerField(default=0)
    warcs_bytes = models.BigIntegerField(default=0)

    @property
    def seed_set(self):
        return self.historical_seed_set.history_object

    def __str__(self):
        return '<Harvest %s "%s">' % (self.id, self.harvest_id)


class Media(models.Model):

    harvest = models.ForeignKey(Harvest, related_name='media')
    size = models.PositiveIntegerField(default=0, help_text='Size (bytes)')
    host = models.CharField(max_length=255, blank=True)
    path = models.TextField(blank=True)
