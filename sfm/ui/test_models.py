from django.test import TestCase
from .models import User, CollectionSet, Credential, Collection, Seed, Group, Harvest, HarvestStat
import pytz
from datetime import datetime, date


class CollectionTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection_set = CollectionSet.objects.create(group=group, name="test_collection_set")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")

    def test_required_seed_count(self):
        collection = Collection.objects.create(collection_set=self.collection_set,
                                               name="test_collection",
                                               harvest_type=Collection.TWITTER_USER_TIMELINE,
                                               credential=self.credential)
        self.assertIsNone(collection.required_seed_count())

        collection.harvest_type = Collection.TWITTER_SAMPLE
        self.assertEqual(0, collection.required_seed_count())

    def test_active_seed_count(self):
        collection = Collection.objects.create(collection_set=self.collection_set,
                                               name="test_collection",
                                               harvest_type=Collection.TWITTER_SEARCH,
                                               credential=self.credential)
        self.assertEqual(0, collection.active_seed_count())

        Seed.objects.create(collection=collection, token='{}', is_active=True)
        self.assertEqual(1, collection.active_seed_count())

        Seed.objects.create(collection=collection, token='{}', is_active=False)
        self.assertEqual(1, collection.active_seed_count())

    def test_is_streaming(self):
        collection = Collection.objects.create(collection_set=self.collection_set,
                                               name="test_collection",
                                               harvest_type=Collection.TWITTER_SEARCH,
                                               credential=self.credential)
        self.assertFalse(collection.is_streaming())

        collection.harvest_type = Collection.TWITTER_FILTER
        self.assertTrue(collection.is_streaming())

    def test_last_harvest(self):
        collection = Collection.objects.create(collection_set=self.collection_set,
                                               name="test_collection",
                                               harvest_type=Collection.TWITTER_SEARCH,
                                               credential=self.credential)
        self.assertIsNone(collection.last_harvest())

        historical_collection = collection.history.all()[0]
        historical_credential = historical_collection.credential.history.all()[0]

        # Add a harvest
        harvest1 = Harvest.objects.create(collection=collection,
                                          historical_collection=historical_collection,
                                          historical_credential=historical_credential)
        self.assertEqual(harvest1, collection.last_harvest())

        # Add a second harvest
        harvest2 = Harvest.objects.create(collection=collection,
                                          historical_collection=historical_collection,
                                          historical_credential=historical_credential)

        self.assertEqual(harvest2, collection.last_harvest())

        # Add a web harvest
        harvest3 = Harvest.objects.create(harvest_type="web", collection=collection,
                                          historical_collection=historical_collection,
                                          historical_credential=historical_credential)
        self.assertEqual(harvest2, collection.last_harvest())
        self.assertEqual(harvest3, collection.last_harvest(include_web_harvests=True))

        # Add a skipped harvest
        harvest4 = Harvest.objects.create(status=Harvest.SKIPPED, collection=collection,
                                          historical_collection=historical_collection,
                                          historical_credential=historical_credential)
        self.assertEqual(harvest2, collection.last_harvest())
        self.assertEqual(harvest4, collection.last_harvest(include_skipped=True))

    def test_stats(self):
        collection1 = Collection.objects.create(collection_set=self.collection_set,
                                                name="test_collection",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=self.credential)
        historical_collection1 = collection1.history.all()[0]
        historical_credential1 = historical_collection1.credential.history.all()[0]
        harvest1 = Harvest.objects.create(collection=collection1,
                                          historical_collection=historical_collection1,
                                          historical_credential=historical_credential1)
        day1 = date(2016, 5, 20)
        day2 = date(2016, 5, 21)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=7, harvest_date=day2)
        harvest2 = Harvest.objects.create(collection=collection1,
                                          historical_collection=historical_collection1,
                                          historical_credential=historical_credential1)
        HarvestStat.objects.create(harvest=harvest2, item="tweets", count=5, harvest_date=day2)
        harvest3 = Harvest.objects.create(parent_harvest=harvest1,
                                          collection=collection1)
        HarvestStat.objects.create(harvest=harvest3, item="web resources", count=25, harvest_date=day2)

        # Add some extraneous stats.
        collection2 = Collection.objects.create(collection_set=self.collection_set,
                                                name="test_collection2",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=self.credential)
        historical_collection2 = collection2.history.all()[0]
        historical_credential2 = historical_collection2.credential.history.all()[0]
        harvest4 = Harvest.objects.create(collection=collection2,
                                          historical_collection=historical_collection2,
                                          historical_credential=historical_credential2)
        HarvestStat.objects.create(harvest=harvest4, item="tweets", count=7, harvest_date=day1)

        stats = collection1.stats()
        self.assertEqual(17, stats["tweets"])
        self.assertEqual(6, stats["users"])
        self.assertEqual(25, stats["web resources"])

    def test_warc_totals(self):
        collection1 = Collection.objects.create(collection_set=self.collection_set,
                                                name="test_collection",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=self.credential)
        historical_collection1 = collection1.history.all()[0]
        historical_credential1 = historical_collection1.credential.history.all()[0]
        Harvest.objects.create(collection=collection1,
                               historical_collection=historical_collection1,
                               historical_credential=historical_credential1,
                               warcs_count=1, warcs_bytes=10)
        Harvest.objects.create(collection=collection1,
                               historical_collection=historical_collection1,
                               historical_credential=historical_credential1,
                               warcs_count=2, warcs_bytes=20)
        self.assertEqual(3, collection1.warcs_count())
        self.assertEqual(30, collection1.warcs_bytes())


class CollectionSetTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection_set = CollectionSet.objects.create(group=group, name="test_collection_set")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")
        collection1 = Collection.objects.create(collection_set=self.collection_set,
                                                name="test_collection",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=self.credential)
        datetime1 = datetime(2016, 5, 18, 17, 31, tzinfo=pytz.utc)
        day1 = date(2016, 5, 18)
        self.day2 = date(2016, 5, 19)
        historical_collection1 = collection1.history.all()[0]
        historical_credential1 = historical_collection1.credential.history.all()[0]
        harvest1 = Harvest.objects.create(collection=collection1,
                                          historical_collection=historical_collection1,
                                          historical_credential=historical_credential1,
                                          date_requested=datetime1,
                                          warcs_count=1, warcs_bytes=10)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=harvest1, item="tweets", count=7, harvest_date=self.day2)
        # Same day
        harvest2 = Harvest.objects.create(collection=collection1,
                                          historical_collection=historical_collection1,
                                          historical_credential=historical_credential1,
                                          date_requested=datetime1,
                                          warcs_count=2, warcs_bytes=20)
        HarvestStat.objects.create(harvest=harvest2, item="tweets", count=5, harvest_date=day1)

        collection2 = Collection.objects.create(collection_set=self.collection_set,
                                                name="test_collection2",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=self.credential)
        historical_collection2 = collection2.history.all()[0]
        historical_credential2 = historical_collection2.credential.history.all()[0]
        # Different day
        harvest3 = Harvest.objects.create(collection=collection2,
                                          historical_collection=historical_collection2,
                                          historical_credential=historical_credential2,
                                          date_requested=datetime1,
                                          warcs_count=3, warcs_bytes=30)
        HarvestStat.objects.create(harvest=harvest3, item="tweets", count=7, harvest_date=self.day2)

    def test_stats(self):
        stats = self.collection_set.stats()
        self.assertEqual(24, stats["tweets"])
        self.assertEqual(6, stats["users"])

    def test_warc_totals(self):
        self.assertEqual(6, self.collection_set.warcs_count())
        self.assertEqual(60, self.collection_set.warcs_bytes())

    def test_stats_item(self):
        self.assertListEqual([(date(2016, 5, 16), 0),
                              (date(2016, 5, 17), 0),
                              (date(2016, 5, 18), 10),
                              (date(2016, 5, 19), 14)],
                             self.collection_set.item_stats("tweets", end_date=self.day2, days=4))
        self.assertListEqual([(date(2016, 5, 16), 0),
                              (date(2016, 5, 17), 0),
                              (date(2016, 5, 18), 6),
                              (date(2016, 5, 19), 0)],
                             self.collection_set.item_stats("users", end_date=self.day2, days=4))

    def test_stats_items(self):
        self.assertListEqual(['tweets', 'users'], self.collection_set.stats_items())


class HarvestTest(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        collection_set = CollectionSet.objects.create(group=group, name="test_collection_set")
        credential = Credential.objects.create(user=user, platform="test_platform",
                                               token="{}")
        collection1 = Collection.objects.create(collection_set=collection_set,
                                                name="test_collection",
                                                harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                credential=credential)
        datetime1 = datetime(2016, 5, 18, 17, 31, tzinfo=pytz.utc)
        day1 = date(2016, 5, 18)
        day2 = date(2016, 5, 19)
        historical_collection1 = collection1.history.all()[0]
        historical_credential1 = historical_collection1.credential.history.all()[0]
        self.harvest1 = Harvest.objects.create(collection=collection1,
                                               historical_collection=historical_collection1,
                                               historical_credential=historical_credential1,
                                               date_requested=datetime1)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=5, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="users", count=6, harvest_date=day1)
        HarvestStat.objects.create(harvest=self.harvest1, item="tweets", count=7, harvest_date=day2)

    def test_stats(self):
        stats = self.harvest1.stats()
        self.assertEqual(12, stats["tweets"])
        self.assertEqual(6, stats["users"])
