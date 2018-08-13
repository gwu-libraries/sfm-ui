import os
import shutil
import codecs
import logging
import json
import iso8601
import itertools

from django.core import serializers
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.db.models import Max
from django.core.serializers.base import DeserializationError
from django.db import transaction

from .utils import collection_path as get_collection_path
from .utils import collection_set_path as get_collection_set_path
from .utils import collection_path_by_id as get_collection_path_by_id
from .models import Group, CollectionSet, Collection, User, Credential, Seed, Harvest, Warc
from sfmutils.utils import datetime_now

log = logging.getLogger(__name__)

RECORD_DIR = "records"
GROUP_FILENAME = "groups.json"
COLLECTION_SET_FILENAME = "collection_set.json"
HISTORICAL_COLLECTION_SET_FILENAME = "historical_collection_set.json"
CREDENTIAL_FILENAME = "credentials.json"
HISTORICAL_CREDENTIAL_FILENAME = "historical_credentials.json"
COLLECTION_FILENAME = "collection.json"
HISTORICAL_COLLECTION_FILENAME = "historical_collection.json"
USER_FILENAME = "users.json"
SEED_FILENAME = "seeds.json"
HISTORICAL_SEED_FILENAME = "historical_seeds.json"
HARVEST_FILENAME = "harvests.json"
HARVEST_STATS_FILENAME = "harvest_stats.json"
WARC_FILENAME = "warcs.json"
INFO_FILENAME = "info.json"


