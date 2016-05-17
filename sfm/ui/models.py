from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField
from simple_history.models import HistoricalRecords
import django.db.models.options as options
from django.conf import settings

import uuid
import datetime
import pytz
import logging

log = logging.getLogger(__name__)

# This adds an additional meta field
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (u'diff_fields',)


def default_uuid():
    return uuid.uuid4().hex


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
    TWITTER = "twitter"
    FLICKR = "flickr"
    WEIBO = "weibo"
    PLATFORM_CHOICES = [
        (TWITTER, 'Twitter'),
        (FLICKR, 'Flickr'),
        (WEIBO, 'Weibo')
    ]
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='credentials')
    platform = models.CharField(max_length=255, help_text='Platform name', choices=PLATFORM_CHOICES)
    token = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history_note = models.TextField(blank=True)
    history = HistoricalRecords()

    class Meta:
        diff_fields = ("name", "platform", "token", "is_active")

    def __str__(self):
        return '<Credential %s "%s">' % (self.id, self.platform)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)


@python_2_unicode_compatible
class Collection(models.Model):
    collection_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    group = models.ForeignKey(Group, related_name='collections')
    name = models.CharField(max_length=255, blank=False,
                            verbose_name='Collection name')
    description = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
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

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest__seed_set__collection=self).values("item").annotate(
                count=models.Sum("count")))

    def stats_items(self):
        """
        Returns a list of items type that have been harvested for this collection.
        """
        return list(
            HarvestStat.objects.filter(harvest__seed_set__collection=self).values_list("item", flat=True).distinct())

    def item_stats(self, item, days=7, end_date=None):
        """
        Gets count of items harvested by date.

        If there are no items for a day, a date, count (of 0) pair is still returned.

        :param item: name of the item to get count for, e.g., tweet.
        :param days: backwards from end_datetime, the number of days to retrieve.
        :param end_date: the date to start backfrom from. Default is today.
        :return: List of date, count pairs.
        """
        if end_date is None:
            end_date = datetime.date.today()

        if days:
            start_date = end_date - datetime.timedelta(days=days-1)
            date_counts = HarvestStat.objects.filter(harvest__seed_set__collection=self, item=item,
                                                     harvest_date__gte=start_date).order_by(
                "harvest_date").values("harvest_date").annotate(count=models.Sum("count"))
        else:
            date_counts = HarvestStat.objects.filter(harvest__seed_set__collection=self, item=item).order_by(
                "harvest_date").values("harvest_date").annotate(count=models.Sum("count"))
            if len(date_counts) > 0:
                days = (end_date - date_counts[0]["harvest_date"]).days + 1
            else:
                days = 1
            start_date = end_date - datetime.timedelta(days=days - 1)

        date_counts_dict = {}
        for date_count in date_counts:
            date_counts_dict[date_count["harvest_date"]] = date_count["count"]

        stats = []
        for i in range(days):
            date = start_date + datetime.timedelta(days=i)
            stats.append((date, date_counts_dict.get(date, 0)))
        return stats

@python_2_unicode_compatible
class SeedSet(models.Model):
    TWITTER_SEARCH = 'twitter_search'
    TWITTER_FILTER = "twitter_filter"
    TWITTER_USER_TIMELINE = 'twitter_user_timeline'
    TWITTER_SAMPLE = 'twitter_sample'
    FLICKR_USER = 'flickr_user'
    WEIBO_TIMELINE = 'weibo_timeline'
    SCHEDULE_CHOICES = [
        (30, 'Every 30 minutes'),
        (60, 'Every hour'),
        (60 * 4, 'Every 4 hours'),
        (60 * 12, 'Every 12 hours'),
        (60 * 24, 'Every day'),
        (60 * 24 * 7, 'Every week'),
        (60 * 24 * 7 * 4, 'Every 4 weeks')
    ]
    HARVEST_CHOICES = [
        (TWITTER_SEARCH, 'Twitter search'),
        (TWITTER_FILTER, 'Twitter filter'),
        (TWITTER_USER_TIMELINE, 'Twitter user timeline'),
        (TWITTER_SAMPLE, 'Twitter sample'),
        (FLICKR_USER, 'Flickr user'),
        (WEIBO_TIMELINE, 'Weibo timeline')
    ]
    REQUIRED_SEED_COUNTS = {
        TWITTER_FILTER: 1,
        TWITTER_SEARCH: 1,
        TWITTER_SAMPLE: 0,
        WEIBO_TIMELINE: 0
    }
    HARVEST_TYPES_TO_PLATFORM = {
        TWITTER_SEARCH: Credential.TWITTER,
        TWITTER_FILTER: Credential.TWITTER,
        TWITTER_USER_TIMELINE: Credential.TWITTER,
        TWITTER_SAMPLE: Credential.TWITTER,
        FLICKR_USER: Credential.FLICKR,
        WEIBO_TIMELINE: Credential.WEIBO
    }
    STREAMING_HARVEST_TYPES = (TWITTER_SAMPLE, TWITTER_FILTER)
    seedset_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    collection = models.ForeignKey(Collection, related_name='seed_sets')
    credential = models.ForeignKey(Credential, related_name='seed_sets')
    harvest_type = models.CharField(max_length=255, choices=HARVEST_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    schedule_minutes = models.PositiveIntegerField(default=60 * 24 * 7, choices=SCHEDULE_CHOICES,
                                                   verbose_name="schedule", null=True)
    harvest_options = models.TextField(blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(blank=True,
                                    null=True,
                                    help_text="If blank, will continue until stopped.")
    history = HistoricalRecords()
    history_note = models.TextField(blank=True)

    class Meta:
        diff_fields = (
            "collection", "credential", "harvest_type", "name", "description", "is_active", "schedule_minutes",
            "harvest_options", "end_date")

    def __str__(self):
        return '<SeedSet %s "%s">' % (self.id, self.name)

    def required_seed_count(self):
        """
        Returns the number of seeds that are required for this harvest type.

        If None, then 1 or more is required.
        """
        return self.REQUIRED_SEED_COUNTS.get(str(self.harvest_type))

    def active_seed_count(self):
        """
        Returns the number of active seeds.
        """
        return self.seeds.filter(is_active=True).count()

    def last_harvest(self):
        """
        Returns the most recent harvest or None if no harvests.

        Web harvests are excluded.
        """
        return self.harvests.exclude(harvest_type="web").order_by("-date_requested").first()

    def is_streaming(self):
        """
        Returns True if a streaming harvest type.
        """
        return self.harvest_type in SeedSet.STREAMING_HARVEST_TYPES

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest__seed_set=self).values("item").annotate(count=models.Sum("count")))

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)


