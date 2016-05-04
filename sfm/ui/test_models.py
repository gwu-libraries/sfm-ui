from django.test import TestCase
from .models import User, Collection, Credential, SeedSet, Seed, Group, Harvest


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
