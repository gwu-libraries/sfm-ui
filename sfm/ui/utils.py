from django.core.exceptions import ObjectDoesNotExist


class Diff:
    def __init__(self):
        self.user = None
        self.date = None
        self.note = None
        self.fields = {}


def diff_historical_object(historical_object):
    """
    Performs a diff on historical object to determine which fields have changed.

    The historical_object must have a HistoricalRecord attribute named history, a
    TextField named history_note, and
    a Meta field named diff_fields containing a list of field names to diff.
    :param historical_object: the historical object (i.e., obtained from object.history)
    :return: a Diff
    """
    try:
        original_object = historical_object.get_previous_by_history_date()
    except ObjectDoesNotExist:
        original_object = None

    diff = Diff()
    diff.date = historical_object.history_date
    diff.user = historical_object.history_user
    diff.note = historical_object.history_note
    for field in historical_object.history_object._meta.diff_fields:
        value = getattr(historical_object, field)
        if value == "":
            value = None
        original_value = getattr(original_object, field) if original_object else None
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
    for historical_object in obj.history.all():
        diffs.append(diff_historical_object(historical_object))
    return diffs