class RecordSerializer:
    def __init__(self, data_dir=None):
        log.debug("Data dir is %s", data_dir)
        self.data_dir = data_dir

    def serialize_all(self, force_serialize=False):
        log.info("Serializing all")
        for collection_set in CollectionSet.objects.all():
            self.serialize_collection_set(collection_set, force_serialize=force_serialize)

    def serialize_collection_set(self, collection_set, force_serialize=False):
        log.info("Serializing %s", collection_set)
        for collection in collection_set.collections.all():
            self.serialize_collection(collection, force_serialize=force_serialize)

        # README
        self._write_readme("collection_set", collection_set,
                           get_collection_set_path(collection_set, sfm_data_dir=self.data_dir))

    def serialize_collection(self, collection, force_serialize=False):
        records_path = os.path.join(get_collection_path(collection, sfm_data_dir=self.data_dir), RECORD_DIR)
        log.debug("Collection records path is %s", records_path)

        # Determine whether to serialize
        if not force_serialize and not self._should_serialize(collection, records_path):
            log.info("Skipping serialization of %s since no update since last serialization.", collection)
            return

        log.info("Serializing %s", collection)
        serialization_date = datetime_now()

        # Initialize records dir
        self._initialize_records_dir(records_path)

        # Serialize collection set, historical collection sets
        self._serialize_collection_set(collection.collection_set, records_path)

        # Serialize credentials, users, groups
        self._serialize_credentials(collection, records_path)

        # Collection
        collection_record_filepath = os.path.join(records_path, COLLECTION_FILENAME)
        self._serialize_objs((collection,), collection_record_filepath)
        log.debug("Serialized collection to %s", collection_record_filepath)

        # Historical collection
        historical_collection_record_filepath = os.path.join(records_path, HISTORICAL_COLLECTION_FILENAME)
        self._serialize_objs(collection.history.all(), historical_collection_record_filepath)
        log.debug("Serialized historical collection to %s", historical_collection_record_filepath)

        # Seeds
        self._serialize_seeds(collection, records_path)

        # Harvests, harvest stats, and warcs
        self._serialize_harvests(collection, records_path)

        # Info file
        self._write_info(serialization_date, records_path)

        # README
        self._write_readme("collection", collection, get_collection_path(collection, sfm_data_dir=self.data_dir))

    def _should_serialize(self, collection, records_path):
        # Determine whether to serialize
        last_serialization_date = self._read_last_serialization(records_path)
        log.debug("Last serialization date is %s", last_serialization_date)
        most_recent_update = self._find_most_recent_update(collection)
        log.debug("Most recent update is %s", most_recent_update)

        if last_serialization_date is not None and last_serialization_date > most_recent_update:
            return False
        return True

    def _serialize_collection_set(self, collection_set, records_path):
        # Collection set
        collection_set_record_filepath = os.path.join(records_path, COLLECTION_SET_FILENAME)
        self._serialize_objs((collection_set,), collection_set_record_filepath)
        log.debug("Serialized collection set to %s", collection_set_record_filepath)

        # Historical collection set
        historical_collection_set_record_filepath = os.path.join(records_path, HISTORICAL_COLLECTION_SET_FILENAME)
        self._serialize_objs(collection_set.history.all(), historical_collection_set_record_filepath)
        log.debug("Serialized historical collection sets to %s", historical_collection_set_record_filepath)

    def _serialize_groups(self, users, collection_set, records_path):
        # Groups (current group and all groups in historical collection sets)
        groups = {collection_set.group, }
        # From historical collection sets
        for historical_collection_set in collection_set.history.all():
            groups.add(historical_collection_set.group)

        # From users
        for user in users:
            groups |= set(user.groups.all())
        group_record_filepath = os.path.join(records_path, GROUP_FILENAME)
        self._serialize_objs(groups, group_record_filepath)
        log.debug("Serialized groups to %s", group_record_filepath)

    def _serialize_credentials(self, collection, records_path):
        # Credentials (current credential and all credentials in historical collections
        credentials = {collection.credential}
        for historical_collection in collection.history.all():
            credentials.add(historical_collection.credential)
        # Also credentials in harvests
        for harvest in collection.harvests.all():
            if harvest.historical_credential:
                credentials.add(harvest.historical_credential.instance)

        credentials_record_filepath = os.path.join(records_path, CREDENTIAL_FILENAME)
        self._serialize_objs(credentials, credentials_record_filepath)
        log.debug("Serialized credentials to %s", credentials_record_filepath)

        # Historical credentials
        historical_credentials_record_filepath = os.path.join(records_path, HISTORICAL_CREDENTIAL_FILENAME)
        self._serialize_objs(self._historical_credentials_iter(credentials), historical_credentials_record_filepath)
        log.debug("Serialized historical credentials to %s", historical_credentials_record_filepath)

        # Users
        self._serialize_users(collection, credentials, records_path)

    @staticmethod
    def _historical_credentials_iter(credentials):
        for credential in credentials:
            for historical_credential in credential.history.all():
                yield historical_credential

    def _serialize_users(self, collection, credentials, records_path):
        users = set()
        # From credentials
        for credential in credentials:
            users.add(credential.user)

        # From historical credentials
        for historical_credential in collection.credential.history.all():
            if historical_credential.history_user:
                users.add(historical_credential.history_user)

        # From historical collections
        for historical_collection in collection.history.all():
            if historical_collection.history_user:
                users.add(historical_collection.history_user)

        # From historical collection sets
        for historical_collection_set in collection.collection_set.history.all():
            if historical_collection_set.history_user:
                users.add(historical_collection_set.history_user)

        # From historical seeds
        for seed in collection.seeds.all():
            for historical_seed in seed.history.all():
                if historical_seed.history_user:
                    users.add(historical_seed.history_user)

        user_record_filepath = os.path.join(records_path, USER_FILENAME)
        self._serialize_objs(users, user_record_filepath)
        log.debug("Serialized users to %s", user_record_filepath)

        # Groups
        self._serialize_groups(users, collection.collection_set, records_path)

    def _serialize_seeds(self, collection, records_path):
        # Seeds
        seeds_record_filepath = os.path.join(records_path, SEED_FILENAME)
        self._serialize_objs(collection.seeds.all(), seeds_record_filepath)
        log.debug("Serialized seeds to %s", seeds_record_filepath)

        # Historical seeds
        historical_seeds_record_filepath = os.path.join(records_path, HISTORICAL_SEED_FILENAME)
        self._serialize_objs(self._historical_seeds_iter(collection), historical_seeds_record_filepath)
        log.debug("Serialized historical seeds to %s", historical_seeds_record_filepath)

    @staticmethod
    def _historical_seeds_iter(collection):
        for seed in collection.seeds.all():
            for historical_seed in seed.history.all():
                # For undetermined reasons, sometimes get historical seeds that are not part of collection.
                if historical_seed.instance.collection == collection:
                    yield historical_seed

    def _serialize_harvests(self, collection, records_path):
        # Harvests
        harvests_record_filepath = os.path.join(records_path, HARVEST_FILENAME)
        # Need to make sure that harvests without parents come first
        self._serialize_objs(itertools.chain(collection.harvests.filter(parent_harvest__isnull=True),
                                             collection.harvests.filter(parent_harvest__isnull=False)),
                             harvests_record_filepath)
        log.debug("Serialized harvests to %s", harvests_record_filepath)

        # Harvest stats
        harvest_stats_record_filepath = os.path.join(records_path, HARVEST_STATS_FILENAME)
        self._serialize_objs(self._harvest_stats_iter(collection), harvest_stats_record_filepath)
        log.debug("Serialized harvest stats to %s", harvest_stats_record_filepath)

        # WARCs
        warc_record_filepath = os.path.join(records_path, WARC_FILENAME)
        self._serialize_objs(self._warcs_iter(collection), warc_record_filepath)
        log.debug("Serialized warcs to %s", warc_record_filepath)

    @staticmethod
    def _harvest_stats_iter(collection):
        for harvest in collection.harvests.all():
            for harvest_stats in harvest.harvest_stats.all():
                yield harvest_stats

    @staticmethod
    def _warcs_iter(collection):
        for harvest in collection.harvests.all():
            for warc in harvest.warcs.all():
                yield warc

    @staticmethod
    def _initialize_records_dir(records_path):
        if os.path.exists(records_path):
            shutil.rmtree(records_path)
        os.makedirs(records_path)

    @staticmethod
    def _serialize_objs(objs, filepath):
        with codecs.open(filepath, "w", encoding="utf-8") as f:
            serializers.serialize("json", objs, indent=4, use_natural_foreign_keys=True,
                                  use_natural_primary_keys=True, stream=f)
        assert os.path.exists(filepath)

    @staticmethod
    def _write_readme(model_name, obj, path):
        readme_template = get_template('readme/{}.txt'.format(model_name))
        readme_txt = readme_template.render({model_name: obj, "now": datetime_now()})
        readme_filepath = os.path.join(path, "README.txt")
        log.debug("Writing %s README to %s: %s", model_name, readme_filepath, readme_txt)
        with codecs.open(readme_filepath, "w", encoding="utf-8") as f:
            f.write(readme_txt)

    @staticmethod
    def _write_info(serialization_date, records_path):
        info_txt = json.dumps({
            "sfm_ui_version": settings.SFM_UI_VERSION,
            "serialization_date": serialization_date.isoformat()
        }, indent=4)
        info_filepath = os.path.join(records_path, INFO_FILENAME)
        log.debug("Writing info to %s: %s", info_filepath, info_txt)
        with codecs.open(info_filepath, "w", encoding="utf-8") as f:
            f.write(info_txt)

    @staticmethod
    def _read_last_serialization(records_path):
        info_filepath = os.path.join(records_path, INFO_FILENAME)
        if os.path.exists(info_filepath):
            with codecs.open(info_filepath, "r", encoding="utf-8") as f:
                info = json.load(f)
            return iso8601.parse_date(info["serialization_date"])
        return None

    @staticmethod
    def _find_most_recent_update(collection):
        # Default date is in case queries return None
        default_date = collection.date_updated
        return max([
            # Collection
            collection.date_updated,
            # Collection set
            collection.collection_set.date_updated,
            # Seeds
            Seed.objects.filter(collection=collection).aggregate(recent_update=Max('date_updated'))[
                "recent_update"] or default_date,
            # Harvests
            Harvest.objects.filter(collection=collection).aggregate(recent_update=Max('date_updated'))[
                "recent_update"] or default_date,
            # Warcs
            Warc.objects.filter(harvest__collection=collection).aggregate(recent_update=Max('date_updated'))[
                "recent_update"] or default_date
        ])


