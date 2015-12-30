from django.test import TestCase
import json
from mock import MagicMock, patch
from .jobs import seedset_harvest
from .models import SeedSet, Collection, Seed, Credential, Group, User
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
        self.seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                              harvest_type="test_type", name="test_seedset",
                                              harvest_options=json.dumps(self.harvest_options))
        Seed.objects.create(seed_set=self.seedset, token="test_token1")
        Seed.objects.create(seed_set=self.seedset, uid="test_uid2")
        Seed.objects.create(seed_set=self.seedset, token="test_token3", uid="test_uid3")

    @patch("ui.jobs.RabbitWorker", autospec=True)
    def test_seedset_harvest(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        seedset_harvest(self.seedset.id)

        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertEqual("collection:{}".format(self.collection.id), message["collection"]["id"])
        self.assertEqual("/tmp/collection/{}".format(self.collection.id), message["collection"]["path"])
        self.assertDictEqual(self.harvest_options, message["options"])
        self.assertDictEqual({"token": "test_token1"}, message["seeds"][0])
        self.assertDictEqual({"uid": "test_uid2"}, message["seeds"][1])
        self.assertDictEqual({"token": "test_token3", "uid": "test_uid3"}, message["seeds"][2])
        self.assertEqual("test_type", message["type"])
        self.assertTrue(message["id"].startswith("harvest:{}:".format(self.seedset.id)))
        self.assertEqual("harvest.start.test_platform.test_type", args[1])

    def test_missing_seedset_harvest(self):
        # Error should be logged and nothing happens
        seedset_harvest(1234567)
