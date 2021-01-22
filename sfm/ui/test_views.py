from django.contrib.auth.models import Group
from django.urls import reverse
from django.test import RequestFactory, TestCase, Client
from django.conf import settings
from django.core.exceptions import PermissionDenied

from .models import CollectionSet, User, Credential, Seed, Collection, Export
from .views import CollectionSetListView, CollectionSetDetailView, CollectionSetUpdateView, \
    CollectionCreateView, SeedUpdateView, SeedCreateView, SeedDetailView, ExportDetailView, export_file, \
    ChangeLogView, UserProfileDetailView, SeedsJSONAPIView

import os
import shutil


class CollectionSetListViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user('testuser', 'testuser@example.com', 'password')
        credential = Credential.objects.create(user=self.user, platform="test_platform",
                                               token="{'key': '1'}")
        group = Group.objects.create(name='testgroup1')
        self.user.groups.add(group)
        self.user.save()
        self.collection_set1 = CollectionSet.objects.create(name='Test Collection Set One',
                                                            group=group)

        Collection.objects.create(collection_set=self.collection_set1, harvest_type="twitter_search",
                                  name="Test Collection One",
                                  credential=credential)
        group2 = Group.objects.create(name='testgroup2')
        CollectionSet.objects.create(name='Test Collection Set Two',
                                     group=group2)

    def test_correct_collection_set_list_for_usergroup(self):
        """
        logged in user should see collection_sets in belonging to the same group
        as the user and not see collection_sets from other groups
        """
        request = self.factory.get('/ui/collection_sets/')
        request.user = self.user
        response = CollectionSetListView.as_view()(request)
        # get active collection set('acs', "Active Collection Sets", active_collection_sets)
        collection_set_list = response.context_data["collection_sets_lists"][0][2]
        self.assertEqual(1, len(collection_set_list))
        self.assertEqual(self.collection_set1, collection_set_list[0])
        self.assertEqual(1, collection_set_list[0].num_collections)


class CollectionSetTestsMixin:
    def setUp(self):
        self.factory = RequestFactory()
        self.group1 = Group.objects.create(name='testgroup1')
        self.user1 = User.objects.create_user('testuser', 'testuser@example.com',
                                              'password')
        self.user1.groups.add(self.group1)
        self.user1.save()
        self.collection_set1 = CollectionSet.objects.create(name='Test Collection Set One',
                                                            group=self.group1)
        self.credential1 = Credential.objects.create(user=self.user1,
                                                     platform='test platform',
                                                     token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set1,
                                                    credential=self.credential1,
                                                    harvest_type='test harvest type',
                                                    name='Test collection one',
                                                    )
        Seed.objects.create(collection=self.collection)
        self.changed_collection_set1_name = "changed collection_set name"
        self.collection_set1.name = self.changed_collection_set1_name
        self.collection_set1.save()
        self.historical_collection_set = self.collection_set1.history.all()
        self.assertEqual(2, len(self.historical_collection_set))
        user2 = User.objects.create_user('testuser2', 'testuser2@example.com',
                                         'password')
        credential2 = Credential.objects.create(user=user2,
                                                platform='test platform',
                                                token="{'key': '2'}")
        group2 = Group.objects.create(name='testgroup2')
        collection_set2 = CollectionSet.objects.create(name='Test Collection Set Two',
                                                       group=group2)
        Collection.objects.create(collection_set=collection_set2,
                                  credential=credential2,
                                  harvest_type='test harvest type',
                                  name='Test collection two')


