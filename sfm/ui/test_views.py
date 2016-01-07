from django.contrib.auth.models import Group
from django.test import TestCase

from ui.models import Collection, User


def create_collection(name, is_active, group):
    return Collection.objects.create(name=name, is_active=is_active,
                                     group=group)


def create_group(name):
    return Group.objects.create(name=name)


def create_new_user(name, email, password):
    return User.objects.create_user(name, email, password)


class CollectionViewTests(TestCase):
    def setUp(self):
        group = create_group(name='testgroup1')
        create_collection(name='Test Collection One', is_active=True,
                          group=group)
        group2 = create_group(name='testgroup2')
        create_collection(name='Test Collection Two', is_active=False,
                          group=group2)
        user = create_new_user('testuser', 'testuser@example.com', 'password')
        user.groups.add(group)

    def test_collections_list_anonymous(self):
        '''
        anonymous user should get the login page instead of a
        collections list.
        '''
        response = self.client.get('/ui/collections/', follow=True)
        self.assertRedirects(response,
                             '/accounts/login/?next=/ui/collections/')

    def test_correct_collection_list_for_usergroup(self):
        '''
        logged in user should see collections in belonging to the same group
        as the user and not see collections from other groups
        '''
        response = self.client.login(username='testuser', password='password')
        response = self.client.get('/ui/collections/')
        self.assertContains(response, 'Test Collection One')
        self.assertNotContains(response, 'Test Collection Two')
