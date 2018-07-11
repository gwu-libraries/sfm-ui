from django.test import TestCase
from ui.models import Harvest, Collection, Group, CollectionSet, Credential, User, Seed, Warc, Export, HarvestStat
import json
from .sfm_ui_consumer import SfmUiConsumer
import iso8601
from mock import patch

from datetime import date


class ConsumerTest(TestCase):
    def setUp(self):
        # Create harvest model object
        group = Group.objects.create(name="test_group")
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        user.groups.add(group)
        collection_set = CollectionSet.objects.create(group=group, name="test_collection_set")
        credential = Credential.objects.create(user=user, platform="test_platform",
                                               token=json.dumps({}))
        collection = Collection.objects.create(collection_set=collection_set, credential=credential,
                                               harvest_type="test_type", name="test_collection",
                                               harvest_options=json.dumps({}))
        stream_collection = Collection.objects.create(collection_set=collection_set, credential=credential,
                                                      harvest_type=Collection.TWITTER_SAMPLE,
                                                      name="test_stream_collection",
                                                      harvest_options=json.dumps({}), is_on=True)

        self.assertTrue(stream_collection.is_on)
        Seed.objects.create(collection=collection, uid="131866249@N02", seed_id='1')
        Seed.objects.create(collection=collection, token="library_of_congress", seed_id='2')

        historical_collection = collection.history.all()[0]
        historical_credential = historical_collection.credential.history.all()[0]
        self.harvest = Harvest.objects.create(harvest_id="test:1",
                                              collection=collection,
                                              historical_collection=historical_collection,
                                              historical_credential=historical_credential)
        # Creating a second harvest to make sure that harvest stats don't conflict
        harvest2 = Harvest.objects.create(harvest_id="test:2",
                                          collection=collection,
                                          historical_collection=historical_collection,
                                          historical_credential=historical_credential)
        historical_stream_collection = stream_collection.history.all()[0]
        historical_stream_credential = historical_stream_collection.credential.history.all()[0]
        self.stream_harvest = Harvest.objects.create(harvest_id="test:3",
                                                     collection=stream_collection,
                                                     historical_collection=historical_stream_collection,
                                                     historical_credential=historical_stream_credential)
        HarvestStat.objects.create(harvest=harvest2, item="photos", count=3, harvest_date=date(2016, 5, 20))
        Export.objects.create(export_id="test:2", user=user, export_type="test_type")
        self.consumer = SfmUiConsumer()

    def test_harvest_status_on_message(self):
        self.consumer.routing_key = "harvest.status.test.test_search"
        self.consumer.message = {
            "id": "test:1",
            "status": Harvest.RUNNING,
            "date_started": "2015-07-28T11:17:36.640044",
            "infos": [{"code": "test_code_1", "message": "congratulations"}],
            "warnings": [{"code": "test_code_2", "message": "be careful"}],
            "errors": [{"code": "test_code_3", "message": "oops"}],
            "stats": {
                "2016-05-20": {
                    "photos": 12,
                },
                "2016-05-21": {
                    "photos": 19,
                },
            },
            "token_updates": {
                "1": "j.littman"
            },
            "uids": {
                "2": "671366249@N03"
            },
            "warcs": {
                "count": 3,
                "bytes": 345234242
            },
            "service": "Twitter Harvester",
            "host": "f0c3c5ef7031",
            "instance": "39",
        }
        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        harvest = Harvest.objects.get(harvest_id="test:1")
        self.assertEqual(Harvest.RUNNING, harvest.status)
        self.assertEqual(12, harvest.harvest_stats.get(item="photos", harvest_date=date(2016, 5, 20)).count)
        self.assertDictEqual({
            "1": "j.littman"
        }, harvest.token_updates)
        self.assertDictEqual({
            "2": "671366249@N03"
        }, harvest.uids)
        self.assertEqual(3, harvest.warcs_count)
        self.assertEqual(345234242, harvest.warcs_bytes)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:36.640044"), harvest.date_started)
        self.assertListEqual([{"code": "test_code_1", "message": "congratulations"}], harvest.infos)
        self.assertListEqual([{"code": "test_code_2", "message": "be careful"}], harvest.warnings)
        self.assertListEqual([{"code": "test_code_3", "message": "oops"}], harvest.errors)
        self.assertEqual("Twitter Harvester", harvest.service)
        self.assertEqual("f0c3c5ef7031", harvest.host)
        self.assertEqual("39", harvest.instance)

        # Check updated seeds
        seed1 = Seed.objects.get(seed_id="1")
        self.assertEqual("j.littman", seed1.token)
        self.assertTrue(seed1.history_note.startswith("Changed token"))
        seed2 = Seed.objects.get(seed_id="2")
        self.assertEqual("671366249@N03", seed2.uid)
        self.assertTrue(seed2.history_note.startswith("Changed uid"))

        # Now update
        self.consumer.message = {
            "id": "test:1",
            "status": Harvest.SUCCESS,
            "date_started": "2015-07-28T11:17:36.640044",
            "date_ended": "2015-07-28T11:17:42.539470",
            "infos": [{"code": "test_code_1", "message": "congratulations"}],
            "warnings": [{"code": "test_code_2", "message": "be careful"}],
            "errors": [{"code": "test_code_3", "message": "oops"}],
            "stats": {
                "2016-05-20": {
                    "photos": 12,
                },
                "2016-05-21": {
                    "photos": 24,
                    "users": 1
                },
            },
            "warcs": {
                "count": 5,
                "bytes": 645234242
            },
            "service": "Twitter Harvester",
            "host": "f0c3c5ef7031",
            "instance": "39",
        }
        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        harvest = Harvest.objects.get(harvest_id="test:1")
        self.assertEqual(Harvest.SUCCESS, harvest.status)
        self.assertEqual(24, harvest.harvest_stats.get(item="photos", harvest_date=date(2016, 5, 21)).count)
        self.assertEqual(1, harvest.harvest_stats.get(item="users", harvest_date=date(2016, 5, 21)).count)
        self.assertEqual(5, harvest.warcs_count)
        self.assertEqual(645234242, harvest.warcs_bytes)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:36.640044"), harvest.date_started)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:42.539470"), harvest.date_ended)
        self.assertListEqual([{"code": "test_code_1", "message": "congratulations"}], harvest.infos)
        self.assertListEqual([{"code": "test_code_2", "message": "be careful"}], harvest.warnings)
        self.assertListEqual([{"code": "test_code_3", "message": "oops"}], harvest.errors)
        self.assertEqual("Twitter Harvester", harvest.service)
        self.assertEqual("f0c3c5ef7031", harvest.host)
        self.assertEqual("39", harvest.instance)

        # Now changes harvest options and check that seeds deleted.
        # "deactivate_not_found_seeds": self.cleaned_data["deleted_accounts_option"],
        # "deactivate_unauthorized_seeds": self.cleaned_data["protected_accounts_options"],
        # "deactivate_suspended_seeds": self.cleaned_data["suspended_accounts_option"]
        collection = Collection.objects.get(name="test_collection")
        # Make sure both seeds are on.
        seed_ids = []
        for seed in collection.seeds.all():
            self.assertTrue(seed.is_active)
            seed_ids.append(seed.seed_id)
        collection.harvest_options = json.dumps({
            "deactivate_not_found_seeds": True,
            "deactivate_unauthorized_seeds": False,
            "deactivate_suspended_seeds": False
        })
        collection.save()

        self.consumer.message = {
            "id": "test:1",
            "status": Harvest.SUCCESS,
            "date_started": "2015-07-28T11:18:36.640044",
            "date_ended": "2015-07-28T11:18:42.539470",
            "warnings": [
                {"code": "token_unauthorized", "message": "This token is unauthorized.", "seed_id": seed_ids[0]},
                {"code": "token_not_found", "message": "This token is not found.", "seed_id": seed_ids[1]},
            ],
            "service": "Twitter Harvester",
            "host": "f0c3c5ef7031",
            "instance": "39",
        }
        # Trigger on_message
        self.consumer.on_message()

        unauthorized_seed = Seed.objects.get(seed_id=seed_ids[0])
        self.assertTrue(unauthorized_seed.is_active)

        not_found_seed = Seed.objects.get(seed_id=seed_ids[1])
        self.assertFalse(not_found_seed.is_active)

    @patch("message_consumer.sfm_ui_consumer.collection_stop")
    def test_harvest_status_stream_failed_on_message(self, mock_collection_stop):
        self.consumer.routing_key = "harvest.status.twitter.twitter_sample"
        self.consumer.message = {
            "id": "test:3",
            "status": Harvest.FAILURE,
            "date_started": "2015-07-28T11:17:36.640044",
            "date_ended": "2015-07-28T11:17:42.539470"
        }
        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        harvest = Harvest.objects.get(harvest_id="test:3")
        self.assertEqual(Harvest.FAILURE, harvest.status)
        self.assertFalse(harvest.collection.is_on)

        mock_collection_stop.assert_called_once_with(harvest.collection.id)

    @patch("message_consumer.sfm_ui_consumer.collection_stop")
    def test_rogue_harvest(self, mock_collection_stop):
        self.consumer.routing_key = "harvest.status.twitter.twitter_sample"
        self.consumer.message = {
            "id": "test:3",
            "status": Harvest.RUNNING,
            "date_started": "2015-07-28T11:17:36.640044",
            "date_ended": "2015-07-28T11:17:42.539470"
        }
        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        harvest = Harvest.objects.get(harvest_id="test:3")
        self.assertEqual(Harvest.RUNNING, harvest.status)
        self.assertTrue(harvest.collection.is_on)

        # Mark the harvest as already being completed.
        harvest.status = Harvest.SUCCESS
        harvest.save()

        # Trigger on_message
        self.consumer.on_message()

        mock_collection_stop.assert_called_once_with(harvest.collection.id)

    def test_on_message_ignores_bad_routing_key(self):
        self.consumer.routing_key = "xharvest.status.test.test_search"

        # Trigger on_message and nothing happens
        self.consumer.on_message()

    def test_on_message_ignores_unknown_harvest(self):
        self.consumer.routing_key = "harvest.status.test.test_search"
        self.consumer.message = {
            "id": "xtest:1"
        }
        # Trigger on_message and nothing happens
        self.consumer.on_message()

    def test_warc_created_on_message(self):
        self.consumer.routing_key = "warc_created"
        self.consumer.message = {
            "warc": {
                "path": "/var/folders/_d/3zzlntjs45nbq1f4dnv48c499mgzyf/T/tmpKwq9NL/test_collection_set/2015/07/28/"
                        "11/" +
                        "test_collection_set-flickr-2015-07-28T11:17:36Z.warc.gz",
                "sha1": "7512e1c227c29332172118f0b79b2ca75cbe8979",
                "bytes": 26146,
                "id": "test_collection-flickr-2015-07-28T11:17:36Z",
                "date_created": "2015-07-28T11:17:36.640178"
            },
            "collection_set": {
                "path": "/var/folders/_d/3zzlntjs45nbq1f4dnv48c499mgzyf/T/tmpKwq9NL/test_collection_set",
                "id": "test_collection_set"
            },
            "harvest": {
                "id": "test:1",
            }
        }
        # Trigger on_message
        self.consumer.on_message()

        # Check created Warc model object
        warc = Warc.objects.get(warc_id="test_collection-flickr-2015-07-28T11:17:36Z")
        self.assertEqual(self.consumer.message["warc"]["path"], warc.path)
        self.assertEqual(self.consumer.message["warc"]["sha1"], warc.sha1)
        self.assertEqual(self.consumer.message["warc"]["bytes"], warc.bytes)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:36.640178"), warc.date_created)
        self.assertEqual(self.harvest, warc.harvest)

    def test_export_status_on_message(self):
        self.consumer.routing_key = "export.status.test"
        self.consumer.message = {
            "id": "test:2",
            "status": "running",
            "date_started": "2015-07-28T11:17:36.640044",
            "infos": [{"code": "test_code_1", "message": "congratulations"}],
            "warnings": [{"code": "test_code_2", "message": "be careful"}],
            "errors": [{"code": "test_code_3", "message": "oops"}],
            "service": "Twitter Exporter",
            "host": "f0c3c5ef7031",
            "instance": "39",
        }

        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        export = Export.objects.get(export_id="test:2")
        self.assertEqual("running", export.status)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:36.640044"), export.date_started)
        self.assertIsNone(export.date_ended)
        self.assertListEqual([{"code": "test_code_1", "message": "congratulations"}], export.infos)
        self.assertListEqual([{"code": "test_code_2", "message": "be careful"}], export.warnings)
        self.assertListEqual([{"code": "test_code_3", "message": "oops"}], export.errors)
        self.assertEqual("Twitter Exporter", export.service)
        self.assertEqual("f0c3c5ef7031", export.host)
        self.assertEqual("39", export.instance)

        # Now update
        self.consumer.message = {
            "id": "test:2",
            "status": "completed success",
            "date_started": "2015-07-28T11:17:36.640044",
            "date_ended": "2015-07-28T11:17:42.539470",
            "infos": [{"code": "test_code_1", "message": "congratulations"}],
            "warnings": [{"code": "test_code_2", "message": "be careful"}],
            "errors": [{"code": "test_code_3", "message": "oops"}],
            "service": "Twitter Exporter",
            "host": "f0c3c5ef7031",
            "instance": "39",
        }

        # Trigger on_message
        self.consumer.on_message()

        # Check updated harvest model object
        export = Export.objects.get(export_id="test:2")
        self.assertEqual("completed success", export.status)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:36.640044"), export.date_started)
        self.assertEqual(iso8601.parse_date("2015-07-28T11:17:42.539470"), export.date_ended)
        self.assertListEqual([{"code": "test_code_1", "message": "congratulations"}], export.infos)
        self.assertListEqual([{"code": "test_code_2", "message": "be careful"}], export.warnings)
        self.assertListEqual([{"code": "test_code_3", "message": "oops"}], export.errors)
        self.assertEqual("Twitter Exporter", export.service)
        self.assertEqual("f0c3c5ef7031", export.host)
        self.assertEqual("39", export.instance)
