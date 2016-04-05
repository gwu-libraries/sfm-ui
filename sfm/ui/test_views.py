from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from ui.models import Collection, User, Credential, Seed, SeedSet
from ui.views import CollectionListView, CollectionDetailView, CollectionUpdateView, SeedSetCreateView


class CollectionListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        credential = Credential.objects.create(user=self.user, platform="test_platform",
                                               token="{}")
        group = Group.objects.create(name='testgroup1')
        self.user.groups.add(group)
        self.user.save()
        self.collection1 = Collection.objects.create(name='Test Collection One',
                                                     group=group)

        SeedSet.objects.create(collection=self.collection1, harvest_type="twitter_search", name="Test SeedSet One",
                               credential=credential)
        group2 = Group.objects.create(name='testgroup2')
        Collection.objects.create(name='Test Collection Two',
                                  group=group2)

    def test_correct_collection_list_for_usergroup(self):
        """
        logged in user should see collections in belonging to the same group
        as the user and not see collections from other groups
        """
        request = self.factory.get('/ui/collections/')
        request.user = self.user
        response = CollectionListView.as_view()(request)
        collection_list = response.context_data["collection_list"]
        self.assertEqual(1, len(collection_list))
        self.assertEqual(self.collection1, collection_list[0])
        self.assertEqual(1, collection_list[0].num_seedsets)


class CollectionTestsMixin:
    def setUp(self):
        self.factory = RequestFactory()
        self.group1 = Group.objects.create(name='testgroup1')
        self.user1 = User.objects.create_user('testuser', 'testuser@example.com',
                                              'password')
        self.user1.groups.add(self.group1)
        self.user1.save()
        self.collection1 = Collection.objects.create(name='Test Collection One',
                                                     group=self.group1)
        self.credential1 = Credential.objects.create(user=self.user1,
                                                     platform='test platform')
        self.seedset = SeedSet.objects.create(collection=self.collection1,
                                              credential=self.credential1,
                                              harvest_type='test harvest type',
                                              name='Test seedset one',
                                              )
        Seed.objects.create(seed_set=self.seedset)
        user2 = User.objects.create_user('testuser2', 'testuser2@example.com',
                                         'password')
        credential2 = Credential.objects.create(user=user2,
                                                platform='test platform')
        group2 = Group.objects.create(name='testgroup2')
        collection2 = Collection.objects.create(name='Test Collection Two',
                                                group=group2)
        SeedSet.objects.create(collection=collection2,
                               credential=credential2,
                               harvest_type='test harvest type',
                               name='Test seedset two')


class CollectionDetailViewTests(CollectionTestsMixin, TestCase):

    def test_seedset_visible(self):
        """
        seedset list should only show seedsets belonging to the collection
        """
        request = self.factory.get('/ui/collections/{}/'.format(self.collection1.pk))
        request.user = self.user1
        response = CollectionDetailView.as_view()(request, pk=self.collection1.pk)
        seedset_list = response.context_data["seedset_list"]
        self.assertEqual(1, len(seedset_list))
        self.assertEqual(self.seedset, seedset_list[0])
        self.assertEqual(1, seedset_list[0].num_seeds)


class CollectionUpdateViewTests(CollectionTestsMixin, TestCase):
    def test_seedset_visible(self):
        """
        seedset list should only show seedsets belonging to the collection
        """
        request = self.factory.put('/ui/collections/{}/'.format(self.collection1.pk))
        request.user = self.user1
        response = CollectionUpdateView.as_view()(request, pk=self.collection1.pk)
        seedset_list = response.context_data["seedset_list"]
        self.assertEqual(1, len(seedset_list))
        self.assertEqual(self.seedset, seedset_list[0])
        self.assertEqual(1, seedset_list[0].num_seeds)


class SeedSetCreateViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection = Collection.objects.create(name='Test Collection One',
                                                    group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform')
        self.seedset = SeedSet.objects.create(collection=self.collection,
                                              credential=self.credential,
                                              harvest_type='test harvest type',
                                              name='Test seedset one',
                                              )
        self.factory = RequestFactory()

    def test_seedset_form_view(self):
        """
        simple test that seedset form loads with collection
        """
        request = self.factory.get(reverse('seedset_create',
                                   args=[self.collection.pk]))
        request.user = self.user
        response = SeedSetCreateView.as_view()(request, collection_pk=self.collection.pk)
        self.assertEqual(self.collection, response.context_data["form"].initial["collection"])
        self.assertEqual(self.collection, response.context_data["collection"])