class CollectionSetDetailViewTests(CollectionSetTestsMixin, TestCase):
    def test_collection_visible(self):
        """
        collection list should only show collections belonging to the collection_set
        """
        request = self.factory.get('/ui/collection_sets/{}/'.format(self.collection_set1.pk))
        request.user = self.user1
        response = CollectionSetDetailView.as_view()(request, pk=self.collection_set1.pk)
        collection_list = response.context_data["collection_list"]
        self.assertEqual(1, len(collection_list))
        self.assertEqual(self.collection, collection_list[0])

    def test_change_log_model_name_id(self):
        """
        change log 'view all' should contain correct model name and id
        """
        request = self.factory.get('/ui/collection_sets/{}/'.format(self.collection_set1.pk))
        request.user = self.user1
        response = CollectionSetDetailView.as_view()(request, pk=self.collection_set1.pk)
        model_name = response.context_data["model_name"]
        item_id = response.context_data["item_id"]
        self.assertEqual("collection_set", model_name)
        self.assertEqual(self.collection_set1.pk, item_id)


class CollectionSetUpdateViewTests(CollectionSetTestsMixin, TestCase):
    def test_collection_visible(self):
        """
        collection list should only show collections belonging to the collection_set
        """
        request = self.factory.put('/ui/collection_sets/{}/'.format(self.collection_set1.pk))
        request.user = self.user1
        response = CollectionSetUpdateView.as_view()(request, pk=self.collection_set1.pk)
        collection_list = response.context_data["collection_list"]
        self.assertEqual(1, len(collection_list))
        self.assertEqual(self.collection, collection_list[0])
        self.assertEqual(1, collection_list[0].num_seeds)


class CollectionCreateViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform=Credential.TWITTER,
                                                    token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type=Collection.TWITTER_FILTER,
                                                    name='Test collection one',
                                                    )
        self.factory = RequestFactory()

    def test_collection_form_view(self):
        """
        simple test that collection form loads with collection_set
        """
        request = self.factory.get(reverse('collection_create',
                                           args=[self.collection_set.pk, Collection.TWITTER_FILTER]))
        request.user = self.user
        response = CollectionCreateView.as_view()(request, collection_set_pk=self.collection_set.pk,
                                                  harvest_type=Collection.TWITTER_FILTER)
        self.assertEqual(self.collection_set, response.context_data["form"].initial["collection_set"])
        self.assertEqual(self.collection_set, response.context_data["collection_set"])

    def test_credential_warning(self):
        """
        test that credential list for platform is empty
        """
        request = self.factory.get(reverse('collection_create',
                                           args=[self.collection_set.pk, Collection.WEIBO_TIMELINE]))
        request.user = self.user
        response = CollectionCreateView.as_view()(request, collection_set_pk=self.collection_set.pk,
                                                  harvest_type=Collection.WEIBO_TIMELINE)
        self.assertEqual(0, len(response.context_data["credentials"]))


class CollectionDetailViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.group1 = Group.objects.create(name='testgroup1')
        self.user1 = User.objects.create_user('testuser', 'testuser@example.com',
                                              'password')
        self.user1.groups.add(self.group1)
        self.user1.save()
        self.collection_set1 = CollectionSet.objects.create(name='Test Collection Set One',
                                                            group=self.group1)
        self.credential1 = Credential.objects.create(user=self.user1,
                                                     platform='test platform',
                                                     token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set1,
                                                    credential=self.credential1,
                                                    harvest_type=Collection.TWITTER_SEARCH,
                                                    name='Test collection one',
                                                    )
        self.seed = Seed.objects.create(collection=self.collection, token='{}')

    def test_seeds_list_visible(self):
        request = self.factory.get(reverse("seedsJSONAPI", args=[self.collection.id, 'active']),
                                   content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        request.user = self.user1
        response = SeedsJSONAPIView.as_view()(request, pk=self.collection.id, status='active')
        self.assertEqual(200, response.status_code)


class SeedCreateViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform',
                                                    token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                    name='Test collection one',
                                                    )
        self.seed = Seed.objects.create(collection=self.collection,
                                        token="test token",
                                        uid="123",
                                        )
        self.factory = RequestFactory()

    def test_seed_form_collection_collection_set(self):
        """
        test that collection and collection_set are loaded with seed form view
        """
        request = self.factory.get(reverse("seed_create",
                                           args=[self.collection.pk]))
        request.user = self.user
        response = SeedCreateView.as_view()(request, collection_pk=self.collection.pk)
        self.assertEqual(self.collection, response.context_data["form"].initial["collection"])
        self.assertEqual(self.collection, response.context_data["collection"])
        self.assertEqual(self.collection_set, response.context_data["collection_set"])


