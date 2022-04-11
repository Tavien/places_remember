from django.test import TestCase

from remembers.apps import RemembersConfig


class UsersAppsTest(TestCase):
    def test_app_name(self):
        self.assertEqual(RemembersConfig.name, "remembers")
