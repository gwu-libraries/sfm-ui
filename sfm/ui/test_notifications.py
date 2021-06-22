from django.test import TestCase
from .notifications import _should_send_email, _create_email, _create_context, _create_space_email, \
    _should_send_space_email, get_warn_queue, _create_queue_warn_email, _was_harvest_in_range, MonitorSpace
from .models import User, Group, CollectionSet, Credential, Collection, Harvest, HarvestStat
import datetime
from collections import OrderedDict
from mock import patch
import pytz


class NotificationTests(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.group1 = Group.objects.create(name="test_group1")
        self.group2 = Group.objects.create(name="test_group2")
        self.user1 = User.objects.create_user(username="test_user", email="testuser1@gwu.edu")
        self.group1.user_set.add(self.user1)
        self.user2 = User.objects.create_user(username="test_user2", email="testuser2@gwu.edu")
        self.group2.user_set.add(self.user2)
        self.user_no_email = User.objects.create_user(username="test_user3")
        self.collection_set1 = CollectionSet.objects.create(group=self.group1, name="ztest_collection_set1")
        self.collection_set2 = CollectionSet.objects.create(group=self.group1, name="atest_collection_set2")
        self.collection_set4 = CollectionSet.objects.create(group=self.group2, name="test_collection_set4")
        self.collection_set5 = CollectionSet.objects.create(group=self.group1, name="test_collection_set5")
        self.credential = Credential.objects.create(user=self.user1, platform="test_platform", token='{}')
        self.collection1 = Collection.objects.create(collection_set=self.collection_set1, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="ztest_collection1",
                                                     harvest_options='{}', is_on=False)
        self.collection2 = Collection.objects.create(collection_set=self.collection_set1, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="atest_collection2",
                                                     harvest_options='{}', is_on=True)
        self.collection3 = Collection.objects.create(collection_set=self.collection_set2, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="test_collection3",
                                                     harvest_options='{}', is_on=True)
        self.collection4 = Collection.objects.create(collection_set=self.collection_set4, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="test_collection5",
                                                     harvest_options='{}', is_on=False)
        self.collection5 = Collection.objects.create(collection_set=self.collection_set5, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="test_collection5",
                                                     harvest_options='{}', is_on=False, is_active=False)
        self.today = datetime.datetime.utcnow().date()
        self.yesterday = self.today + datetime.timedelta(days=-1)
        self.prev_day = self.today + datetime.timedelta(days=-2)
        self.today_dt = datetime.datetime.now(pytz.utc)
        self.yesterday_dt = self.today_dt + datetime.timedelta(days=-1)
        self.prev_day_dt = self.today_dt + datetime.timedelta(days=-2)

        self.historical_collection = self.collection2.history.all()[0]
        self.historical_credential = self.historical_collection.credential.history.all()[0]

        self.harvest1 = Harvest.objects.create(harvest_id="test_harvest1",
                                               collection=self.collection2,
                                               historical_collection=self.historical_collection,
                                               historical_credential=self.historical_credential)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.today,
                                   item="test_type1",
                                   count=100)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.yesterday,
                                   item="test_type1",
                                   count=1)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.yesterday,
                                   item="test_type2",
                                   count=2)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.prev_day,
                                   item="test_type1",
                                   count=11)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.prev_day,
                                   item="test_type2",
                                   count=12)
        # Last week
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.today + datetime.timedelta(days=-8),
                                   item="test_type1",
                                   count=111)

        # Prev week
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.today + datetime.timedelta(days=-15),
                                   item="test_type1",
                                   count=1111)

        # Prev month
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=self.today + datetime.timedelta(days=-35),
                                   item="test_type1",
                                   count=11111)

    def test_should_send_email_no_email_address(self):
        self.assertFalse(_should_send_email(self.user_no_email, today=datetime.date.today()))

    def test_should_send_email_none(self):
        self.user1.email_frequency = User.NONE
        self.assertFalse(_should_send_email(self.user1))

    def test_should_send_email_daily(self):
        self.user1.email_frequency = User.DAILY
        self.assertTrue(_should_send_email(self.user1))

    def test_should_send_email_weekly(self):
        self.user1.email_frequency = User.WEEKLY
        # If it is Sunday
        self.assertTrue(_should_send_email(self.user1, today=datetime.date(2016, 9, 4)))
        self.assertFalse(_should_send_email(self.user1, today=datetime.date(2016, 9, 5)))

    def test_should_send_email_monthly(self):
        self.user1.email_frequency = User.MONTHLY
        # If it is the 1st
        self.assertTrue(_should_send_email(self.user1, today=datetime.date(2016, 9, 1)))
        self.assertFalse(_should_send_email(self.user1, today=datetime.date(2016, 9, 5)))

    def test_should_send_email_no_active_collections(self):
        self.assertFalse(_should_send_email(self.user2, today=datetime.date.today()))

    def test_create_context(self):
        self.assertEqual(
            {'url': 'http://example.com/ui/',
             'collection_sets': OrderedDict([(
                 self.collection_set2, {
                     'url': 'http://example.com/ui/collection_sets/2/',
                     'collections': OrderedDict([(
                         self.collection3, {
                             'url': 'http://example.com/ui/collections/3/',
                             'next_run_time': None,
                             'stats': {}})])}), (
                 self.collection_set1, {
                     'url': 'http://example.com/ui/collection_sets/1/',
                     'collections': OrderedDict([(
                         self.collection2, {
                             'url': 'http://example.com/ui/collections/2/',
                             'next_run_time': None,
                             'stats': {
                                 u'test_type2': {
                                     'prev_day': 12,
                                     'prev_30': 'N/A',
                                     'last_7': 14,
                                     'yesterday': 2,
                                     'prev_7': 'N/A',
                                     'last_30': 14},
                                 u'test_type1': {
                                     'prev_day': 11,
                                     'prev_30': 11111,
                                     'last_7': 12,
                                     'yesterday': 1,
                                     'prev_7': 111,
                                     'last_30': 1234}}}),
                         (
                             self.collection1,
                             {
                                 'url': 'http://example.com/ui/collections/1/'})])})])},
            _create_context(self.user1, {}))

    def test_create_email(self):
        msg = _create_email(self.user1, {})
        self.assertTrue(msg.body.startswith("Here's an update on your harvests from Social Feed Manager "
                                            "(http://example.com/ui/)."))
        self.assertEqual([self.user1.email], msg.to)

    def test_was_harvest_in_range1(self):
        # Starts before range and ends during range
        self.assertFalse(_was_harvest_in_range(self.prev_day, self.yesterday, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.prev_day_dt + datetime.timedelta(hours=-12),
                               date_ended=self.prev_day_dt + datetime.timedelta(hours=12))
        self.assertTrue(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_was_harvest_in_range2(self):
        # Starts during range and ends after range.
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.yesterday_dt + datetime.timedelta(hours=-12),
                               date_ended=self.yesterday_dt + datetime.timedelta(hours=12))
        self.assertTrue(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_was_harvest_in_range3(self):
        # Starts and ends during range
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.yesterday_dt + datetime.timedelta(hours=-18),
                               date_ended=self.yesterday_dt + datetime.timedelta(hours=-12))
        self.assertTrue(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_was_harvest_in_range4(self):
        # Starts before range and ends after range
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.prev_day_dt + datetime.timedelta(hours=-12),
                               date_ended=self.yesterday_dt + datetime.timedelta(days=1))
        self.assertTrue(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_was_harvest_in_range5(self):
        # Running harvest
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.RUNNING,
                               date_started=self.prev_day_dt + datetime.timedelta(hours=12))
        self.assertTrue(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_web_harvest_was_not_in_range(self):
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="web",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.prev_day_dt + datetime.timedelta(hours=-12),
                               date_ended=self.prev_day_dt + datetime.timedelta(hours=12))
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday, self.collection1))

    def test_was_not_in_harvest_in_range_before(self):
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.prev_day_dt + datetime.timedelta(days=-1),
                               date_ended=self.prev_day_dt + datetime.timedelta(hours=-12))
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_was_not_in_harvest_in_range_after(self):
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.SUCCESS,
                               date_started=self.yesterday_dt + datetime.timedelta(days=1),
                               date_ended=self.yesterday_dt + datetime.timedelta(days=2))
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_voided_harvest_was_not_in_range(self):
        # Voided harvest
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.VOIDED,
                               date_started=self.prev_day_dt + datetime.timedelta(hours=12))
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

    def test_running_after_harvest_was_not_in_range(self):
        # Running harvest that started after range
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))

        # Started before range start and ended during range
        Harvest.objects.create(harvest_id="test_harvest",
                               harvest_type="user_timeline",
                               collection=self.collection1,
                               historical_collection=self.historical_collection,
                               historical_credential=self.historical_credential,
                               status=Harvest.RUNNING,
                               date_started=self.yesterday + datetime.timedelta(days=1))
        self.assertFalse(_was_harvest_in_range(self.prev_day_dt, self.yesterday_dt, self.collection1))