class SeedTestsMixin:
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform',
                                                    token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type=Collection.TWITTER_USER_TIMELINE,
                                                    name='Test collection one',
                                                    )
        self.seed = Seed.objects.create(collection=self.collection,
                                        token="test",
                                        uid="123",
                                        )
        self.factory = RequestFactory()


class SeedUpdateViewTests(SeedTestsMixin, TestCase):
    def test_seed_update_collection_set(self):
        """
        test that collection_set loaded into seed update view
        """
        request = self.factory.get(reverse("seed_update", args=[self.seed.pk]))
        request.user = self.user
        response = SeedUpdateView.as_view()(request, pk=self.seed.pk)
        self.assertEqual(self.collection_set, response.context_data["collection_set"])


class SeedDetailViewTests(SeedTestsMixin, TestCase):
    def test_seed_detail_collection_set(self):
        """
        test that collection_set loaded into seed detail view
        """
        request = self.factory.get(reverse("seed_detail", args=[self.seed.pk]))
        request.user = self.user
        response = SeedDetailView.as_view()(request, pk=self.seed.pk)
        self.assertEqual(self.collection_set, response.context_data["collection_set"])


class SeedBulkCreateViewTests(SeedTestsMixin, TestCase):
    def setUp(self):
        SeedTestsMixin.setUp(self)
        self.client = Client()
        self.assertTrue(self.client.login(username=self.user.username, password='password'))

    def test_get(self):
        response = self.client.get(reverse("bulk_seed_create", args=[self.collection.pk]))
        self.assertTrue(response.context["form"])
        self.assertEqual(self.collection, response.context["collection"])
        self.assertEqual(self.collection_set, response.context["collection_set"])
        self.assertEqual("Twitter user timeline", response.context["harvest_type_name"])

    def test_post(self):
        response = self.client.post(reverse("bulk_seed_create", args=[self.collection.pk]),
                                    {'seeds_type': 'token', 'tokens': """
        test

        test2
          @test3
        null
        """})
        self.assertEqual(3, Seed.objects.filter(collection=self.collection).count())
        self.assertTrue(Seed.objects.filter(collection=self.collection, token='test3').exists())
        self.assertTrue(response.url.endswith('/ui/collections/1/'))

    def test_post_uid(self):
        response = self.client.post(reverse("bulk_seed_create", args=[self.collection.pk]),
                                    {'seeds_type': 'uid', 'tokens': """
        123

        45367
          9087
        """})
        self.assertEqual(3, Seed.objects.filter(collection=self.collection).count())
        self.assertSetEqual({'123', '45367', '9087'}, {s.uid for s in Seed.objects.filter(collection=self.collection)})
        self.assertTrue(response.url.endswith('/ui/collections/1/'))


class ExportDetailViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform',
                                                    token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type='test harvest type',
                                                    name='Test collection one')
        self.seed = Seed.objects.create(collection=self.collection,
                                        token="test token",
                                        uid="123")
        self.factory = RequestFactory()

    def _write_test_file(self, export):
        os.makedirs(export.path)
        self.export_file = os.path.join(export.path, "test.csv")
        with open(self.export_file, "w") as f:
            f.write("test")

    def tearDown(self):
        if os.path.exists(settings.SFM_COLLECTION_SET_DATA_DIR):
            shutil.rmtree(settings.SFM_COLLECTION_SET_DATA_DIR)

    def test_export_detail_collection(self):
        export = Export.objects.create(user=self.user,
                                       collection=self.collection,
                                       export_type="flickr_user",
                                       export_format="csv",
                                       status=Export.SUCCESS)
        self._write_test_file(export)
        request = self.factory.get(reverse("export_detail", args=[export.pk]))
        request.user = self.user
        response = ExportDetailView.as_view()(request, pk=export.pk)
        self.assertEqual(self.collection_set, response.context_data["collection_set"])
        self.assertEqual(self.collection, response.context_data["collection"])
        self.assertEqual([("test.csv", 4)], response.context_data["fileinfos"])

    def test_export_detail_collection_only_if_success(self):
        export = Export.objects.create(user=self.user,
                                       collection=self.collection,
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
        self.assertEqual(self.collection_set, response.context_data["collection_set"])
        self.assertEqual(self.collection, response.context_data["collection"])
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
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform',
                                                    token="{'key': '1'}")
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type='test harvest type',
                                                    name='Test collection one',
                                                    )
        self.export = Export.objects.create(user=self.user,
                                            collection=self.collection,
                                            export_type="flickr_user",
                                            export_format="csv")
        os.makedirs(self.export.path)
        self.export_file = os.path.join(self.export.path, "test.csv")
        with open(self.export_file, "w") as f:
            f.write("test")
        self.factory = RequestFactory()

    def tearDown(self):
        if os.path.exists(settings.SFM_COLLECTION_SET_DATA_DIR):
            shutil.rmtree(settings.SFM_COLLECTION_SET_DATA_DIR)

    def test_export_file_by_user(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.user
        response = export_file(request, self.export.pk, "test.csv")
        self.assertEquals(response["content-disposition"], "attachment; filename=test.csv")
        self.assertEquals("test", self._streaming_content(response))

    def test_export_file_by_superuser(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.superuser
        response = export_file(request, self.export.pk, "test.csv")
        self.assertEquals(response["content-disposition"], "attachment; filename=test.csv")
        self.assertEquals("test", self._streaming_content(response))

    def test_file_not_found(self):
        request = self.factory.get(reverse("export_file", args=[self.export.pk, "test.csv"]))
        request.user = self.user2
        with self.assertRaises(PermissionDenied):
            export_file(request, self.export.pk, "test.csv")

    @staticmethod
    def _streaming_content(response):
        return "".join((c.decode('utf-8') for c in response.streaming_content))


class ChangeLogTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.collection_set = CollectionSet.objects.create(name='Test Collection Set One',
                                                           group=self.group)
        self.changed_collection_set_name = "changed collection_set name"
        self.collection_set.name = self.changed_collection_set_name
        self.collection_set.save()
        self.historical_collection_set = self.collection_set.history.all()
        self.assertEqual(2, len(self.historical_collection_set))

    def test_context_data(self):
        """
        test that model name correctly pulled from url
        """
        request = self.factory.get(reverse("change_log", args=("collection_set", self.collection_set.id)))
        request.user = self.user
        response = ChangeLogView.as_view()(request, model="CollectionSet", item_id=self.collection_set.id)
        self.assertEqual(self.collection_set, response.context_data["item"])
        self.assertEqual(2, response.context_data["paginator"].count)
        self.assertEqual("CollectionSet", response.context_data["model_name"])
        self.assertEqual("changed collection_set name", response.context_data["name"])


class UserProfileTestsUnit:
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = User.objects.create_user('testuser', 'testuser@example.com',
                                             'password')
        self.user.groups.add(self.group)
        self.user.save()
        self.superuser = User.objects.create_superuser('testsuperuser', 'testsuperuser@example.com',
                                                       'password')
        self.factory = RequestFactory()


class UserProfileDetailViewTests(UserProfileTestsUnit, TestCase):
    def test_seed_detail_collection_set(self):
        """
        test that collection_set loaded into seed detail view
        """
        request = self.factory.get(reverse("user_profile_detail"))
        request.user = self.user
        response = UserProfileDetailView.as_view()(request)
        self.assertEqual('mailto:' + self.superuser.email, response.context_data["email_info"])
