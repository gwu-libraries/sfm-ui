from django.test import TestCase
from .notifications import _should_send_email, _create_email, _create_context
from .models import User, Group, CollectionSet, Credential, Collection, Harvest, HarvestStat
import datetime
from collections import OrderedDict


class NotificationTests(TestCase):
    def setUp(self):
        self.group1 = Group.objects.create(name="test_group1")
        self.group2 = Group.objects.create(name="test_group2")
        self.user1 = User.objects.create_user(username="test_user", email="testuser1@gwu.edu")
        self.group1.user_set.add(self.user1)
        self.user2 = User.objects.create_user(username="test_user2", email="testuser2@gwu.edu")
        self.group2.user_set.add(self.user2)
        self.user_no_email = User.objects.create_user(username="test_user3")
        self.collection_set1 = CollectionSet.objects.create(group=self.group1, name="ztest_collection_set1")
        self.collection_set2 = CollectionSet.objects.create(group=self.group1, name="atest_collection_set2")
        # self.collection_set3 = CollectionSet.objects.create(group=self.group1, name="test_collection_set3")
        self.collection_set4 = CollectionSet.objects.create(group=self.group2, name="test_collection_set4")
        self.credential = Credential.objects.create(user=self.user1, platform="test_platform", token='{}')
        self.collection1 = Collection.objects.create(collection_set=self.collection_set1, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="ztest_collection1",
                                                     harvest_options='{}', is_active=False)
        self.collection2 = Collection.objects.create(collection_set=self.collection_set1, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="atest_collection2",
                                                     harvest_options='{}', is_active=True)
        self.collection3 = Collection.objects.create(collection_set=self.collection_set2, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="test_collection3",
                                                     harvest_options='{}', is_active=True)
        self.collection4 = Collection.objects.create(collection_set=self.collection_set4, credential=self.credential,
                                                     harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                     name="test_collection5",
                                                     harvest_options='{}', is_active=False)
        today = datetime.date.today()
        yesterday = today + datetime.timedelta(days=-1)
        prev_day = today + datetime.timedelta(days=-2)
        historical_collection = self.collection2.history.all()[0]
        historical_credential = historical_collection.credential.history.all()[0]

        self.harvest1 = Harvest.objects.create(harvest_id="test_harvest1",
                                               collection=self.collection2,
                                               historical_collection=historical_collection,
                                               historical_credential=historical_credential)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=today,
                                   item="test_type1",
                                   count=100)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=yesterday,
                                   item="test_type1",
                                   count=1)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=yesterday,
                                   item="test_type2",
                                   count=2)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=prev_day,
                                   item="test_type1",
                                   count=11)
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=prev_day,
                                   item="test_type2",
                                   count=12)
        # Last week
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=today + datetime.timedelta(days=-8),
                                   item="test_type1",
                                   count=111)

        # Prev week
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=today + datetime.timedelta(days=-15),
                                   item="test_type1",
                                   count=1111)

        # Prev month
        HarvestStat.objects.create(harvest=self.harvest1,
                                   harvest_date=today + datetime.timedelta(days=-35),
                                   item="test_type1",
                                   count=11111)

    def test_should_send_email_no_email_address(self):
        self.assertFalse(_should_send_email(self.user_no_email, date=datetime.date.today()))

    def test_should_send_email_none(self):
        self.user1.email_frequency = User.NONE
        self.assertFalse(_should_send_email(self.user1))

    def test_should_send_email_daily(self):
        self.user1.email_frequency = User.DAILY
        self.assertTrue(_should_send_email(self.user1))

    def test_should_send_email_weekly(self):
        self.user1.email_frequency = User.WEEKLY
        # If it is Sunday
        self.assertTrue(_should_send_email(self.user1, date=datetime.date(2016, 9, 4)))
        self.assertFalse(_should_send_email(self.user1, date=datetime.date(2016, 9, 5)))

    def test_should_send_email_monthly(self):
        self.user1.email_frequency = User.MONTHLY
        # If it is the 1st
        self.assertTrue(_should_send_email(self.user1, date=datetime.date(2016, 9, 1)))
        self.assertFalse(_should_send_email(self.user1, date=datetime.date(2016, 9, 5)))

    def test_should_send_email_no_active_collections(self):
        self.assertFalse(_should_send_email(self.user2, date=datetime.date.today()))

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
                                      'prev_30': 0,
                                      'last_7': 14,
                                      'yesterday': 2,
                                      'prev_7': 0,
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
