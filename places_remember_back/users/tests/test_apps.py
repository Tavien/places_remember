from django.test import TestCase

from users.apps import UsersConfig


class UsersAppsTest(TestCase):
    def test_app_name(self):
        self.assertEqual(UsersConfig.name, "users")
