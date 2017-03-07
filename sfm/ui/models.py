from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField
from simple_history.models import HistoricalRecords
import django.db.models.options as options
from django.conf import settings

from .utils import collection_path as get_collection_path, collection_set_path as get_collection_set_path

import uuid
import datetime
import logging
import json
import os
import shutil

log = logging.getLogger(__name__)

# This adds an additional meta field
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (u'diff_fields',)


def default_uuid():
    return uuid.uuid4().hex


class User(AbstractUser):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = "none"
    EMAIL_FREQUENCY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
        (NONE, "None")
    ]
    local_id = models.CharField(max_length=255, blank=True, default='',
                                help_text='Local identifier')
    email_frequency = models.CharField(max_length=10, choices=EMAIL_FREQUENCY_CHOICES, default=DAILY)
    harvest_notifications = models.BooleanField(default=True)

    def get_user(self):
        return self


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

    if kw.get("force_history"):
        is_changed = True
        del kw["force_history"]

    if is_changed:
        return super(self.__class__, self).save(*args, **kw)
    else:
        self.skip_history_when_saving = True
        try:
            ret = super(self.__class__, self).save(*args, **kw)
        finally:
            del self.skip_history_when_saving
        return ret


class CredentialManager(models.Manager):
    def get_by_natural_key(self, credential_id):
        return self.get(credential_id=credential_id)


class CredentialHistoryManager(models.Manager):
    def get_by_natural_key(self, credential_id, history_date):
        return self.get(credential_id=credential_id, history_date=history_date)


class CredentialHistoryModel(models.Model):
    objects = CredentialHistoryManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return self.credential_id, self.history_date


class Credential(models.Model):
    TWITTER = "twitter"
    FLICKR = "flickr"
    WEIBO = "weibo"
    TUMBLR = "tumblr"
    PLATFORM_CHOICES = [
        (TWITTER, 'Twitter'),
        (FLICKR, 'Flickr'),
        (WEIBO, 'Weibo'),
        (TUMBLR, "Tumblr")
    ]
    credential_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    name = models.CharField(max_length=255, verbose_name='Credential name')
    user = models.ForeignKey(User, related_name='credentials')
    platform = models.CharField(max_length=255, help_text='Platform name', choices=PLATFORM_CHOICES)
    token = models.TextField(blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history_note = models.TextField(blank=True)
    history = HistoricalRecords(bases=[CredentialHistoryModel])

    objects = CredentialManager()

    class Meta:
        diff_fields = ("name", "platform", "token", "is_active")

    def __str__(self):
        return '<Credential %s "%s">' % (self.id, self.platform)

    def natural_key(self):
        return self.credential_id,

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)

    def get_user(self):
        return self.user


class CollectionSetManager(models.Manager):
    def get_by_natural_key(self, collection_set_id):
        return self.get(collection_set_id=collection_set_id)


class CollectionSetHistoryModel(models.Model):
    class Meta:
        abstract = True

    def natural_key(self):
        return self.collection_set_id, self.history_date


