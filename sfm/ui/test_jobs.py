from django.test import TestCase
from django.conf import settings
import json
from mock import MagicMock, patch
from .jobs import collection_harvest, collection_stop
from .models import Collection, CollectionSet, Seed, Credential, Group, User, Harvest
from .rabbit import RabbitWorker


class StartJobsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection_set = CollectionSet.objects.create(group=self.group, name="test_collection_set")
        self.credential_token = {"key": "test_key"}
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token=json.dumps(self.credential_token))
        self.harvest_options = {"test_option": "test_value"}

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_collection_harvest(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_USER_TIMELINE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)
        Seed.objects.create(collection=collection, token="test_token1", seed_id="1")
        Seed.objects.create(collection=collection, uid="test_uid2", seed_id="2")
        Seed.objects.create(collection=collection, token="test_token3", uid="test_uid3", seed_id="3")
        # Creating Inactive seed which will be ignored from harvest
        Seed.objects.create(collection=collection, uid="test_uid4", seed_id="4", is_active=False)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_harvest(collection.id)

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertTrue(message["collection_set"]["id"])
        self.assertTrue(message["collection"]["id"])
        self.assertEqual(
            "{}/collection_set/{}/{}".format(settings.SFM_COLLECTION_SET_DATA_DIR, self.collection_set.collection_set_id,
                                             collection.collection_id),
            message["path"])
        self.assertDictEqual(self.harvest_options, message["options"])
        self.assertDictEqual({"token": "test_token1", "id": "1"}, message["seeds"][0])
        self.assertDictEqual({"uid": "test_uid2", "id": "2"}, message["seeds"][1])
        self.assertDictEqual({"token": "test_token3", "uid": "test_uid3", "id": "3"}, message["seeds"][2])
        self.assertEqual(Collection.TWITTER_USER_TIMELINE, message["type"])
        self.assertTrue(message["id"])
        self.assertEqual("harvest.start.test_platform.twitter_user_timeline", args[1])

        # Harvest model object created
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertIsNotNone(harvest.date_requested)
        self.assertEqual(collection, harvest.collection)
        self.assertEqual(Harvest.REQUESTED, harvest.status)
        self.assertEqual(Collection.TWITTER_USER_TIMELINE, harvest.harvest_type)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_priority_collection_harvest(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_USER_TIMELINE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True,
                                               schedule_minutes=30)
        Seed.objects.create(collection=collection, token="test_token1", seed_id="1")

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_harvest(collection.id)

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        self.assertEqual("harvest.start.test_platform.twitter_user_timeline.priority", args[1])

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_missing_collection_harvest(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        collection_harvest(1234567)
        mock_rabbit_worker.assert_not_called()

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_collection_without_seeds_harvest(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_harvest(collection.id)

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertTrue(message["collection_set"]["id"])
        self.assertEqual(
            "{}/collection_set/{}/{}".format(settings.SFM_COLLECTION_SET_DATA_DIR, self.collection_set.collection_set_id,
                                             collection.collection_id),
            message["path"])
        self.assertDictEqual(self.harvest_options, message["options"])
        self.assertFalse("seeds" in message)
        self.assertEqual(Collection.TWITTER_SAMPLE, message["type"])
        self.assertTrue(message["id"])
        self.assertEqual("harvest.start.test_platform.twitter_sample", args[1])

        # Harvest model object created
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertIsNotNone(harvest.date_requested)
        self.assertEqual(collection, harvest.collection)
        self.assertEqual(Harvest.REQUESTED, harvest.status)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_skip_send(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)

        Harvest.objects.create(collection=collection,
                               historical_collection=collection.history.all()[0],
                               historical_credential=self.credential.history.all()[0])

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_harvest(collection.id)

        # Last harvest isn't done, so skip this harvest.
        # Harvest start message not sent
        mock_rabbit_worker.assert_not_called()

        # Harvest model object created
        harvest = collection.last_harvest(include_skipped=True)
        self.assertEqual(Harvest.SKIPPED, harvest.status)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_skip_send_after_void(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)

        Harvest.objects.create(collection=collection,
                               historical_collection=collection.history.all()[0],
                               historical_credential=self.credential.history.all()[0],
                               status=Harvest.VOIDED)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_harvest(collection.id)

        # Last harvest voided, so this one should be sent.
        # Harvest start message sent
        mock_rabbit_worker.assert_not_called()

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]

        # Harvest model object created
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertEqual(Harvest.REQUESTED, harvest.status)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_missing_seeds(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_USER_TIMELINE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        collection_harvest(collection.id)
        mock_rabbit_worker.assert_not_called()

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_wrong_number_of_seeds(self, mock_rabbit_worker_class):
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                               harvest_options=json.dumps(self.harvest_options), is_on=True)
        Seed.objects.create(collection=collection, token="test_token1")

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        collection_harvest(collection.id)
        mock_rabbit_worker.assert_not_called()


class StopJobsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection_set = CollectionSet.objects.create(group=self.group, name="test_collection_set")
        self.credential_token = {"key": "test_key"}
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token=json.dumps(self.credential_token))
        self.collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                                    harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                                    is_on=True)

        self.historical_collection = self.collection.history.all()[0]
        self.historical_credential = self.historical_collection.credential.history.all()[0]

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_stop_harvest(self, mock_rabbit_worker_class):
        harvest = Harvest.objects.create(harvest_type=Collection.TWITTER_SAMPLE,
                                         collection=self.collection,
                                         historical_collection=self.historical_collection,
                                         historical_credential=self.historical_credential)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        collection_stop(self.collection.id)

        # Harvest stop message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertEqual(message["id"], harvest.harvest_id)
        self.assertEqual("harvest.stop.test_platform.twitter_sample", args[1])

        # Harvest model object update
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertEqual(Harvest.STOP_REQUESTED, harvest.status)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_missing_collection(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        collection_stop(1234567)
        mock_rabbit_worker.assert_not_called()
