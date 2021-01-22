from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site

import os
from os import environ as env
from itertools import islice, chain
import logging

log = logging.getLogger(__name__)


class Diff:
    def __init__(self):
        self.obj = None
        self.user = None
        self.date = None
        self.note = None
        self.fields = {}


def diff_historical_objects(original_historical_object, changed_historical_object):
    """
    Performs a diff between two historical objects to determine which fields have changed.

    The historical_object must have a HistoricalRecord attribute named history, a
    TextField named history_note, and
    a Meta field named diff_fields containing a list of field names to diff.
    :param original_historical_object: the original historical object
    :param changed_historical_object: the changed historical object
    :return: a Diff
    """
    diff = Diff()
    diff.obj = changed_historical_object.instance
    diff.date = changed_historical_object.history_date
    diff.user = changed_historical_object.history_user
    diff.note = changed_historical_object.history_note
    for field in changed_historical_object.history_object._meta.diff_fields:
        try:
            value = getattr(changed_historical_object, field)
        except ObjectDoesNotExist:
            value = "Deleted"
        if value == "":
            value = None
        try:
            original_value = getattr(original_historical_object, field) if original_historical_object else None
        except ObjectDoesNotExist:
            original_value = "Deleted"
        if original_value == "":
            original_value = None
        if value != original_value:
            diff.fields[field] = (original_value, value)
    return diff


def diff_historical_object(historical_object):
    try:
        prev_historical_object = historical_object.get_previous_by_history_date(id=historical_object.id)
    except ObjectDoesNotExist:
        prev_historical_object = None
    return diff_historical_objects(prev_historical_object, historical_object)


class CollectionHistoryIter(object):
    def __init__(self, collection_historical_objs, seed_historical_objs):
        self.collection_historical_objs = collection_historical_objs
        self.seed_historical_objs = seed_historical_objs
        self.iter = self._merge_history_objs(collection_historical_objs.iterator(), seed_historical_objs.iterator())
        self.len = len(collection_historical_objs) + len(seed_historical_objs)

    def __len__(self):
        return self.len

    def __getitem__(self, given):
        if isinstance(given, slice):
            # do your handling for a slice object:
            return list(islice(self.iter, given.start, given.stop, given.step))
        else:
            return list(islice(self.iter, given, given + 1))[0]

    @staticmethod
    def _merge_history_objs(collection_historical_objs, seed_historical_objs):
        next_collection_historical_obj = CollectionHistoryIter._next_historical_obj(collection_historical_objs)
        next_seed_historical_obj = CollectionHistoryIter._next_historical_obj(seed_historical_objs)
        while next_collection_historical_obj is not None or next_seed_historical_obj is not None:
            if next_collection_historical_obj is not None and next_seed_historical_obj is not None:
                if next_collection_historical_obj.history_date > next_seed_historical_obj.history_date:
                    ret_historical_obj = next_collection_historical_obj
                    next_collection_historical_obj = CollectionHistoryIter._next_historical_obj(
                        collection_historical_objs)
                    yield ret_historical_obj
                else:
                    ret_historical_obj = next_seed_historical_obj
                    next_seed_historical_obj = CollectionHistoryIter._next_historical_obj(seed_historical_objs)
                    yield ret_historical_obj
            elif next_collection_historical_obj is None:
                ret_historical_obj = next_seed_historical_obj
                next_seed_historical_obj = CollectionHistoryIter._next_historical_obj(seed_historical_objs)
                yield ret_historical_obj
            else:
                ret_historical_obj = next_collection_historical_obj
                next_collection_historical_obj = CollectionHistoryIter._next_historical_obj(collection_historical_objs)
                yield ret_historical_obj

    @staticmethod
    def _next_historical_obj(objs):
        if objs is None:
            return None
        try:
            return next(objs)
        except StopIteration:
            return None


def diff_object_history(obj):
    """
    Performs a diff on all of an object's historical objects.
    :param obj: the object which has a history
    :return: a list of Diffs, from most recent historical object backwards
    """
    diffs = []
    historical_objects = list(obj.history.all())
    for i, historical_object in enumerate(historical_objects):
        diffs.append(diff_historical_objects(historical_objects[i + 1] if i < len(historical_objects) - 1 else None,
                                             historical_object))
    return diffs


def diff_collection_and_seeds_history(collection):
    """
    Performs a diff on a collection and its seeds historical objects
    :param collection: the collection
    :return: a list of Diffs, from most recent historical objects backwards
    """
    diffs = [diff_object_history(collection)]
    for seed in collection.seeds.all():
        diffs.append(diff_object_history(seed))
    ret = sorted(chain(*diffs), key=lambda diff: diff.date, reverse=True)
    return ret


def diff_field_changed(obj):
    """
    Returns True if a diff field was changed the last time this object was saved.

    This is determined by comparing the date_updated fields of the object and
    the first historical object.
    :param obj: the object which has a history
    :return: True if a diff field was changed
    """
    first_object_history = obj.history.first()
    return first_object_history and obj.date_updated == first_object_history.date_updated


def clean_token(token):
    """
    Cleans a token such as a Twitter screen name.
    """
    if token is None:
        return None
    # all save as lowercase
    stripped_token = token.strip()
    return stripped_token[1:] if stripped_token.startswith('@') else stripped_token


def clean_blogname(blogname):
    """
    Cut of the 'tumblr.com'
    :param blogname:
    :return: short blogname
    """
    if blogname is None:
        return None
    stripped_blogname = blogname.strip()
    return stripped_blogname[:-11] if stripped_blogname.endswith('.tumblr.com') else stripped_blogname


def collection_path(collection, sfm_data_dir=None):
    return collection_path_by_id(collection.collection_set.collection_set_id, collection.collection_id,
                                 sfm_data_dir=sfm_data_dir)


def collection_path_by_id(collection_set_id, collection_id, sfm_data_dir=None):
    return os.path.join(sfm_data_dir or settings.SFM_COLLECTION_SET_DATA_DIR, "collection_set",
                        collection_set_id,
                        collection_id)


def collection_set_path(collection_set, sfm_data_dir=None):
    return collection_set_path_by_id(collection_set.collection_set_id, sfm_data_dir=sfm_data_dir)


def collection_set_path_by_id(collection_set_id, sfm_data_dir=None):
    return os.path.join(sfm_data_dir or settings.SFM_COLLECTION_SET_DATA_DIR, "collection_set", collection_set_id)


def get_email_addresses_for_collection_set(collection_set, use_harvest_notification_preference=False,
                                           include_admins=False):
    """
    Get the email addresses of users associated with a collection set.
    """
    email_addresses = []
    for user in collection_set.group.user_set.all():
        if user.email and (not use_harvest_notification_preference or user.harvest_notifications):
            email_addresses.append(user.email)
    if include_admins:
        email_addresses.extend(get_admin_email_addresses())
    return email_addresses


def get_admin_email_addresses():
    email_addresses = []
    for _, email_address in settings.ADMINS:
        email_addresses.append(email_address)
    return email_addresses


def get_site_url():
    return '{}://{}'.format("https" if env.get('SFM_USE_HTTPS', 'False').lower() == 'true' else "http",
                            Site.objects.get_current().domain)