@python_2_unicode_compatible
class CollectionSet(models.Model):
    collection_set_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    group = models.ForeignKey(Group,
                              related_name='collection_sets')
    name = models.CharField(max_length=255, blank=False,
                            verbose_name='Collection set name')
    description = models.TextField(blank=True)
    is_visible = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(bases=[CollectionSetHistoryModel])
    history_note = models.TextField(blank=True)

    objects = CollectionSetManager()

    class Meta:
        diff_fields = ("group", "name", "description")

    def __str__(self):
        return '<Collection Set %s "%s">' % (self.id, self.name)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)

    def natural_key(self):
        return self.collection_set_id,

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest__collection__collection_set=self).values("item").annotate(
                count=models.Sum("count")))

    def stats_items(self):
        """
        Returns a list of items type that have been harvested for this collection set.
        """
        return list(
            HarvestStat.objects.filter(harvest__collection__collection_set=self).values_list("item",
                                                                                             flat=True).distinct())

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
            start_date = end_date - datetime.timedelta(days=days - 1)
            date_counts = HarvestStat.objects.filter(harvest__collection__collection_set=self, item=item,
                                                     harvest_date__gte=start_date).order_by(
                "harvest_date").values("harvest_date").annotate(count=models.Sum("count"))
        else:
            date_counts = HarvestStat.objects.filter(harvest__collection__collection_set=self, item=item).order_by(
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

    def warcs_count(self):
        """
        Returns total number of WARC files harvested for this collection set.
        """
        return Harvest.objects.filter(collection__collection_set=self).aggregate(count=models.Sum("warcs_count"))[
                   "count"] or 0

    def warcs_bytes(self):
        """
        Returns total number of WARC bytes harvested for this collection set.
        """
        return Harvest.objects.filter(collection__collection_set=self).aggregate(total=models.Sum("warcs_bytes"))[
            "total"]

    def get_collection_set(self):
        return self


def delete_collection_set_receiver(sender, **kwargs):
    """
    A post_delete receiver that is triggered when Collection Set model objects are deleted.
    """
    collection_set = kwargs["instance"]

    collection_set_path = get_collection_set_path(collection_set)
    if os.path.exists(collection_set_path):
        log.info("Deleting %s", collection_set_path)
        shutil.rmtree(collection_set_path)


class CollectionManager(models.Manager):
    def get_by_natural_key(self, collection_id):
        return self.get(collection_id=collection_id)


class CollectionHistoryManager(models.Manager):
    def get_by_natural_key(self, collection_id, history_date):
        return self.get(collection_id=collection_id, history_date=history_date)


class CollectionHistoryModel(models.Model):
    objects = CollectionHistoryManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return self.collection_id, self.history_date


@python_2_unicode_compatible
class Collection(models.Model):
    TWITTER_SEARCH = 'twitter_search'
    TWITTER_FILTER = "twitter_filter"
    TWITTER_USER_TIMELINE = 'twitter_user_timeline'
    TWITTER_SAMPLE = 'twitter_sample'
    FLICKR_USER = 'flickr_user'
    WEIBO_TIMELINE = 'weibo_timeline'
    WEIBO_SEARCH = 'weibo_search'
    TUMBLR_BLOG_POSTS = 'tumblr_blog_posts'
    SCHEDULE_CHOICES = [
        (1, 'One time harvest'),
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
        (WEIBO_TIMELINE, 'Weibo timeline'),
        (TUMBLR_BLOG_POSTS, 'Tumblr blog posts')
    ]
    REQUIRED_SEED_COUNTS = {
        TWITTER_FILTER: 1,
        TWITTER_SEARCH: 1,
        WEIBO_SEARCH: 1,
        TWITTER_SAMPLE: 0,
        WEIBO_TIMELINE: 0
    }
    HARVEST_TYPES_TO_PLATFORM = {
        TWITTER_SEARCH: Credential.TWITTER,
        TWITTER_FILTER: Credential.TWITTER,
        TWITTER_USER_TIMELINE: Credential.TWITTER,
        TWITTER_SAMPLE: Credential.TWITTER,
        FLICKR_USER: Credential.FLICKR,
        WEIBO_TIMELINE: Credential.WEIBO,
        WEIBO_SEARCH: Credential.WEIBO,
        TUMBLR_BLOG_POSTS: Credential.TUMBLR
    }
    STREAMING_HARVEST_TYPES = (TWITTER_SAMPLE, TWITTER_FILTER)
    RATE_LIMITED_HARVEST_TYPES = (TWITTER_USER_TIMELINE, TWITTER_SEARCH)
    collection_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    collection_set = models.ForeignKey(CollectionSet, related_name='collections')
    credential = models.ForeignKey(Credential, related_name='collections')
    harvest_type = models.CharField(max_length=255, choices=HARVEST_CHOICES)
    name = models.CharField(max_length=255, verbose_name='Collection name')
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
    history = HistoricalRecords(bases=[CollectionHistoryModel])
    history_note = models.TextField(blank=True)

    objects = CollectionManager()

    class Meta:
        diff_fields = (
            "collection_set", "credential", "harvest_type", "name", "description", "is_active", "schedule_minutes",
            "harvest_options", "end_date")

    def __str__(self):
        return '<Collection %s "%s">' % (self.id, self.name)

    def natural_key(self):
        return self.collection_id,

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

    def last_harvest(self, include_skipped=False, include_web_harvests=False):
        """
        Returns the most recent harvest or None if no harvests.
        """
        harvests = self.harvests
        if not include_web_harvests:
            harvests = harvests.exclude(harvest_type="web")
        if not include_skipped:
            harvests = harvests.exclude(status=Harvest.SKIPPED)

        return harvests.order_by("-date_requested").first()

    def is_streaming(self):
        """
        Returns True if a streaming harvest type.
        """
        return self.harvest_type in Collection.STREAMING_HARVEST_TYPES

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest__collection=self).values("item").annotate(count=models.Sum("count")))

    def warcs_count(self):
        """
        Returns total number of WARC files harvested for this collection.
        """
        return Harvest.objects.filter(collection=self).aggregate(count=models.Sum("warcs_count"))["count"] or 0

    def warcs_bytes(self):
        """
        Returns total number of WARC bytes harvested for this collection.
        """
        return Harvest.objects.filter(collection=self).aggregate(total=models.Sum("warcs_bytes"))["total"]

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)

    def get_collection_set(self):
        return self.collection_set


