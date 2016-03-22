from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from ui.models import Collection, User, Credential, Seed, SeedSet


def create_collection(name, group):
    return Collection.objects.create(name=name,
                                     group=group)


def create_group(name):
    return Group.objects.create(name=name)


def create_new_user(name, email, password):
    return User.objects.create_user(name, email, password)


class CollectionListViewTests(TestCase):
    def setUp(self):
        group = create_group(name='testgroup1')
        create_collection(name='Test Collection One',
                          group=group)
        group2 = create_group(name='testgroup2')
        create_collection(name='Test Collection Two',
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
        self.client.login(username='testuser', password='password')
        response = self.client.get('/ui/collections/')
        self.assertContains(response, 'Test Collection One')
        self.assertNotContains(response, 'Test Collection Two')


class CollectionDetailViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = create_new_user('testuser', 'testuser@example.com',
                                    'password')
        self.user.groups.add(self.group)
        self.collection = create_collection(name='Test Collection One',
                                            group=self.group)
        self.credential = Credential.objects.create(user=self.user,
                                                    platform='test platform')
        self.seedset = SeedSet.objects.create(collection=self.collection,
                                              credential=self.credential,
                                              harvest_type='test harvest type',
                                              name='Test seedset one',
                                              )
        Seed.objects.create(seed_set=self.seedset)
        User.objects.create_user('testuser2', 'testuser2@example.com',
                                 'password')
        Credential.objects.create(user=User.objects.get(username='testuser2'),
                                  platform='test platform')
        Group.objects.create(name='testgroup2')
        Collection.objects.create(name='Test Collection Two',
                                  group=Group.objects.get(name='testgroup2'))
        SeedSet.objects.create(collection=Collection.objects.get(
                                          name='Test Collection Two'),
                               credential=Credential.objects.get(
                                          user=User.objects.get(
                                               username='testuser2')),
                               harvest_type='test harvest type',
                               name='Test seedset two')

    def test_collections_detail_anonymous(self):
        '''
        anonymous user should get the login page instead of a
        collections list.
        '''
        response = self.client.get('/ui/collections/1/', follow=True)
        self.assertRedirects(response,
                             '/accounts/login/?next=/ui/collections/1/')

    def test_seedset_visible(self):
        '''
        seedset list should only show seedsets belonging to the collection
        '''
        self.client.login(username='testuser', password='password')
        path = '/ui/collections/' + str(self.collection.pk) + '/'
        response = self.client.get(path)
        self.assertContains(response, 'Test seedset one')
        self.assertNotContains(response, 'Test seedset two')

    def test_number_of_seeds(self):
        '''
        count of seeds in seedset table should be correct
        '''
        self.client.login(username='testuser', password='password')
        path = '/ui/collections/' + str(self.collection.pk) + '/'
        response = self.client.get(path)
        self.assertContains(response, '1 seed')
        self.assertNotContains(response, '0 seeds')

    def test_update_view_works(self):
        '''
        update page should load for a given collection
        '''
        self.client.login(username='testuser', password='password')
        path = '/ui/collections/' + str(self.collection.pk) + '/update/'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)


class SeedSetCreateViewTests(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='testgroup1')
        self.user = create_new_user('testuser', 'testuser@example.com',
                                    'password')
        self.user.groups.add(self.group)
        self.collection = create_collection(name='Test Collection One',
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
        '''
        simple test that seedset form loads with collection
        '''
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('seedset_create',
                                   args=[self.collection.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Seedset')

    def test_seedset_anonymous(self):
        '''
        anonymous user should get the login page instead of a
        seedset create page.
        '''
        response = self.client.get(reverse('seedset_create',
                                           args=[self.collection.pk]))
        path = '/accounts/login/?next=/ui/seedsets/create/' + \
               str(self.collection.pk)
        self.assertRedirects(response, path)
