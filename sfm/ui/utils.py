class Diff:
    def __init__(self):
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
