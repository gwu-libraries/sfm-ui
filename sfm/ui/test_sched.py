from django.test import TestCase
import json
from mock import patch, ANY, call
from .models import SeedSet, Collection, Credential, Group, User
from jobs import seedset_harvest
from datetime import datetime
import pytz
from django.db.models.signals import post_save, pre_delete
from sched import schedule_harvest_receiver, unschedule_harvest_receiver, toggle_seedset_inactive


class ScheduleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=self.group, name="test_collection")
        self.credential_token = {"key": "test_key"}
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token=json.dumps(self.credential_token))

        # Register receivers. This would normally be done in config.py but is disabled for unit tests.
        post_save.connect(schedule_harvest_receiver, sender=SeedSet)
        pre_delete.connect(unschedule_harvest_receiver, sender=SeedSet)

    # Modify Seedset
    @patch("ui.sched.sched", autospec=True)
    def test_modify_seedset(self, mock_scheduler):

        # Add seedset
        # mock_scheduler.get_job.side_effect = [None, True, True, True]
        mock_scheduler.get_job.side_effect = [None, None, True, True]
        end_date = datetime(2207, 12, 22, 17, 31, tzinfo=pytz.utc)
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type="test_type", name="test_seedset", is_active=True,
                                         schedule_minutes=60, end_date=end_date)
        seedset_id = seedset.id

        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_not_called()
        # Using actual calls since ANY doesn't work with has_calls
        actual_calls = mock_scheduler.add_job.mock_calls
        # Add job called to add seedset_harvest and toggle_seedset_inactive.
        mock_scheduler.add_job.assert_has_calls([call(seedset_harvest,
                                                      args=[seedset_id],
                                                      end_date=end_date,
                                                      id=str(seedset_id),
                                                      minutes=60,
                                                      name=actual_calls[0][2]["name"],
                                                      start_date=actual_calls[0][2]["start_date"],
                                                      trigger="interval"

                                                      ),
                                                 call(toggle_seedset_inactive,
                                                      args=[seedset_id],
                                                      id="end_{}".format(seedset_id),
                                                      name=actual_calls[1][2]["name"],
                                                      run_date=end_date,
                                                      trigger="date")
                                                 ])

        # Modify seedset
        seedset.schedule_minutes = 60 * 24
        # Removing the end date.
        seedset.end_date = None
        mock_scheduler.reset_mock()
        seedset.save()
        # mock_scheduler.get_job.assert_called_once_with(str(seedset.id))
        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.add_job.assert_called_once_with(seedset_harvest,
                                                       args=[seedset_id],
                                                       id=str(seedset_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60*24)

    # Modify Inactive Seedset
    @patch("ui.sched.sched", autospec=True)
    def test_modify_inactive_seedset(self, mock_scheduler):

        # Add seedset
        mock_scheduler.get_job.side_effect = [None, None, True, None]
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type="test_type", name="test_seedset", is_active=True,
                                         schedule_minutes=60)
        seedset_id = seedset.id
        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_not_called()
        mock_scheduler.add_job.assert_called_once_with(seedset_harvest,
                                                       args=[seedset_id],
                                                       id=str(seedset_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60)

        # Modify seedset - inactive seedset
        seedset.is_active = False
        mock_scheduler.reset_mock()
        seedset.save()
        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_called_once_with(str(seedset_id))

    # Delete seedset
    @patch("ui.sched.sched", autospec=True)
    def test_delete_seedset(self, mock_scheduler):

        # Add seedset
        mock_scheduler.get_job.side_effect = [None, None, True, None]
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type="test_type", name="test_seedset", is_active=True,
                                         schedule_minutes=60)
        seedset_id = seedset.id
        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_not_called()
        mock_scheduler.add_job.assert_called_once_with(seedset_harvest,
                                                       args=[seedset_id],
                                                       id=str(seedset_id),
                                                       name=ANY,
                                                       trigger="interval",
                                                       start_date=ANY,
                                                       end_date=None,
                                                       minutes=60)

        # Delete seedset
        mock_scheduler.reset_mock()
        seedset.delete()
        mock_scheduler.get_job.assert_has_calls([call(str(seedset_id)), call("end_{}".format(seedset_id))])
        mock_scheduler.remove_job.assert_called_once_with(str(seedset_id))
