from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory
from django.utils import timezone

from .forms import CollectionForm, SeedSetForm
from .views import CollectionCreateView, CollectionUpdateView
from .models import User, Collection, SeedSet, Credential


def create_group(name):
    return Group.objects.create(name=name)


class CollectionFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                                             email='testuser@example.com',
                                             password='password')
        group = create_group(name='testgroup1')
        self.user.groups.add(group)
        create_group(name='testgroup2')

    def test_form_has_correct_groups(self):
        request = self.factory.get('/ui/collections/create/')
        request.user = self.user
        response = CollectionCreateView.as_view()(request)
        self.assertContains(response, 'testgroup')
        self.assertNotContains(response, 'testgroup2')

    def test_valid_data(self):
        request = self.factory.get('/ui/collections/create')
        request.user = self.user
        groupno = Group.objects.filter(name='testgroup1')
        form = CollectionForm({
            'name': 'my test collection',
            'description': 'my description',
            'group': groupno
        }, request=request)
        self.assertTrue(form.is_valid())

    def test_invalid_data_blank_name(self):
        request = self.factory.get('/ui/collections/create')
        request.user = self.user
        groupno = Group.objects.filter(name='testgroup1')
        form = CollectionForm({
            'name': '',
            'description': 'my description',
            'group': groupno
        }, request=request)
        self.assertFalse(form.is_valid())

    def test_invalid_data_blank_group(self):
        request = self.factory.get('/ui/collections/create')
        request.user = self.user
        form = CollectionForm({
            'name': 'my test collection',
            'description': 'my description',
            'group': ''
        }, request=request)
        self.assertFalse(form.is_valid())


class CollectionUpdateFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                                             email='testuser@example.com',
                                             password='password')
        group = create_group(name='testgroup1')
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
