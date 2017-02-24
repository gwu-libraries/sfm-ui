from django.conf import settings

import os
from itertools import chain


class Diff:
    def __init__(self):
        self.obj = None
        self.user = None
        self.date = None
        self.note = None
        self.fields = {}


def diff_historical_object(original_historical_object, changed_historical_object):
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
        value = getattr(changed_historical_object, field)
        if value == "":
            value = None
        original_value = getattr(original_historical_object, field) if original_historical_object else None
        if original_value == "":
            original_value = None
        if value != original_value:
            diff.fields[field] = (original_value, value)
    return diff


def diff_object_history(obj):
    """
    Performs a diff on all of an object's historical objects.
    :param obj: the object which has a history
    :return: a list of Diffs, from most recent historical object backwards
    """
    diffs = []
    historical_objects = list(obj.history.all())
    for i, historical_object in enumerate(historical_objects):
        diffs.append(diff_historical_object(historical_objects[i + 1] if i < len(historical_objects) - 1 else None,
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
    return sorted(chain(*diffs), key=lambda diff: diff.date, reverse=True)


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
    return os.path.join(sfm_data_dir or settings.SFM_DATA_DIR, "collection_set",
                        collection_set_id,
                        collection_id)


def collection_set_path(collection_set, sfm_data_dir=None):
    return collection_set_path_by_id(collection_set.collection_set_id, sfm_data_dir=sfm_data_dir)


def collection_set_path_by_id(collection_set_id, sfm_data_dir=None):
    return os.path.join(sfm_data_dir or settings.SFM_DATA_DIR, "collection_set", collection_set_id)


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
