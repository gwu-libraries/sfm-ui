from django.contrib.auth.models import AbstractUser, Group
from django.test import TestCase

from ui.models import Collection, User 

def create_collection(name, is_active, group):
    return Collection.objects.create(name=name, is_active=is_active, group=group)  

def create_group(name):
    return Group.objects.create(name=name)

class CollectionViewTests(TestCase):

    def test_collections_list_anonymous(self):
        '''
        anonymous user should get the login page instead of a 
        collections list. 
        '''
        group = create_group(name='testgroup1') 
        collection = create_collection(name='Test Collection One', is_active=True, group=group)
        response = self.client.get('/ui/collections/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/ui/collections/')

