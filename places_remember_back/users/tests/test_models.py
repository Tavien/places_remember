from django.test import TestCase

from users.models import User


class UsersModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_1", password="pass")

    def test_str_method(self):
        self.assertIsInstance(self.user.username, str)

    def test_photo_blank(self):
        self.assertEqual(self.user.photo, "")
