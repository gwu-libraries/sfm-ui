from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory

from .forms import CollectionForm
from .views import CollectionCreateView
from .models import User


def create_group(name):
    return Group.objects.create(name=name)


class CollectionFormTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser',
                        email='testuser@example.com', password='password')
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