def delete_collection_receiver(sender, **kwargs):
    """
    A post_delete receiver that is triggered when Collection model objects are deleted.
    """
    collection = kwargs["instance"]

    collection_path = get_collection_path(collection)
    if os.path.exists(collection_path):
        log.info("Deleting %s", collection_path)
        shutil.rmtree(collection_path)


def _item_counts_to_dict(item_counts):
    stats = {}
    for item_count in item_counts:
        stats[item_count["item"]] = item_count["count"]
    return stats


class SeedManager(models.Manager):
    def get_by_natural_key(self, seed_id):
        return self.get(seed_id=seed_id)


class SeedHistoryManager(models.Manager):
    def get_by_natural_key(self, seed_id, history_date):
        return self.get(seed_id=seed_id, history_date=history_date)


class SeedHistoryModel(models.Model):
    objects = SeedHistoryManager()

    class Meta:
        abstract = True

    def natural_key(self):
        return self.seed_id, self.history_date


@python_2_unicode_compatible
class Seed(models.Model):
    UPDATE_VIEW = "updateView"
    CREATE_VIEW = "createView"
    collection = models.ForeignKey(Collection, related_name='seeds')
    seed_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    token = models.TextField(blank=True)
    uid = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_valid = models.BooleanField(default=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(bases=[SeedHistoryModel])
    history_note = models.TextField(blank=True)

    objects = SeedManager()

    class Meta:
        diff_fields = ("token", "uid", "is_active")
        unique_together = ("collection", "uid", "token")

    def social_url(self):
        twitter_user = 'twitter_user_timeline'
        flickr_user = 'flickr_user'
        tumblr_blog = 'tumblr_blog_posts'
        twitter_user_url = "https://twitter.com/"
        flickr_user_url = 'https://www.flickr.com/photos/'
        tumblr_blog_url = '.tumblr.com'
        if twitter_user in self.collection.harvest_type and self.token:
            return twitter_user_url + self.token
        if flickr_user in self.collection.harvest_type and self.token:
            return flickr_user_url + self.token
        if tumblr_blog in self.collection.harvest_type and self.uid:
            return 'https://' + self.uid + tumblr_blog_url

    def __str__(self):
        return '<Seed %s "%s">' % (self.id, self.token)

    def save(self, *args, **kw):
        return history_save(self, *args, **kw)

    def natural_key(self):
        return self.seed_id,

    def label(self):
        labels = []
        if self.token:
            try:
                j = json.loads(self.token)
                for key, value in j.items():
                    labels.append(u"{}: {}".format(key.title(), value))
            except (AttributeError, ValueError):
                labels.append(u"Token: {}".format(self.token))
        if self.uid:
            labels.append(u"Uid: {}".format(self.uid))
        return u"; ".join(labels)

    def get_collection_set(self):
        return self.collection.collection_set


class HarvestManager(models.Manager):
    def get_by_natural_key(self, harvest_id):
        return self.get(harvest_id=harvest_id)


class Harvest(models.Model):
    REQUESTED = "requested"
    SUCCESS = "completed success"
    FAILURE = "completed failure"
    RUNNING = "running"
    VOIDED = "voided"
    STOP_REQUESTED = "stop requested"
    SKIPPED = "skipped"
    PAUSED = "paused"
    STATUS_CHOICES = (
        (REQUESTED, "Requested"),
        (SUCCESS, "Success"),
        (FAILURE, "Failure"),
        (RUNNING, "Running"),
        (STOP_REQUESTED, "Stop requested"),
        (VOIDED, "Voided"),
        (SKIPPED, "Skipped"),
        (PAUSED, "Paused")
    )
    harvest_type = models.CharField(max_length=255)
    historical_collection = models.ForeignKey(HistoricalCollection, related_name='historical_harvests', null=True)
    historical_credential = models.ForeignKey(HistoricalCredential, related_name='historical_harvests', null=True)
    historical_seeds = models.ManyToManyField(HistoricalSeed, related_name='historical_harvests')
    harvest_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    collection = models.ForeignKey(Collection, related_name='harvests')
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
    # These identify who is doing the harvest
    service = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=255, null=True)
    # Since a host may have multiple instances of a harvester, this identifies which. Might be a PID.
    instance = models.CharField(max_length=255, null=True)

    objects = HarvestManager()

    def __str__(self):
        return '<Harvest %s "%s">' % (self.id, self.harvest_id)

    def natural_key(self):
        return self.harvest_id,

    def get_harvest_type_display(self):
        return self.harvest_type.replace("_", " ").capitalize()

    def message_count(self):
        return len(self.infos) if self.infos else 0 + len(self.warnings) if self.warnings else 0 + len(
            self.errors) if self.errors else 0

    def stats(self):
        """
        Returns a dict of items to count.
        """
        return _item_counts_to_dict(
            HarvestStat.objects.filter(harvest=self).values("item").annotate(count=models.Sum("count")))

    def get_collection_set(self):
        return self.collection.collection_set