class SpaceNotificationTests(TestCase):
    def setUp(self):
        # self.superuser = User.objects.create_superuser(username="superuser", email="superuser@test.com",
        #                                                password="test_password")
        self.user = User.objects.create_user(username="test_user", email="testuser@test.com")
        self.user_no_email = User.objects.create_user(username="test_user3")

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_db(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['/dev/sda1        204800M 50949M   102400M  50% /sfm-db-data']
        data_monitor = MonitorSpace('/sfm-db-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('200.0GB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('100.0GB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(50, space_msg_cache['space_data']['percentage'])
        self.assertTrue(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_mq(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['/dev/sda1        204800M 50949M   102400M  50% /sfm-mq-data']
        data_monitor = MonitorSpace('/sfm-mq-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('200.0GB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('100.0GB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(50, space_msg_cache['space_data']['percentage'])
        self.assertTrue(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_export(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['/dev/sda1        204800M 50949M   102400M  50% /sfm-export-data']
        data_monitor = MonitorSpace('/sfm-export-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('200.0GB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('100.0GB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(50, space_msg_cache['space_data']['percentage'])
        self.assertTrue(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_containers(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['/dev/sda1        204800M 50949M   102400M  50% /sfm-containers-data']
        data_monitor = MonitorSpace('/sfm-containers-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('200.0GB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('100.0GB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(50, space_msg_cache['space_data']['percentage'])
        self.assertTrue(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_collection_set(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['/dev/sda1        204800M 50949M   102400M  50% /sfm-collection-set-data']
        data_monitor = MonitorSpace('/sfm-collection-set-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('200.0GB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('100.0GB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(50, space_msg_cache['space_data']['percentage'])
        self.assertTrue(space_msg_cache['space_data']['send_email'])



    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_empty_db(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['']
        data_monitor = MonitorSpace('/sfm-db-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(0, space_msg_cache['space_data']['percentage'])
        self.assertFalse(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_empty_mq(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['']
        data_monitor = MonitorSpace('/sfm-mq-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(0, space_msg_cache['space_data']['percentage'])
        self.assertFalse(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_empty_export(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['']
        data_monitor = MonitorSpace('/sfm-export-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(0, space_msg_cache['space_data']['percentage'])
        self.assertFalse(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_empty_containers(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['']
        data_monitor = MonitorSpace('/sfm-containers-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(0, space_msg_cache['space_data']['percentage'])
        self.assertFalse(space_msg_cache['space_data']['send_email'])

    @patch("ui.notifications.MonitorSpace.run_check_cmd", autospec=True)
    def test_get_free_info_empty_collection_set(self, mock_run_cmd):
        mock_run_cmd.side_effect = ['']
        data_monitor = MonitorSpace('/sfm-collection-set-data', '200GB')
        space_msg_cache = {'space_data': data_monitor.get_space_info()}
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_space'])
        self.assertEqual('0.0MB', space_msg_cache['space_data']['total_free_space'])
        self.assertEqual(0, space_msg_cache['space_data']['percentage'])
        self.assertFalse(space_msg_cache['space_data']['send_email'])


    def test_should_send_space_email_space_below(self):
        msg_cache = {
            'space_data': [{'volume_id': '/sfm-db-data', 'threshold': '200GB', 'bar_color': 'progress-bar-success',
                            'total_space': '200GB', 'total_free_space': '100GB', 'percentage': 50, 'send_email': True},
                           {'volume_id': '/sfm-processing', 'threshold': '200GB', 'bar_color': 'progress-bar-success',
                            'total_space': '0.0MB', 'total_free_space': '0.0MB', 'percentage': 0, 'send_email': False}]
        }
        self.assertTrue(_should_send_space_email(msg_cache))


    def test_should_send_space_email_space_over(self):
        msg_cache = {
            'space_data': [{'volume_id': '/sfm-db-data', 'threshold': '50GB', 'bar_color': 'progress-bar-success',
                            'total_space': '200GB', 'total_free_space': '100GB', 'percentage': 50, 'send_email': False},
                           {'volume_id': '/sfm-processing', 'threshold': '200GB', 'bar_color': 'progress-bar-success',
                            'total_space': '0.0MB', 'total_free_space': '0.0MB', 'percentage': 0, 'send_email': False}]
        }
        self.assertFalse(_should_send_space_email(msg_cache))

    def test_create_email(self):
        msg = _create_space_email("superuser@test.com", {})
        self.assertTrue(msg.body.startswith("This is a warning that free space on your Social Feed Manager server at "
                                            "http://example.com/ui/ is low."))
        self.assertEqual(["superuser@test.com"], msg.to)


class QueueNotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", email="testuser@test.com")
        self.user_no_email = User.objects.create_user(username="test_user3")

    @patch("ui.monitoring.monitor_queues", autospec=True)
    def test_get_queue_info(self, mock_monitor_queues):
        mock_monitor_queues.return_value = ({'Twitter Rest Harvester': 0, 'Web Harvester': 0, 'Flickr Harvester': 0,
                                             'Tumblr Harvester': 0, 'Twitter Harvester': 0, 'Weibo Harvester': 0},
                                            {'Weibo Exporter': 0, 'Twitter Stream Exporter': 0,
                                             'Twitter Rest Exporter': 0, 'Tumblr Exporter': 0, 'Flickr Exporter': 0},
                                            {'Sfm Ui': 0})

        msg_cache = {}
        queue_th_map = {'Twitter Rest Harvester': '20', 'Web Harvester': '10'}
        queue_th_other = '10'
        msg_cache['queue_data'] = get_warn_queue(queue_th_map, queue_th_other)
        self.assertEqual([], msg_cache['queue_data'])

    @patch("ui.monitoring.monitor_queues", autospec=True)
    def test_get_queue_info_full(self, mock_monitor_queues):
        mock_monitor_queues.return_value = ({'Twitter Rest Harvester': 100, 'Web Harvester': 50, 'Flickr Harvester': 0,
                                             'Tumblr Harvester': 200, 'Twitter Harvester': 0, 'Weibo Harvester': 0},
                                            {'Weibo Exporter': 0, 'Twitter Stream Exporter': 5,
                                             'Twitter Rest Exporter': 100, 'Tumblr Exporter': 0, 'Flickr Exporter': 0},
                                            {'Sfm Ui': 25})

        msg_cache = {}
        queue_th_map = {'Twitter Rest Harvester': '20', 'Web Harvester': '25', 'Sfm Ui': '15'}
        queue_th_other = '10'
        msg_cache['queue_data'] = get_warn_queue(queue_th_map, queue_th_other)
        self.assertEqual(dict(
            [('Twitter Rest Harvester', 100), ('Web Harvester', 50), ('Tumblr Harvester', 200),
             ('Twitter Rest Exporter', 100), ('Sfm Ui', 25)]),
            dict(msg_cache['queue_data']))

    def test_create_email(self):
        msg = _create_queue_warn_email("superuser@test.com", {})
        self.assertTrue(msg.body.startswith("The following message queues on your Social Feed Manager server at "
                                            "http://example.com/ui/"))
        self.assertEqual(["superuser@test.com"], msg.to)
