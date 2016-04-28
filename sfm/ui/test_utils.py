from django.test import TestCase
from .models import Collection, Credential, Group, User, SeedSet
from .utils import diff_historical_object, diff_object_history, diff_field_changed


class DiffTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username="test_user", email="test_user@test.com",
                                                  password="test_password")
        self.group = Group.objects.create(name="test_group")
        self.collection = Collection.objects.create(group=self.group, name="test_collection")
        self.original_credential_token = "original token"
        self.credential = Credential.objects.create(name="test_credential",
                                                    user=self.user, platform="test_platform",
                                                    token=self.original_credential_token)
        self.changed_credential_token = "changed token"
        self.credential.token = self.changed_credential_token
        self.history_note = "Change note"
        self.credential.history_note = self.history_note
        self.credential.save()
        self.historical_credentials = self.credential.history.all()
        self.assertEqual(2, len(self.historical_credentials))

    def test_diff_historical_object(self):
        historical_credential = self.historical_credentials[0]
        historical_credential.history_user = self.user

        diff = diff_historical_object(self.historical_credentials[1], historical_credential)
        self.assertDictEqual({"token": (self.original_credential_token, self.changed_credential_token)}, diff.fields)
        self.assertEqual(self.user, diff.user)
        self.assertEqual(historical_credential.history_date, diff.date)
        self.assertEqual(self.history_note, diff.note)

    def test_diff_first_historical_object(self):
        historical_credential = self.historical_credentials[1]
        historical_credential.history_user = self.user

        diff = diff_historical_object(None, historical_credential)
        self.assertDictEqual(
            {"name": (None, "test_credential"), "platform": (None, "test_platform"), "token": (None, "original token"),
             "is_active": (None, True)},
            diff.fields)
        self.assertEqual(self.user, diff.user)
        self.assertEqual(historical_credential.history_date, diff.date)

    def test_diff_object(self):
        diffs = diff_object_history(self.credential)
        self.assertEqual(2, len(diffs))
        self.assertDictEqual({"token": (self.original_credential_token, self.changed_credential_token)},
                             diffs[0].fields)
        self.assertDictEqual(
            {"name": (None, "test_credential"), "platform": (None, "test_platform"), "token": (None, "original token"),
             "is_active": (None, True)},
            diffs[1].fields)

    def test_diff_field_changed(self):
        seedset = SeedSet.objects.create(collection=self.collection, credential=self.credential,
                                         harvest_type="test_type", name="test_seedset", is_active=True,
                                         schedule_minutes=60)
        self.assertTrue(diff_field_changed(seedset))
        seedset.harvest_type = "foo"
        seedset.save()
        self.assertTrue(diff_field_changed(seedset))
        seedset.stats = {"foo": 5}
        seedset.save()
        self.assertFalse(diff_field_changed(seedset))
