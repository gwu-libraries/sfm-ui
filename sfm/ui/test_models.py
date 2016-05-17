from django.test import TestCase
from .models import User, Collection, Credential, SeedSet, Seed, Group, Harvest, HarvestStat
import pytz
from datetime import datetime, date


class SeedsetTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=group, name="test_collection")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")

    def test_required_seed_count(self):
        seedset = SeedSet.objects.create(collection=self.collection,
                                         name="test_seedset",
                                         harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                         credential=self.credential)
        self.assertIsNone(seedset.required_seed_count())

        seedset.harvest_type = SeedSet.TWITTER_SAMPLE
        self.assertEqual(0, seedset.required_seed_count())

    def test_active_seed_count(self):
        seedset = SeedSet.objects.create(collection=self.collection,
                                         name="test_seedset",
                                         harvest_type=SeedSet.TWITTER_SEARCH,
                                         credential=self.credential)
        self.assertEqual(0, seedset.active_seed_count())

        Seed.objects.create(seed_set=seedset, token='{}', is_active=True)
        self.assertEqual(1, seedset.active_seed_count())

        Seed.objects.create(seed_set=seedset, token='{}', is_active=False)
        self.assertEqual(1, seedset.active_seed_count())

    def test_is_streaming(self):
        seedset = SeedSet.objects.create(collection=self.collection,
                                         name="test_seedset",
                                         harvest_type=SeedSet.TWITTER_SEARCH,
                                         credential=self.credential)
        self.assertFalse(seedset.is_streaming())

        seedset.harvest_type = SeedSet.TWITTER_FILTER
        self.assertTrue(seedset.is_streaming())

    def test_last_harvest(self):
        seedset = SeedSet.objects.create(collection=self.collection,
                                         name="test_seedset",
                                         harvest_type=SeedSet.TWITTER_SEARCH,
                                         credential=self.credential)
        self.assertIsNone(seedset.last_harvest())

        historical_seed_set = seedset.history.all()[0]
        historical_credential = historical_seed_set.credential.history.all()[0]

        harvest1 = Harvest.objects.create(seed_set=seedset,
                                          historical_seed_set=historical_seed_set,
                                          historical_credential=historical_credential)
        self.assertEqual(harvest1, seedset.last_harvest())

        harvest2 = Harvest.objects.create(seed_set=seedset,
                                          historical_seed_set=historical_seed_set,
                                          historical_credential=historical_credential)

        self.assertEqual(harvest2, seedset.last_harvest())

        Harvest.objects.create(harvest_type="web", seed_set=seedset,
                               historical_seed_set=historical_seed_set,
                               historical_credential=historical_credential)

        self.assertEqual(harvest2, seedset.last_harvest())

    def test_stats(self):
        seedset1 = SeedSet.objects.create(collection=self.collection,
                                          name="test_seedset",
                                          harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                          credential=self.credential)
        historical_seed_set1 = seedset1.history.all()[0]
        historical_credential1 = historical_seed_set1.credential.history.all()[0]
        harvest1 = Harvest.objects.create(seed_set=seedset1,
                                          historical_seed_set=historical_seed_set1,
                                          historical_credential=historical_credential1)
        day1 = date(2016, 5, 20)
        day2 = date(2016, 5, 21)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=7, harvest_date=day2)
        harvest2 = Harvest.objects.create(seed_set=seedset1,
                                          historical_seed_set=historical_seed_set1,
                                          historical_credential=historical_credential1)
        HarvestStat.objects.create(harvest=harvest2, item="tweets", count=5, harvest_date=day2)
        harvest3 = Harvest.objects.create(parent_harvest = harvest1,
                                          seed_set=seedset1)
        HarvestStat.objects.create(harvest=harvest3, item="web resources", count=25, harvest_date=day2)

        # Add some extraneous stats.
        seedset2 = SeedSet.objects.create(collection=self.collection,
                                          name="test_seedset2",
                                          harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                          credential=self.credential)
        historical_seed_set2 = seedset2.history.all()[0]
        historical_credential2 = historical_seed_set2.credential.history.all()[0]
        harvest4 = Harvest.objects.create(seed_set=seedset2,
                                          historical_seed_set=historical_seed_set2,
                                          historical_credential=historical_credential2)
        HarvestStat.objects.create(harvest=harvest4, item="tweets", count=7, harvest_date=day1)

        stats = seedset1.stats()
        self.assertEqual(17, stats["tweets"])
        self.assertEqual(6, stats["users"])
        self.assertEqual(25, stats["web resources"])


class CollectionTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=group, name="test_collection")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")
        seedset1 = SeedSet.objects.create(collection=self.collection,
                                          name="test_seedset",
                                          harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                          credential=self.credential)
        datetime1 = datetime(2016, 5, 18, 17, 31, tzinfo=pytz.utc)
        day1 = date(2016, 5, 18)
        self.day2 = date(2016, 5, 19)
        historical_seed_set1 = seedset1.history.all()[0]
        historical_credential1 = historical_seed_set1.credential.history.all()[0]
        harvest1 = Harvest.objects.create(seed_set=seedset1,
                                          historical_seed_set=historical_seed_set1,
                                          historical_credential=historical_credential1,
                                          date_requested=datetime1)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=7, harvest_date=self.day2)
        # Same day
        harvest2 = Harvest.objects.create(seed_set=seedset1,
                                          historical_seed_set=historical_seed_set1,
                                          historical_credential=historical_credential1,
                                          date_requested=datetime1)
        HarvestStat.objects.create(harvest=harvest2, item="tweets", count=5, harvest_date=day1)

        seedset2 = SeedSet.objects.create(collection=self.collection,
                                          name="test_seedset2",
                                          harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                          credential=self.credential)
        historical_seed_set2 = seedset2.history.all()[0]
        historical_credential2 = historical_seed_set2.credential.history.all()[0]
        # Different day
        harvest3 = Harvest.objects.create(seed_set=seedset2,
                                          historical_seed_set=historical_seed_set2,
                                          historical_credential=historical_credential2,
                                          date_requested=datetime1)
        HarvestStat.objects.create(harvest=harvest3, item="tweets", count=7, harvest_date=self.day2)

    def test_stats(self):
        stats = self.collection.stats()
        self.assertEqual(24, stats["tweets"])
        self.assertEqual(6, stats["users"])

    def test_stats_item(self):
        self.assertListEqual([(date(2016, 5, 16), 0),
                              (date(2016, 5, 17), 0),
                              (date(2016, 5, 18), 10),
                              (date(2016, 5, 19), 14)],
                             self.collection.item_stats("tweets", end_date=self.day2, days=4))
        self.assertListEqual([(date(2016, 5, 16), 0),
                              (date(2016, 5, 17), 0),
                              (date(2016, 5, 18), 6),
                              (date(2016, 5, 19), 0)],
                             self.collection.item_stats("users", end_date=self.day2, days=4))

    def test_stats_items(self):
        self.assertListEqual(['tweets', 'users'], self.collection.stats_items())


class HarvestTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        collection = Collection.objects.create(group=group, name="test_collection")
        credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")
        seedset1 = SeedSet.objects.create(collection=collection,
                                          name="test_seedset",
                                          harvest_type=SeedSet.TWITTER_USER_TIMELINE,
                                          credential=credential)
        datetime1 = datetime(2016, 5, 18, 17, 31, tzinfo=pytz.utc)
        day1 = date(2016, 5, 18)
        day2 = date(2016, 5, 19)
        historical_seed_set1 = seedset1.history.all()[0]
        historical_credential1 = historical_seed_set1.credential.history.all()[0]
        self.harvest1 = Harvest.objects.create(seed_set=seedset1,
                                          historical_seed_set=historical_seed_set1,
                                          historical_credential=historical_credential1,
                                          date_requested=datetime1)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=7, harvest_date=day2)

    def test_stats(self):
        stats = self.harvest1.stats()
        self.assertEqual(12, stats["tweets"])
        self.assertEqual(6, stats["users"])
