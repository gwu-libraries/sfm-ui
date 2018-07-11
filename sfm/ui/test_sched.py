from django.test import TestCase
import json
from mock import patch, ANY, call
from .models import Collection, CollectionSet, Credential, Group, User, Harvest
from .jobs import collection_harvest
from datetime import datetime
import pytz
from django.db.models.signals import post_save, pre_delete
from .sched import schedule_harvest_receiver, unschedule_harvest_receiver, toggle_collection_inactive


class ScheduleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection_set = CollectionSet.objects.create(group=self.group, name="test_collection_set")
        self.credential_token = {"key": "test_key"}
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token=json.dumps(self.credential_token))

        # Register receivers. This would normally be done in config.py but is disabled for unit tests.
        post_save.connect(schedule_harvest_receiver, sender=Collection)
        pre_delete.connect(unschedule_harvest_receiver, sender=Collection)

    @patch("ui.sched.sched", autospec=True)
    def test_modify_collection(self, mock_scheduler):
        # Add collection
        mock_scheduler.get_job.side_effect = [None, None, True, True]
        end_date = datetime(2207, 12, 22, 17, 31, tzinfo=pytz.utc)
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type="test_type", name="test_collection", is_on=True,
                                               schedule_minutes=60, end_date=end_date)
        collection_id = collection.id

        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_not_called()
        # Using actual calls since ANY doesn't work with has_calls
        actual_calls = mock_scheduler.add_job.mock_calls
        # Add job called to add collection_harvest and toggle_collection_inactive.
        mock_scheduler.add_job.assert_has_calls([call(collection_harvest,
                                                      args=[collection_id],
                                                      end_date=end_date,
                                                      id=str(collection_id),
                                                      minutes=60,
                                                      name=actual_calls[0][2]["name"],
                                                      start_date=actual_calls[0][2]["start_date"],
                                                      trigger="interval"

                                                      ),
                                                 call(toggle_collection_inactive,
                                                      args=[collection_id],
                                                      id="end_{}".format(collection_id),
                                                      name=actual_calls[1][2]["name"],
                                                      run_date=end_date,
                                                      trigger="date")
                                                 ])

        # Modify collection
        collection.schedule_minutes = 60 * 24
        # Removing the end date.
        collection.end_date = None
        mock_scheduler.reset_mock()
        collection.save()
        # mock_scheduler.get_job.assert_called_once_with(str(collection.id))
        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.add_job.assert_called_once_with(collection_harvest,
                                                       args=[collection_id],
                                                       id=str(collection_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60 * 24)

    # Modify Inactive Collection
    @patch("ui.sched.sched", autospec=True)
    def test_modify_inactive_collection(self, mock_scheduler):
        # Add collection
        mock_scheduler.get_job.side_effect = [None, None, True, None]
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type="test_type", name="test_collection", is_on=True,
                                               schedule_minutes=60)
        collection_id = collection.id
        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_not_called()
        mock_scheduler.add_job.assert_called_once_with(collection_harvest,
                                                       args=[collection_id],
                                                       id=str(collection_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60)

        # Modify collection - inactive collection
        collection.is_on = False
        mock_scheduler.reset_mock()
        collection.save()
        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_called_once_with(str(collection_id))

    # Delete collection
    @patch("ui.sched.sched", autospec=True)
    def test_delete_collection(self, mock_scheduler):
        # Add collection
        mock_scheduler.get_job.side_effect = [None, None, True, None]
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type="test_type", name="test_collection", is_on=True,
                                               schedule_minutes=60)
        collection_id = collection.id
        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_not_called()
        mock_scheduler.add_job.assert_called_once_with(collection_harvest,
                                                       args=[collection_id],
                                                       id=str(collection_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60)

        # Delete collection
        mock_scheduler.reset_mock()
        collection.delete()
        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_called_once_with(str(collection_id))

    @patch("ui.sched.sched", autospec=True)
    @patch("ui.sched.collection_stop")
    def test_modify_streaming_collection(self, mock_collection_stop, mock_scheduler):
        # Add collection
        mock_scheduler.get_job.side_effect = [None, None, True, True]
        end_date = datetime(2207, 12, 22, 17, 31, tzinfo=pytz.utc)
        collection = Collection.objects.create(collection_set=self.collection_set, credential=self.credential,
                                               harvest_type=Collection.TWITTER_SAMPLE, name="test_collection",
                                               is_on=True,
                                               end_date=end_date)
        collection_id = collection.id

        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_not_called()
        mock_collection_stop.assert_not_called()
        # Using actual calls since ANY doesn't work with has_calls
        actual_calls = mock_scheduler.add_job.mock_calls
        # Add job called to add toggle_collection_inactive.
        mock_scheduler.add_job.assert_has_calls([call(toggle_collection_inactive,
                                                      args=[collection_id],
                                                      id="end_{}".format(collection_id),
                                                      name=actual_calls[1][2]["name"],
                                                      run_date=end_date,
                                                      trigger="date")
                                                 ])

        # Add a harvest
        historical_collection = collection.history.all()[0]
        historical_credential = historical_collection.credential.history.all()[0]

        Harvest.objects.create(collection=collection,
                               historical_collection=historical_collection,
                               historical_credential=historical_credential)
        # Modify collection
        collection.end_date = None
        collection.is_on = False
        mock_scheduler.reset_mock()
        collection.save()

        mock_scheduler.get_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_scheduler.remove_job.assert_has_calls([call(str(collection_id)), call("end_{}".format(collection_id))])
        mock_collection_stop.assert_called_once_with(collection_id)
