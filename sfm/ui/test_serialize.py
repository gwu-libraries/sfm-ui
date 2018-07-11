from django.test import TestCase
from django.core.serializers.base import DeserializationError
from .models import Collection, CollectionSet, Seed, Credential, Group, User, Harvest, HarvestStat, Warc, default_uuid
from .utils import collection_path as get_collection_path
from .utils import collection_set_path as get_collection_set_path
from . import serialize
import tempfile
import os
import shutil
from datetime import date, datetime, timedelta
from time import sleep
from tzlocal import get_localzone


class SerializeTests(TestCase):
    def setUp(self):
        self.data_dir = tempfile.mkdtemp()
        group1 = Group.objects.create(name="test_group1")
        self.group2 = Group.objects.create(name="test_group2")
        self.collection_set = CollectionSet.objects.create(group=group1,
                                                           name="test_collection_set")
        self.collection_set_path = get_collection_set_path(self.collection_set, sfm_data_dir=self.data_dir)

        # Now change it to group2
        self.collection_set.group = self.group2
        # Now add a description
        self.collection_set.description = "This is a test collection."
        self.collection_set.save()

        self.user1 = User.objects.create_superuser(username="test_user1", email="test_user@test.com",
                                                   password="test_password")
        self.user2 = User.objects.create_superuser(username="test_user2", email="test_user@test.com",
                                                   password="test_password")
        credential1 = Credential.objects.create(user=self.user1, platform="test_platform1",
                                                token='{"key":"key1"}')
        self.credential2 = Credential.objects.create(user=self.user2, platform="test_platform2",
                                                     token='{"key":"key2"}')
        self.credential3 = Credential.objects.create(user=self.user1, platform="test_platform3",
                                                     token='{"key":"key3"}')

        # Now change credential2
        self.credential2.token = '{"key":"key2.1"}'
        self.credential2.save()
        self.collection1 = Collection.objects.create(collection_set=self.collection_set,
                                                     name="test_collection1",
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     credential=credential1,
                                                     is_on=True)
        # Now change to credential2
        self.collection1.credential = self.credential2
        self.collection1.save()
        self.collection1_path = get_collection_path(self.collection1, sfm_data_dir=self.data_dir)
        self.collection1_records_path = os.path.join(self.collection1_path, serialize.RECORD_DIR)

        # Seed
        self.seed1 = Seed.objects.create(collection=self.collection1, token='{"token":"token1}', is_active=True)
        # Now change seed1
        self.seed1.token = '{"token":"token1.1}'
        self.seed1.save()
        Seed.objects.create(collection=self.collection1, token='{"token":"token2}', is_active=False)

        # Harvest
        self.historical_collection = self.collection1.history.all()[0]
        self.historical_credential = self.historical_collection.credential.history.all()[0]
        self.harvest1 = Harvest.objects.create(collection=self.collection1,
                                               historical_collection=self.historical_collection,
                                               historical_credential=self.historical_credential)
        self.harvest2 = Harvest.objects.create(collection=self.collection1,
                                               parent_harvest=self.harvest1)
        # Harvest3 uses a credential that is not elsewhere
        self.harvest3 = Harvest.objects.create(collection=self.collection1,
                                               historical_collection=self.historical_collection,
                                               historical_credential=self.credential3.history.all()[0])

        # Harvest stats
        day1 = date(2016, 5, 20)
        day2 = date(2016, 5, 21)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=7, harvest_date=day2)

        # Warcs
        Warc.objects.create(harvest=self.harvest1, warc_id=default_uuid(), path="/data/warc1.warc.gz", sha1="warc1sha",
                            bytes=10, date_created=datetime.now(get_localzone()))
        Warc.objects.create(harvest=self.harvest1, warc_id=default_uuid(), path="/data/warc2.warc.gz", sha1="warc2sha",
                            bytes=11,
                            date_created=datetime.now(get_localzone()))

        # Another collection
        self.collection2 = Collection.objects.create(collection_set=self.collection_set,
                                                     name="test_collection2",
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     credential=credential1,
                                                     is_on=True)
        self.collection2_path = get_collection_path(self.collection2, sfm_data_dir=self.data_dir)

    def tearDown(self):
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)

    def test_serialize(self):
        self.assertTrue(self.collection1.is_on)

        serializer = serialize.RecordSerializer(data_dir=self.data_dir)
        serializer.serialize_collection_set(self.collection_set)

        # Records files exist
        self.assertTrue(os.path.exists(self.collection1_records_path))
        # collection set, historical collection set, groups
        # collection, historical collection, credentials, historical credentials
        # users, seed, historical seeds
        # harvests, harvest_stats, warcs, info
        self.assertEqual(14, len(os.listdir(self.collection1_records_path)))

        # Number of historical records for particular objects
        self.assertEqual(2, self.collection1.history.count())
        self.assertEqual(2, self.collection_set.history.count())
        self.assertEqual(2, self.credential2.history.count())
        self.assertEqual(2, self.seed1.history.count())

        # Deserialize while collection set already exists
        self.assertEqual(2, Group.objects.count())
        self.assertEqual(1, CollectionSet.objects.count())
        self.assertEqual(2, CollectionSet.history.count())
        self.assertEqual(2, Collection.objects.count())
        self.assertEqual(3, Collection.history.count())
        self.assertEqual(3, Credential.objects.count())
        self.assertEqual(4, Credential.history.count())
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Seed.objects.count())
        self.assertEqual(3, Seed.history.count())
        self.assertEqual(3, Harvest.objects.count())
        self.assertEqual(3, HarvestStat.objects.count())
        self.assertEqual(2, Warc.objects.count())

        deserializer = serialize.RecordDeserializer(data_dir=self.data_dir)
        deserializer.deserialize_collection_set(self.collection_set_path)
        # Nothing should change
        self.assertEqual(2, Group.objects.count())
        self.assertEqual(1, CollectionSet.objects.count())
        self.assertEqual(2, CollectionSet.history.count())
        self.assertEqual(2, Collection.objects.count())
        self.assertEqual(3, Collection.history.count())
        self.assertEqual(3, Credential.objects.count())
        self.assertEqual(4, Credential.history.count())
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Seed.objects.count())
        self.assertEqual(3, Seed.history.count())
        self.assertEqual(3, Harvest.objects.count())
        self.assertEqual(3, HarvestStat.objects.count())
        self.assertEqual(2, Warc.objects.count())

        # Partially clean the database in preparation for deserializing
        Warc.objects.all().delete()
        self.assertEqual(0, Warc.objects.count())

        HarvestStat.objects.all().delete()
        self.assertEqual(0, HarvestStat.objects.count())

        self.harvest1.delete()
        self.harvest2.delete()
        self.harvest3.delete()
        self.assertEqual(0, Harvest.objects.count())

        Seed.objects.all().delete()
        self.assertEqual(0, Seed.objects.count())

        Seed.history.all().delete()
        self.assertEqual(0, Seed.history.count())

        self.collection1.delete()
        self.collection2.delete()
        self.assertEqual(0, Collection.objects.count())
        Collection.history.all().delete()
        self.assertEqual(0, Collection.history.count())

        # Note that credential1 still exists.
        self.credential2.delete()
        self.credential3.delete()
        self.assertEqual(1, Credential.objects.count())
        # This is also deleting credential1's history
        Credential.history.all().delete()
        self.assertEqual(0, Credential.history.count())

        self.collection_set.delete()
        self.assertEqual(0, CollectionSet.objects.count())
        CollectionSet.history.all().delete()
        self.assertEqual(0, CollectionSet.history.count())

        self.group2.delete()
        # Note that group1 still exists.
        self.assertEqual(1, Group.objects.count())

        CollectionSet.history.all().delete()
        self.assertEqual(0, CollectionSet.history.count())

        # Note that user1 still exists
        self.user2.delete()
        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, Credential.objects.count())

        # Now deserialize again
        deserializer.deserialize_collection_set(self.collection_set_path)

        # And check the deserialization
        self.assertEqual(2, Group.objects.count())
        self.assertEqual(1, CollectionSet.objects.count())
        # +1 for added history note
        self.assertEqual(3, CollectionSet.history.count())
        self.assertEqual(CollectionSet.history.first().instance.history_note, "Collection set imported.")
        self.assertEqual(2, Collection.objects.count())
        # +2 for turning off collection after it is deserialized
        # +2 for added history note
        self.assertEqual(7, Collection.history.count())
        self.assertEqual(Collection.history.first().instance.history_note, "Collection imported.")
        self.assertEqual(3, Credential.objects.count())
        # This is one less since credential1's history was deleted.
        self.assertEqual(3, Credential.history.count())
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Seed.objects.count())
        self.assertEqual(3, Seed.history.count())
        self.assertEqual(3, Harvest.objects.count())
        self.assertEqual(3, HarvestStat.objects.count())
        self.assertEqual(2, Warc.objects.count())

        # Number of historical records for particular objects
        self.assertEqual(4, Collection.objects.get(collection_id=self.collection1.collection_id).history.count())
        # Make sure we got the right historical objects
        for h_collection in Collection.objects.get(collection_id=self.collection1.collection_id).history.all():
            self.assertEqual("test_collection1", h_collection.name)

        self.assertEqual(3, CollectionSet.objects.get(
            collection_set_id=self.collection_set.collection_set_id).history.count())
        self.assertEqual(2, Credential.objects.get(credential_id=self.credential2.credential_id).history.count())
        # Make sure we got the right historical objects
        for h_credential in Credential.objects.get(credential_id=self.credential2.credential_id).history.all():
            self.assertEqual("test_platform2", h_credential.platform)
        self.assertEqual(2, Seed.objects.get(seed_id=self.seed1.seed_id).history.count())

        # Collection turned off
        collection = Collection.objects.get_by_natural_key(self.collection1.collection_id)
        self.assertFalse(collection.is_on)

        # User2 is inactive
        self.assertFalse(User.objects.get(username="test_user2").is_active)

        # READMEs
        self.assertTrue(os.path.exists(os.path.join(self.collection_set_path, "README.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.collection1_path, "README.txt")))

        # Info file
        self.assertTrue(os.path.exists(os.path.join(self.collection1_records_path, "info.json")))

    def test_deserialize_wrong_collection_set(self):
        # This is testing that deserialization is not permitted when collection is placed
        # in incorrect collection set directory.
        serializer = serialize.RecordSerializer(data_dir=self.data_dir)
        serializer.serialize_collection_set(self.collection_set)

        # Partially clean the database in preparation for deserializing
        self.collection1.delete()
        self.collection_set.delete()

        self.assertTrue(os.path.exists(self.collection1_records_path))
        new_collection_set_path = "{}x".format(self.collection_set_path)
        shutil.move(self.collection_set_path, new_collection_set_path)
        self.assertFalse(os.path.exists(self.collection1_records_path))

        deserializer = serialize.RecordDeserializer(data_dir=self.data_dir)
        caught_error = False
        try:
            deserializer.deserialize_collection_set(new_collection_set_path)
        except DeserializationError:
            caught_error = True
        self.assertTrue(caught_error)

    def test_should_serialize(self):
        if not os.path.exists(self.collection1_records_path):
            os.makedirs(self.collection1_records_path)
        serializer = serialize.RecordSerializer(data_dir=self.data_dir)
        # serializer.serialize_collection_set(self.collection_set)
        # No existing info.json
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Existing serialization_date before last update
        serializer._write_info(datetime.utcnow() - timedelta(days=1), self.collection1_records_path)
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Existing serialization after last update
        serializer._write_info(datetime.utcnow() + timedelta(days=1), self.collection1_records_path)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Update collection
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        self.collection_set.description = "Changing the description"
        self.collection_set.save()
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Update collection set
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        self.collection1.description = "Changing the description"
        self.collection1.save()
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Update seed
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        self.seed1.token = '{"token":"token1.2}'
        self.seed1.save()
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Add seed
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        Seed.objects.create(collection=self.collection1, token='{"token":"token3}', is_active=False)
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Update harvest
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        self.harvest1.status = Harvest.SUCCESS
        self.harvest1.save()
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Add harvest
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        Harvest.objects.create(collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential)
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

        # Add warc
        serializer._write_info(datetime.utcnow(), self.collection1_records_path)
        sleep(.5)
        self.assertFalse(serializer._should_serialize(self.collection1, self.collection1_records_path))
        Warc.objects.create(harvest=self.harvest1, warc_id=default_uuid(), path="/data/warc3.warc.gz", sha1="warc3sha",
                            bytes=10, date_created=datetime.utcnow())
        self.assertTrue(serializer._should_serialize(self.collection1, self.collection1_records_path))

    def test_serialize_by_collection(self):
        serializer = serialize.RecordSerializer(data_dir=self.data_dir)
        serializer.serialize_collection_set(self.collection_set)

        deserializer = serialize.RecordDeserializer(data_dir=self.data_dir)

        deserializer.deserialize_collection(self.collection2_path)
        deserializer.deserialize_collection(self.collection1_path)

        # Nothing should change
        self.assertEqual(2, Group.objects.count())
        self.assertEqual(1, CollectionSet.objects.count())
        self.assertEqual(2, CollectionSet.history.count())
        self.assertEqual(2, Collection.objects.count())
        self.assertEqual(3, Collection.history.count())
        self.assertEqual(3, Credential.objects.count())
        self.assertEqual(4, Credential.history.count())
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Seed.objects.count())
        self.assertEqual(3, Seed.history.count())
        self.assertEqual(3, Harvest.objects.count())
        self.assertEqual(3, HarvestStat.objects.count())
        self.assertEqual(2, Warc.objects.count())

        # Partially clean the database in preparation for deserializing
        Warc.objects.all().delete()
        HarvestStat.objects.all().delete()
        self.harvest1.delete()
        self.harvest2.delete()
        self.harvest3.delete()
        Seed.objects.all().delete()
        Seed.history.all().delete()
        self.collection1.delete()
        self.collection2.delete()
        Collection.history.all().delete()
        # Note that credential1 still exists.
        self.credential2.delete()
        self.credential3.delete()
        # This is also deleting credential1's history
        Credential.history.all().delete()
        # self.group2.delete()
        # Note that group1 and group2 still exists.
        self.assertEqual(2, Group.objects.count())
        # Note that user1 still exists
        self.user2.delete()
        self.assertEqual(1, User.objects.count())
        self.assertEqual(1, Credential.objects.count())
        # Note that collection set still exists
        self.assertEqual(1, CollectionSet.objects.count())
        self.assertEqual(2, CollectionSet.history.count())

        # Now deserialize again
        deserializer.deserialize_collection(self.collection2_path)
        deserializer.deserialize_collection(self.collection1_path)

        # And check the deserialization
        self.assertEqual(2, Group.objects.count())
        self.assertEqual(1, CollectionSet.objects.count())
        self.assertEqual(2, CollectionSet.history.count())
        self.assertEqual(2, Collection.objects.count())
        # +2 for turning off collection after it is deserialized
        # +2 for added history note
        self.assertEqual(7, Collection.history.count())
        self.assertEqual(Collection.history.first().instance.history_note, "Collection imported.")
        self.assertEqual(3, Credential.objects.count())
        # This is one less since credential1's history was deleted.
        self.assertEqual(3, Credential.history.count())
        self.assertEqual(2, User.objects.count())
        self.assertEqual(2, Seed.objects.count())
        self.assertEqual(3, Seed.history.count())
        self.assertEqual(3, Harvest.objects.count())
        self.assertEqual(3, HarvestStat.objects.count())
        self.assertEqual(2, Warc.objects.count())

        # Number of historical records for particular objects
        self.assertEqual(4, Collection.objects.get(collection_id=self.collection1.collection_id).history.count())
        # Make sure we got the right historical objects
        for h_collection in Collection.objects.get(collection_id=self.collection1.collection_id).history.all():
            self.assertEqual("test_collection1", h_collection.name)

        self.assertEqual(2, CollectionSet.objects.get(
            collection_set_id=self.collection_set.collection_set_id).history.count())
        self.assertEqual(2, Credential.objects.get(credential_id=self.credential2.credential_id).history.count())
        # Make sure we got the right historical objects
        for h_credential in Credential.objects.get(credential_id=self.credential2.credential_id).history.all():
            self.assertEqual("test_platform2", h_credential.platform)
        self.assertEqual(2, Seed.objects.get(seed_id=self.seed1.seed_id).history.count())
