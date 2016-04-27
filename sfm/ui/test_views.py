from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.conf import settings
from django.core.exceptions import PermissionDenied

from .models import Collection, User, Credential, Seed, SeedSet, Export
from .views import CollectionListView, CollectionDetailView, CollectionUpdateView, SeedSetCreateView, \
    SeedSetDetailView, SeedUpdateView, SeedCreateView, SeedDetailView, ExportDetailView, export_file

import os
import shutil


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


class SeedSetDetailViewTests(TestCase):
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
        self.seed = Seed.objects.create(seed_set=self.seedset, token='{}')

    def test_seeds_list_visible(self):
        request = self.factory.get("ui/seedsets/{}".format(self.seedset.id))
        request.user = self.user1
        response = SeedSetDetailView.as_view()(request, pk=self.seedset.id)
        seed_list = response.context_data["seed_list"]
        self.assertEqual(1, len(seed_list))
        self.assertEqual(self.seed, seed_list[0])


class SeedCreateViewTests(TestCase):

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
        self.seed = Seed.objects.create(seed_set=self.seedset,
                                        token="test token",
                                        uid="123",
                                        )
        self.factory = RequestFactory()

    def test_seed_form_seedset_collection(self):
        """
        test that seedset and collection are loaded with seed form view
        """
        request = self.factory.get(reverse("seed_create",
                                           args=[self.seedset.pk]))
        request.user = self.user
        response = SeedCreateView.as_view()(request, seed_set_pk=self.seedset.pk)
        self.assertEqual(self.seedset, response.context_data["form"].initial["seed_set"])
        self.assertEqual(self.seedset, response.context_data["seed_set"])
        self.assertEqual(self.collection, response.context_data["collection"])


class SeedTestsMixin:
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
        self.seed = Seed.objects.create(seed_set=self.seedset,
                                        token="test token",
                                        uid="123",
                                        )
        self.factory = RequestFactory()


class SeedUpdateViewTests(SeedTestsMixin, TestCase):

    def test_seed_update_collection(self):
        """
        test that collection loaded into seed update view
        """
        request = self.factory.get(reverse("seed_update", args=[self.seed.pk]))
        request.user = self.user
        response = SeedUpdateView.as_view()(request, pk=self.seed.pk)
        self.assertEqual(self.collection, response.context_data["collection"])


class SeedDetailViewTests(SeedTestsMixin, TestCase):

    def test_seed_detail_collection(self):
        """
        test that collection loaded into seed detail view
        """
        request = self.factory.get(reverse("seed_detail", args=[self.seed.pk]))
        request.user = self.user
        response = SeedDetailView.as_view()(request, pk=self.seed.pk)
        self.assertEqual(self.collection, response.context_data["collection"])


class ExportDetailViewTests(TestCase):
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
                                              name='Test seedset one')
        self.seed = Seed.objects.create(seed_set=self.seedset,
                                        token="test token",
                                        uid="123")
        self.factory = RequestFactory()

    def _write_test_file(self, export):
        os.makedirs(export.path)
        self.export_file = os.path.join(export.path, "test.csv")
        with open(self.export_file, "w") as f:
            f.write("test")

    def tearDown(self):
        if os.path.exists(settings.SFM_DATA_DIR):
            shutil.rmtree(settings.SFM_DATA_DIR)

    def test_export_detail_seedset(self):
        export = Export.objects.create(user=self.user,
                                       seed_set=self.seedset,
                                       export_type="flickr_user",
                                       export_format="csv",
                                       status=Export.SUCCESS)
        self._write_test_file(export)
        request = self.factory.get(reverse("export_detail", args=[export.pk]))
        request.user = self.user
        response = ExportDetailView.as_view()(request, pk=export.pk)
        self.assertEqual(self.collection, response.context_data["collection"])
        self.assertEqual(self.seedset, response.context_data["seedset"])
        self.assertEqual([("test.csv", 4)], response.context_data["fileinfos"])

    def test_export_detail_seedset_only_if_success(self):
        export = Export.objects.create(user=self.user,
                                       seed_set=self.seedset,
                                       export_type="flickr_user",
                                       export_format="csv",
                                       status=Export.REQUESTED)
        self._write_test_file(export)
        request = self.factory.get(reverse("export_detail", args=[export.pk]))
        request.user = self.user
        response = ExportDetailView.as_view()(request, pk=export.pk)
        self.assertEqual((), response.context_data["fileinfos"])

    def test_export_detail_seed(self):
        export = Export.objects.create(user=self.user,
                                       export_type="flickr_user",
                                       export_format="csv",
                                       status=Export.SUCCESS)
        export.seeds.add(self.seed)
        export.save()
        self._write_test_file(export)
        request = self.factory.get(reverse("export_detail", args=[export.pk]))
        request.user = self.user
        response = ExportDetailView.as_view()(request, pk=export.pk)
        self.assertEqual(self.collection, response.context_data["collection"])
        self.assertEqual(self.seedset, response.context_data["seedset"])
        self.assertEqual([("test.csv", 4)], response.context_data["fileinfos"])


class ExportFileTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@example.com',
                                              'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.superuser = User.objects.create_superuser('testsuperuser', 'testsuperuser@example.com',
                                                       'password')
        self.collection = Collection.objects.create(name='Test Collection One',
                                                    group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform')
        self.seedset = SeedSet.objects.create(collection=self.collection,
                                              credential=self.credential,
                                              harvest_type='test harvest type',
                                              name='Test seedset one',
                                              )
        self.export = Export.objects.create(user=self.user,
                                            seed_set=self.seedset,
                                            export_type="flickr_user",
                                            export_format="csv")
        os.makedirs(self.export.path)
        self.export_file = os.path.join(self.export.path, "test.csv")
        with open(self.export_file, "w") as f:
            f.write("test")
        self.factory = RequestFactory()

    def tearDown(self):
        if os.path.exists(settings.SFM_DATA_DIR):
            shutil.rmtree(settings.SFM_DATA_DIR)

    def test_export_file_by_user(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.user
        response = export_file(request, self.export.pk, "test.csv")
        self.assertEquals(response["content-disposition"], "attachment; filename=test.csv")
        self.assertEquals("test", "".join(response.streaming_content))

    def test_export_file_by_superuser(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.superuser
        response = export_file(request, self.export.pk, "test.csv")
        self.assertEquals(response["content-disposition"], "attachment; filename=test.csv")
        self.assertEquals("test", "".join(response.streaming_content))

    def test_file_not_found(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.user2
        with self.assertRaises(PermissionDenied):
            export_file(request, self.export.pk, "test.csv")
