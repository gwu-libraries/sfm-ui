from django.test import TestCase
from mock import MagicMock, patch
from .export import request_export
from .models import SeedSet, Collection, Seed, Credential, Group, User, Export
from .rabbit import RabbitWorker
import datetime
from tzlocal import get_localzone
import iso8601


class ExportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        group = Group.objects.create(name="test_group")
        collection = Collection.objects.create(group=group, name="test_collection")
        credential = Credential.objects.create(user=self.user, platform="test_platform",
                                               token="{}")
        self.seedset = SeedSet.objects.create(collection=collection, credential=credential,
                                              harvest_type="test_type", name="test_seedset",
                                              harvest_options="{}")
        self.seed1 = Seed.objects.create(seed_set=self.seedset, uid="test_uid")
        self.seed2 = Seed.objects.create(seed_set=self.seedset, uid="test_uid2")

    @patch("ui.export.RabbitWorker", autospec=True)
    def test_seedset_export(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        export = Export.objects.create(user=self.user,
                                       export_type="test_type",
                                       export_format="json",
                                       dedupe=True,
                                       item_date_start=datetime.datetime.now(get_localzone()),
                                       item_date_end=datetime.datetime.now(get_localzone()),
                                       harvest_date_start=datetime.datetime.now(get_localzone()),
                                       harvest_date_end=datetime.datetime.now(get_localzone()))
        export.seed_set = self.seedset
        export.save()

        request_export(export)

        # Export start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertEqual(message["id"], export.export_id)
        self.assertEqual(message["path"], export.path)
        self.assertEqual(message["type"], export.export_type)
        self.assertEqual(message["format"], export.export_format)
        self.assertTrue(message["dedupe"])
        self.assertEqual(iso8601.parse_date(message["item_date_start"]), export.item_date_start)
        self.assertEqual(iso8601.parse_date(message["item_date_end"]), export.item_date_end)
        self.assertEqual(iso8601.parse_date(message["harvest_date_start"]), export.harvest_date_start)
        self.assertEqual(iso8601.parse_date(message["harvest_date_end"]), export.harvest_date_end)
        self.assertEqual(message["seedset"]["id"], export.seed_set.seedset_id)
        self.assertEqual("export.start.test_platform.test_type", args[1])

    @patch("ui.export.RabbitWorker", autospec=True)
    def test_seed_export(self, mock_rabbit_worker_class):
        mock_rabbit_worker = MagicMock(spec=RabbitWorker)
        mock_rabbit_worker_class.side_effect = [mock_rabbit_worker]

        export = Export.objects.create(user=self.user,
                                       export_type="test_type")
        export.seeds.add(self.seed1)
        export.seeds.add(self.seed2)
        export.save()

        request_export(export)

        # Export start message sent
        name, args, kwargs = mock_rabbit_worker.mock_calls[0]
        self.assertEqual("send_message", name)
        message = args[0]
        self.assertEqual(message["id"], export.export_id)
        self.assertEqual(message["path"], export.path)
        self.assertEqual(message["type"], export.export_type)
        self.assertEqual(message["format"], export.export_format)
        self.assertFalse(message["dedupe"])
        self.assertTrue("item_date_start" not in message)
        self.assertTrue("item_date_end" not in message)
        self.assertTrue("harvest_date_start" not in message)
        self.assertTrue("harvest_date_end" not in message)
        self.assertListEqual(message["seeds"], [{"id": self.seed1.seed_id, "uid": self.seed1.uid},
                                                {"id": self.seed2.seed_id, "uid": self.seed2.uid}])
        self.assertEqual("export.start.test_platform.test_type", args[1])