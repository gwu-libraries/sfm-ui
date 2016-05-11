from datetime import datetime
import pytz

from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory

from .forms import CollectionForm, ExportForm, CredentialWeiboForm, CredentialFlickrForm, CredentialTwitterForm, \
    SeedSetTwitterSearchForm, SeedTwitterUserTimelineForm
from .views import CollectionUpdateView
from .models import User, Collection, Credential, SeedSet, Seed


class CollectionFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/")
        self.user = User.objects.create_user(username='testuser',
                                             email='testuser@example.com',
                                             password='password')
        self.request.user = self.user
        self.group = Group.objects.create(name='testgroup1')
        self.user.groups.add(self.group)
        Group.objects.create(name='testgroup2')

    def test_form_has_correct_groups(self):
        form = CollectionForm(request=self.request)
        self.assertEqual([self.group, ], list(form.fields['group'].queryset))

    def test_valid_data(self):
        groupno = Group.objects.filter(name='testgroup1')
        form = CollectionForm({
            'name': 'my test collection',
            'description': 'my description',
            'group': groupno
        }, request=self.request)
        self.assertTrue(form.is_valid())

    def test_invalid_data_blank_group(self):
        form = CollectionForm({
            'name': 'my test collection',
            'description': 'my description',
            'group': ''
        }, request=self.request)
        self.assertFalse(form.is_valid())


class CollectionUpdateFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                                             email='testuser@example.com',
                                             password='password')
        group = Group.objects.create(name='testgroup1')
        self.user.groups.add(group)
        self.collection = Collection.objects.create(name='Test Collection One',
                                                    group=group)
        self.path = '/ui/collections/' + str(self.collection.pk) + '/update/'

    def test_valid_data(self):
        request = self.factory.get(self.path)
        request.user = self.user
        groupno = Group.objects.filter(name='testgroup1')
        response = CollectionUpdateView.as_view()(request,
                                                  pk=self.collection.pk)
        form = CollectionForm({
            'name': 'my test collection updated name',
            'description': 'my updated description',
            'group': groupno
        }, request=request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())

    def test_group_choices_correct(self):
        request = self.factory.get(self.path)
        request.user = self.user
        response = CollectionUpdateView.as_view()(request,
                                                  pk=self.collection.pk)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'testgroup2')

    def test_invalid_data_blank_name(self):
        request = self.factory.get(self.path)
        request.user = self.user
        groupno = Group.objects.filter(name='testgroup1')
        response = CollectionUpdateView.as_view()(request,
                                                  pk=self.collection.pk)
        form = CollectionForm({
            'name': '',
            'description': 'my description',
            'group': groupno
        }, request=request)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())


class SeedSetFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=group, name="test_collection")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")
        self.data = {
            'collection': self.collection.pk,
            'credential': self.credential.pk,
            'harvest_type': 'twitter_search',
            'name': 'my test seedset',
            'end_date': '01/01/2200',
            'date_added': '03/16/2016',
            'schedule_minutes': '60'
        }

    def test_valid_form(self):
        form = SeedSetTwitterSearchForm(self.data, coll=self.collection.pk)
        self.assertTrue(form.is_valid())

    def test_end_date_after_now(self):
        self.data['end_date'] = "01/01/2000"
        form = SeedSetTwitterSearchForm(self.data, coll=self.collection.pk)
        self.assertFalse(form.is_valid())


class SeedFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                             password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=group, name="test_collection")
        self.credential = Credential.objects.create(user=user, platform="test_platform",
                                                    token="{}")
        self.seedset = SeedSet.objects.create(collection=self.collection,
                                              name="test_seedset",
                                              harvest_type="twitter_search",
                                              credential=self.credential,
                                              end_date=datetime(2200, 1, 1, 1, 30, tzinfo=pytz.utc),
                                              date_added=datetime(2016, 1, 1, 1, 30, tzinfo=pytz.utc),
                                              schedule_minutes=60,
                                              )
        self.data = {
            "token": "test_token",
            "uid": "test_uid",
            "seed_set": self.seedset.pk,
            "date_added": "01/01/2016",
        }

    def test_valid_from(self):
        form = SeedTwitterUserTimelineForm(self.data, seedset=self.seedset.pk)
        self.assertTrue(form.is_valid())


class CredentialFlickrFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.path = "/ui/credentials/flickr/create/"
        self.user = User.objects.create_superuser(username="test_user",
                                                  email="test_user@test.com",
                                                  password="test_password")
        self.data = {
            "name": "test_flickr_credential",
            "user": self.user.pk,
            "platform": "flickr",
            "key": "dummy_key",
            "secret": "dummy_secret",
            "date_added": "04/14/2016",
        }

    def test_form(self):
        form = CredentialFlickrForm(self.data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        credential = form.save()
        self.assertJSONEqual(credential.token, '{"key":"dummy_key","secret":"dummy_secret"}')


class CredentialTwitterFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.path = "/ui/credentials/flickr/create/"
        self.user = User.objects.create_superuser(username="test_user",
                                                  email="test_user@test.com",
                                                  password="test_password")
        self.data = {
            "name": "test_twitter_credential",
            "user": self.user.pk,
            "platform": "twitter",
            "consumer_key": "dummy_consumer_key",
            "consumer_secret": "dummy_consumer_secret",
            "access_token": "dummy_access_token",
            "access_token_secret": "dummy_access_token_secret",
            "date_added": "04/14/2016",
        }

    def test_form(self):
        form = CredentialTwitterForm(self.data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        credential = form.save()
        self.assertJSONEqual(credential.token, '{"consumer_key": "dummy_consumer_key",'
                                               '"consumer_secret": "dummy_consumer_secret",'
                                               '"access_token": "dummy_access_token",'
                                               '"access_token_secret": "dummy_access_token_secret"}')


class CredentialWeiboFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.path = "/ui/credentials/flickr/create/"
        self.user = User.objects.create_superuser(username="test_user",
                                                  email="test_user@test.com",
                                                  password="test_password")
        self.data = {
            "name": "test_weibo_credential",
            "user": self.user.pk,
            "platform": "weibo",
            "api_key": "dummy_api_key",
            "api_secret": "dummy_api_secret",
            "redirect_uri": "dummy_redirect_uri",
            "access_token": "dummy_access_token",
            "date_added": "04/14/2016",
        }

    def test_form(self):
        form = CredentialWeiboForm(self.data)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        credential = form.save()
        self.assertJSONEqual(credential.token,
                             '{"api_key": "dummy_api_key",'
                             '"api_secret": "dummy_api_secret",'
                             '"redirect_uri": "dummy_redirect_uri",'
                             '"access_token": "dummy_access_token"}')


class TestExportForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=group, name="test_collection")
        self.credential = Credential.objects.create(user=self.user, platform="test_platform",
                                                    token="{}")
        self.seedset = SeedSet.objects.create(collection=self.collection,
                                              name="test_seedset",
                                              harvest_type="twitter_search",
                                              credential=self.credential)
        self.seed = Seed.objects.create(token="test",
                                        seed_set=self.seedset)
        self.data = {
            "export_format": "csv"
        }

    def test_valid_seedset_form(self):
        form = ExportForm(self.data, seedset=self.seedset.pk)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        export = form.save()
        self.assertEquals(0, len(export.seeds.all()))
        self.assertEqual(self.seedset, export.seed_set)
        self.assertEqual("twitter_search", export.export_type)

    def test_valid_seeds_form(self):
        data = dict(self.data)
        data["seeds"] = (self.seed.pk,)
        form = ExportForm(data, seedset=self.seedset.pk)
        form.instance.user = self.user
        self.assertTrue(form.is_valid())
        export = form.save()
        self.assertEquals(1, len(export.seeds.all()))
        self.assertIsNone(export.seed_set)
        self.assertEqual("twitter_search", export.export_type)