class RecordDeserializer:
    def __init__(self, data_dir=None):
        log.debug("Data dir is %s", data_dir)
        self.data_dir = data_dir

    @staticmethod
    def _check_exists(filepath):
        if not os.path.exists(filepath):
            raise IOError("{} not found".format(filepath))

    def deserialize_collection_set(self, collection_set_path):
        log.info("Deserializing collection set at %s", collection_set_path)
        self._check_exists(collection_set_path)
        for pathname in os.listdir(collection_set_path):
            collection_path = os.path.join(collection_set_path, pathname)
            if os.path.isdir(collection_path):
                records_path = os.path.join(collection_path, RECORD_DIR)
                if os.path.exists(records_path):
                    self.deserialize_collection(collection_path)
                else:
                    log.debug("%s is not a collection", collection_path)

    def deserialize_collection(self, collection_path):
        log.info("Deserializing collection at %s", collection_path)

        # Determine paths and make sure they exist before deserializing
        records_path = os.path.join(collection_path, RECORD_DIR)
        self._check_exists(records_path)

        group_record_filepath = os.path.join(records_path, GROUP_FILENAME)
        self._check_exists(group_record_filepath)

        collection_set_record_filepath = os.path.join(records_path, COLLECTION_SET_FILENAME)
        self._check_exists(collection_set_record_filepath)

        historical_collection_set_record_filepath = os.path.join(records_path, HISTORICAL_COLLECTION_SET_FILENAME)
        self._check_exists(historical_collection_set_record_filepath)

        collection_record_filepath = os.path.join(records_path, COLLECTION_FILENAME)
        self._check_exists(collection_record_filepath)

        historical_collection_record_filepath = os.path.join(records_path, HISTORICAL_COLLECTION_FILENAME)
        self._check_exists(historical_collection_record_filepath)

        user_record_filepath = os.path.join(records_path, USER_FILENAME)
        self._check_exists(user_record_filepath)

        credential_record_filepath = os.path.join(records_path, CREDENTIAL_FILENAME)
        self._check_exists(credential_record_filepath)

        historical_credential_record_filepath = os.path.join(records_path, HISTORICAL_CREDENTIAL_FILENAME)
        self._check_exists(historical_credential_record_filepath)

        seed_filepath = os.path.join(records_path, SEED_FILENAME)
        self._check_exists(seed_filepath)

        historical_seed_filepath = os.path.join(records_path, HISTORICAL_SEED_FILENAME)
        self._check_exists(historical_seed_filepath)

        harvest_filepath = os.path.join(records_path, HARVEST_FILENAME)
        self._check_exists(harvest_filepath)

        harvest_stats_filepath = os.path.join(records_path, HARVEST_STATS_FILENAME)
        self._check_exists(harvest_stats_filepath)

        warcs_filepath = os.path.join(records_path, WARC_FILENAME)
        self._check_exists(warcs_filepath)

        # Only proceed with deserialization if collection doesn't already exist
        collection_id = self._load_record(collection_record_filepath)[0]["fields"]["collection_id"]
        if not Collection.objects.filter(collection_id=collection_id).exists():
            log.debug("Collection does not exist, so proceeding with deserialization")

            collection_set_id = self._load_record(collection_set_record_filepath)[0]["fields"]["collection_set_id"]
            # Only proceed with deserialization of collection set if it doesn't already exist

            # Make sure that in collection path is correct
            expected_collection_path = get_collection_path_by_id(collection_set_id=collection_set_id,
                                                                 collection_id=collection_id,
                                                                 sfm_data_dir=self.data_dir)
            if not os.path.exists(expected_collection_path) or not os.path.samefile(expected_collection_path,
                                                                                    collection_path):
                raise DeserializationError(
                    "Collection path is {}, but should be {}".format(collection_path, expected_collection_path))

            # Groups first
            self._deserialize_groups(group_record_filepath)

            # Users
            self._deserialize_users(user_record_filepath)

            if not CollectionSet.objects.filter(collection_set_id=collection_set_id).exists():
                log.debug("Collection set does not exist, so proceeding with deserialization")

                # Collection set
                self._deserialize(collection_set_record_filepath)

                # Historical collection set
                self._deserialize_historical_objects(historical_collection_set_record_filepath,
                                                     collection_set_record_filepath,
                                                     "collection_set_id", CollectionSet)

                # Add a history note
                collection_set = CollectionSet.objects.get(collection_set_id=collection_set_id)
                collection_set.history_note = "Collection set imported."
                collection_set.save(force_history=True)

            else:
                log.warning("Collection set already exists, so not deserializing")

            # Credentials and credential history
            self._deserialize_credentials(credential_record_filepath, historical_credential_record_filepath)

            # Collection
            self._deserialize(collection_record_filepath)

            # Collection history
            self._deserialize_historical_objects(historical_collection_record_filepath, collection_record_filepath,
                                                 "collection_id", Collection)

            # Seeds
            self._deserialize(seed_filepath)

            # Historical seeds
            self._deserialize_historical_objects(historical_seed_filepath, seed_filepath,
                                                 "seed_id", Seed)

            # Harvests
            self._deserialize_harvests(harvest_filepath)

            # Harvest stats
            self._deserialize(harvest_stats_filepath)

            # Warcs
            self._deserialize(warcs_filepath)

            # Turn off collection
            collection = Collection.objects.get_by_natural_key(collection_id)
            if collection.is_on:
                log.debug("Turning off collection")
                collection.is_on = False
                collection.history_note = "Turned off as part of import of this collection."
                collection.save()
            # Add history note for import
            collection.history_note = "Collection imported."
            collection.save(force_history=True)

        else:
            log.warning("Collection already exists, so not deserializing")

    @transaction.atomic
    def _deserialize_groups(self, group_record_filepath):
        log.debug("Deserializing groups")
        for d_group in self._deserialize_iter(group_record_filepath):
            if not Group.objects.filter(name=d_group.object.name).exists():
                log.debug("Saving group %s", d_group.object.name)
                d_group.save()
            else:
                log.debug("Group %s already exists", d_group.object.name)

    @transaction.atomic
    def _deserialize_users(self, user_record_filepath):
        log.debug("Deserializing users")
        for d_user in self._deserialize_iter(user_record_filepath):
            if not User.objects.filter(username=d_user.object.username).exists():
                log.debug("Saving user %s", d_user.object.username)
                # Make them inactive
                d_user.object.is_active = False
                d_user.save()
            else:
                log.debug("User %s already exists", d_user.object.username)

    @transaction.atomic
    def _deserialize_credentials(self, credentials_record_filepath, historical_credentials_record_filepath):
        log.debug("Deserializing credentials")
        credential_ids = []
        for d_credential in self._deserialize_iter(credentials_record_filepath):
            if not Credential.objects.filter(credential_id=d_credential.object.credential_id).exists():
                log.debug("Saving credential %s", d_credential.object.credential_id)
                d_credential.save()
                credential_ids.append(d_credential.object.credential_id)
            else:
                log.debug("Credential %s already exists", d_credential.object.credential_id)

        self._deserialize_historical_objects(historical_credentials_record_filepath, credentials_record_filepath,
                                             "credential_id", Credential, credential_ids)

    @transaction.atomic
    def _deserialize_harvests(self, filepath):
        for d_harvest in self._deserialize_iter(filepath):
            # Due to historical reasons, these JSON fields are a mess.
            if isinstance(d_harvest.object.infos, str):
                d_harvest.object.infos = json.loads(d_harvest.object.infos)
                d_harvest.object.warnings = json.loads(d_harvest.object.warnings)
                d_harvest.object.errors = json.loads(d_harvest.object.errors)
            d_harvest.save()

    @transaction.atomic
    def _deserialize_historical_objects(self, historical_record_filepath, record_filepath, record_id_field, Model,
                                        limit_ids=None):
        # Historical objects need to be handled differently because they must have their id set correctly.
        records_ids_to_keys = {}
        records = self._load_record(record_filepath)
        for record in records:
            record_id = record["fields"][record_id_field]
            records_ids_to_keys[record_id] = Model.objects.get(**{record_id_field: record_id}).id
        for d_obj in self._deserialize_iter(historical_record_filepath):
            d_obj.object.id = records_ids_to_keys[getattr(d_obj.object, record_id_field)]
            if limit_ids is None or getattr(d_obj.object.instance, record_id_field) in limit_ids:
                d_obj.save()

    @staticmethod
    def _load_record(record_filepath):
        with codecs.open(record_filepath, "r", encoding="utf-8") as f:
            record = json.load(f)
        return record

    def _deserialize_item(self, record_filepath):
        return self._deserialize_iter(record_filepath).__next__()

    @transaction.atomic
    def _deserialize(self, filepath):
        for d_obj in self._deserialize_iter(filepath):
            d_obj.save()

    @staticmethod
    def _deserialize_iter(filepath):
        log.debug("Deserializing %s", filepath)
        with codecs.open(filepath, "r", encoding="utf-8") as f:
            for d_obj in serializers.deserialize("json", f):
                yield d_obj


def serialize_all():
    serializer = RecordSerializer()
    serializer.serialize_all()