class HarvestStatManager(models.Manager):
    def get_by_natural_key(self, harvest, harvest_date, item):
        return self.get(harvest=harvest, harvest_date=harvest_date, item=item)


class HarvestStat(models.Model):
    harvest = models.ForeignKey(Harvest, related_name="harvest_stats")
    harvest_date = models.DateField()
    item = models.CharField(max_length=255)
    count = models.PositiveIntegerField()

    objects = HarvestStatManager()

    class Meta:
        unique_together = ("harvest", "harvest_date", "item")

    def natural_key(self):
        return self.harvest, self.harvest_date, self.item,

    def __str__(self):
        return '<HarvestStat %s "%s from %s">' % (self.id, self.item, self.harvest_date)


class WarcManager(models.Manager):
    def get_by_natural_key(self, warc_id):
        return self.get(warc_id=warc_id)


class Warc(models.Model):
    harvest = models.ForeignKey(Harvest, related_name='warcs')
    warc_id = models.CharField(max_length=32, unique=True)
    path = models.TextField()
    sha1 = models.CharField(max_length=42)
    bytes = models.PositiveIntegerField()
    date_created = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    objects = WarcManager()

    @property
    def harvest_type(self):
        return self.harvest.harvest_type

    def natural_key(self):
        return self.warc_id,

    def get_collection_set(self):
        return self.harvest.collection.collection_set


def delete_warc_receiver(sender, **kwargs):
    """
    A post_delete receiver that is triggered when Warc model objects are deleted.
    """
    assert kwargs["instance"]
    warc = kwargs["instance"]

    if os.path.exists(warc.path):
        log.info("Deleting %s", warc.path)
        os.remove(warc.path)
        collection_path = get_collection_path(warc.harvest.collection)
        parent_path = os.path.dirname(warc.path)
        # Also delete empty parent directories
        while len(os.listdir(parent_path)) == 0 and parent_path != collection_path:
            os.rmdir(parent_path)
            parent_path = os.path.dirname(parent_path)


class Export(models.Model):
    NOT_REQUESTED = "not requested"
    REQUESTED = "requested"
    SUCCESS = "completed success"
    FAILURE = "completed failure"
    RUNNING = "running"
    STATUS_CHOICES = (
        (NOT_REQUESTED, "Not requested"),
        (REQUESTED, "Requested"),
        (RUNNING, "Running"),
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
    SEGMENT_CHOICES = [
        (100000, "100,000"),
        (250000, "250,000"),
        (5000000, "500,000"),
        (10000000, "1,000,000"),
        (None, "Single file"),
    ]
    user = models.ForeignKey(User, related_name='exports')
    collection = models.ForeignKey(Collection, blank=True, null=True)
    seeds = models.ManyToManyField(Seed, blank=True)
    export_id = models.CharField(max_length=32, unique=True, default=default_uuid)
    export_type = models.CharField(max_length=255)
    export_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default="csv")
    export_segment_size = models.BigIntegerField(choices=SEGMENT_CHOICES, default=250000,
                                                 help_text="Number of items per file.", null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NOT_REQUESTED)
    path = models.TextField(blank=True)
    date_requested = models.DateTimeField(blank=True, null=True)
    date_started = models.DateTimeField(blank=True, null=True)
    date_ended = models.DateTimeField(blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    dedupe = models.BooleanField(blank=False, default=False)
    item_date_start = models.DateTimeField(blank=True, null=True)
    item_date_end = models.DateTimeField(blank=True, null=True)
    harvest_date_start = models.DateTimeField(blank=True, null=True)
    harvest_date_end = models.DateTimeField(blank=True, null=True)
    infos = JSONField(blank=True)
    warnings = JSONField(blank=True)
    errors = JSONField(blank=True)
    # These identify who is doing the harvest
    service = models.CharField(max_length=255, null=True)
    host = models.CharField(max_length=255, null=True)
    # Since a host may have multiple instances of a harvester, this identifies which. Might be a PID.
    instance = models.CharField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        self.path = "{}/export/{}".format(settings.SFM_DATA_DIR, self.export_id)
        super(Export, self).save(*args, **kwargs)

    def __str__(self):
        return '<Export %s "%s">' % (self.id, self.export_id)

    def get_collection_set(self):
        # Export can have a collection or seeds
        if self.collection:
            return self.collection.collection_set
        seed = self.seeds.first()
        if seed:
            return seed.get_collection_set()
        return None


def delete_export_receiver(sender, **kwargs):
    """
    A post_delete receiver that is triggered when Export model objects are deleted.
    """
    export = kwargs["instance"]

    if os.path.exists(export.path):
        log.info("Deleting %s", export.path)
        shutil.rmtree(export.path)
