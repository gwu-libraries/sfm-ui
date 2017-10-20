from django.test import TestCase
import json
from .models import CollectionSet, Credential, Group, User, Collection
from .auth import has_collection_set_based_permission, has_user_based_permission


class AuthTests(TestCase):
    def setUp(self):
        self.group1 = Group.objects.create(name="test_group1")
        self.group2 = Group.objects.create(name="test_group2")
        self.user1 = User.objects.create_user(username="test_user1", email="test_user1@test.com",
                                              password="test_password")
        self.user1.groups.add(self.group1)
        self.user1.save()
        self.user2 = User.objects.create_user(username="test_user2", email="test_user2@test.com",
                                              password="test_password")
        self.staff = User.objects.create_user(username="staff", email="staff@test.com",
                                              password="test_password")
        self.staff.is_staff = True
        self.staff.save()
        self.superuser = User.objects.create_superuser(username="superuser", email="superuser@test.com",
                                                       password="test_password")

        self.collection_set = CollectionSet.objects.create(group=self.group1, name="test_collection_set")
        self.credential = Credential.objects.create(user=self.user1, platform="test_platform",
                                                    token=json.dumps({"key": "test_key"}))
        self.collection = Collection.objects.create(collection_set=self.collection_set,
                                                    credential=self.credential,
                                                    harvest_type='test harvest type',
                                                    name='Test collection two',
                                                    visibility=Collection.LOCAL_VISIBILITY)

    def test_has_collection_set_based_permission_superuser(self):
        self.assertTrue(has_collection_set_based_permission(self.collection_set, self.superuser))
        self.assertFalse(
            has_collection_set_based_permission(self.collection_set, self.superuser, allow_superuser=False))

    def test_has_collection_set_based_permission_staff(self):
        self.assertTrue(has_collection_set_based_permission(self.collection_set, self.staff, allow_staff=True))
        self.assertFalse(has_collection_set_based_permission(self.collection_set, self.staff))

    def test_has_collection_set_based_permission_user(self):
        self.assertTrue(has_collection_set_based_permission(self.collection_set, self.user1))
        self.assertFalse(has_collection_set_based_permission(self.collection_set, self.user2))

    def test_has_collection_set_based_permission_visibility(self):
        self.assertTrue(
            has_collection_set_based_permission(self.collection_set, self.user1, allow_collection_visibility=True))
        self.assertTrue(
            has_collection_set_based_permission(self.collection_set, self.user2, allow_collection_visibility=True))

    def test_has_user_based_permission_superuser(self):
        self.assertTrue(has_user_based_permission(self.credential, self.superuser))
        self.assertFalse(has_user_based_permission(self.credential, self.superuser, allow_superuser=False))

    def test_has_user_based_permission_staff(self):
        self.assertTrue(has_user_based_permission(self.credential, self.staff, allow_staff=True))
        self.assertFalse(has_user_based_permission(self.credential, self.staff))

    def test_has_user_based_permission_user(self):
        self.assertTrue(has_user_based_permission(self.credential, self.user1))
        self.assertFalse(has_user_based_permission(self.credential, self.user2))