def _item_counts_to_dict(item_counts):
    stats = {}
    for item_count in item_counts:
        stats[item_count["item"]] = item_count["count"]
    return stats


@python_2_unicode_compatible
class Seed(models.Model):
    seed_set = models.ForeignKey(SeedSet, related_name='seeds')
    seed_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    token = models.TextField(blank=True)
    uid = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
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
    STOP_REQUESTED = "stop requested"
    STATUS_CHOICES = (
        (REQUESTED, "Requested"),
        (SUCCESS, "Success"),
        (FAILURE, "Failure"),
        (RUNNING, "Running"),
        (STOP_REQUESTED, "Stop requested")
    )
    harvest_type = models.CharField(max_length=255)
    historical_seed_set = models.ForeignKey(HistoricalSeedSet, related_name='historical_harvests', null=True)
    historical_credential = models.ForeignKey(HistoricalCredential, related_name='historical_harvests', null=True)
    historical_seeds = models.ManyToManyField(HistoricalSeed, related_name='historical_harvests')
    harvest_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    harvest_type = models.CharField(max_length=255)
    seed_set = models.ForeignKey(SeedSet, related_name='harvests')
    parent_harvest = models.ForeignKey("self", related_name='child_harvests', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
    date_requested = models.DateTimeField(blank=True, default=timezone.now)
    date_started = models.DateTimeField(blank=True, null=True, db_index=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    infos = JSONField(blank=True)
    warnings = JSONField(blank=True)
    errors = JSONField(blank=True)
    token_updates = JSONField(blank=True)
    uids = JSONField(blank=True)
    warcs_count = models.PositiveIntegerField(default=0)
    warcs_bytes = models.BigIntegerField(default=0)

    def __str__(self):
        return '<Harvest %s "%s">' % (self.id, self.harvest_id)

    def get_harvest_type_display(self):
        return self.harvest_type.replace("_", " ").capitalize()

    def message_count(self):
        return len(self.infos) if self.infos else 0 \
                                                  + len(self.warnings) if self.warnings else 0 \
                                                                                             + len(
            self.errors) if self.errors else 0

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest=self).values("item").annotate(count=models.Sum("count")))


class HarvestStat(models.Model):
    harvest = models.ForeignKey(Harvest, related_name="harvest_stats")
    harvest_date = models.DateField()
    item = models.CharField(max_length=255)
    count = models.PositiveIntegerField()

    class Meta:
        unique_together = ("harvest", "harvest_date", "item")

    def __str__(self):
        return '<HarvestStat %s "%s from %s">' % (self.id, self.item, self.harvest_date)


class Warc(models.Model):
    harvest = models.ForeignKey(Harvest, related_name='warcs')
    warc_id = models.CharField(max_length=32, unique=True)
    path = models.TextField()
    sha1 = models.CharField(max_length=42)
    bytes = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


class Export(models.Model):
    NOT_REQUESTED = "not requested"
    REQUESTED = "requested"
    SUCCESS = "completed success"
    FAILURE = "completed failure"
    STATUS_CHOICES = (
        (NOT_REQUESTED, "Not requested"),
        (REQUESTED, "Requested"),
        (SUCCESS, "Success"),
        (FAILURE, "Failure")
    )
    FORMAT_CHOICES = (
        ("csv", "Comma separated values (CSV)"),
        ("tsv", "Tab separated values (TSV)"),
        ("html", "HTML"),
        ("xlsx", "Excel (XLSX)"),
        ("json", "JSON of limited fields"),
        ("json_full", "Full JSON"),
        ("dehydrate", "Text file of identifiers (dehydrate)")
    )
    user = models.ForeignKey(User, related_name='exports')
    seed_set = models.ForeignKey(SeedSet, blank=True, null=True)
    seeds = models.ManyToManyField(Seed, blank=True)
    export_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    export_type = models.CharField(max_length=255)
    export_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default="csv")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_REQUESTED)
    path = models.TextField(blank=True)
    date_requested = models.DateTimeField(blank=True, null=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    dedupe = models.BooleanField(blank=False, default=False)
    item_date_start = models.DateTimeField(blank=True, null=True)
    item_date_end = models.DateTimeField(blank=True, null=True)
    harvest_date_start = models.DateTimeField(blank=True, null=True)
    harvest_date_end = models.DateTimeField(blank=True, null=True)
    infos = JSONField(blank=True)
    warnings = JSONField(blank=True)
    errors = JSONField(blank=True)

    def save(self, *args, **kwargs):
        self.path = "{}/export/{}".format(settings.SFM_DATA_DIR, self.export_id)
        super(Export, self).save(*args, **kwargs)

    def __str__(self):
        return '<Export %s "%s">' % (self.id, self.export_id)
