from django.test import TestCase
from django.conf import settings
import json
from mock import MagicMock, patch
from .jobs import seedset_harvest
from .models import SeedSet, Collection, Seed, Credential, Group, User, Harvest
from .rabbit import RabbitWorker


class JobsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=self.group, name="test_collection")
        self.credential_token = {"key": "test_key"}
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token=json.dumps(self.credential_token))
        self.harvest_options = {"test_option": "test_value"}

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_seedset_harvest(self, mock_rabbit_worker_class):
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type=SeedSet.TWITTER_USER_TIMELINE, name="test_seedset",
                                         harvest_options=json.dumps(self.harvest_options), is_active=True)
        Seed.objects.create(seed_set=seedset, token="test_token1", seed_id="1")
        Seed.objects.create(seed_set=seedset, uid="test_uid2", seed_id="2")
        Seed.objects.create(seed_set=seedset, token="test_token3", uid="test_uid3", seed_id="3")
        # Creating Inactive seed which will be ignored from harvest
        Seed.objects.create(seed_set=seedset, uid="test_uid4", seed_id="4", is_active=False)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        seedset_harvest(seedset.id)

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertTrue(message["collection"]["id"])
        self.assertEqual(
            "{}/collection/{}/{}".format(settings.SFM_DATA_DIR, self.collection.collection_id, self.seedset.seedset_id),
            message["path"])
        self.assertDictEqual(self.harvest_options, message["options"])
        self.assertDictEqual({"token": "test_token1", "id": "1"}, message["seeds"][0])
        self.assertDictEqual({"uid": "test_uid2", "id": "2"}, message["seeds"][1])
        self.assertDictEqual({"token": "test_token3", "uid": "test_uid3", "id": "3"}, message["seeds"][2])
        self.assertEqual(SeedSet.TWITTER_USER_TIMELINE, message["type"])
        self.assertTrue(message["id"])
        self.assertEqual("harvest.start.test_platform.twitter_user_timeline", args[1])

        # Harvest model object created
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertIsNotNone(harvest.date_requested)
        self.assertEqual(seedset, harvest.seed_set)
        self.assertEqual(Harvest.REQUESTED, harvest.status)
        self.assertEqual("test_type", harvest.harvest_type)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_missing_seedset_harvest(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        seedset_harvest(1234567)
        mock_rabbit_worker.assert_not_called()

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_seedset_without_seeds_harvest(self, mock_rabbit_worker_class):
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type=SeedSet.TWITTER_SAMPLE, name="test_seedset",
                                         harvest_options=json.dumps(self.harvest_options), is_active=True)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        seedset_harvest(seedset.id)

        # Harvest start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertTrue(message["collection"]["id"])
        self.assertEqual("/test-data/collection/{}".format(self.collection.collection_id),
                         message["collection"]["path"])
        self.assertDictEqual(self.harvest_options, message["options"])
        self.assertFalse("seeds" in message)
        self.assertEqual(SeedSet.TWITTER_SAMPLE, message["type"])
        self.assertTrue(message["id"])
        self.assertEqual("harvest.start.test_platform.twitter_sample", args[1])

        # Harvest model object created
        harvest = Harvest.objects.get(harvest_id=message["id"])
        self.assertIsNotNone(harvest.date_requested)
        self.assertEqual(seedset, harvest.seed_set)
        self.assertEqual(Harvest.REQUESTED, harvest.status)

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_missing_seeds(self, mock_rabbit_worker_class):
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type=SeedSet.TWITTER_USER_TIMELINE, name="test_seedset",
                                         harvest_options=json.dumps(self.harvest_options), is_active=True)

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        seedset_harvest(seedset.id)
        mock_rabbit_worker.assert_not_called()

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_wrong_number_of_seeds(self, mock_rabbit_worker_class):
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type=SeedSet.TWITTER_SAMPLE, name="test_seedset",
                                         harvest_options=json.dumps(self.harvest_options), is_active=True)
        Seed.objects.create(seed_set=seedset, token="test_token1")

        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        # Error should be logged and nothing happens
        seedset_harvest(seedset.id)
        mock_rabbit_worker.assert_not_called()
