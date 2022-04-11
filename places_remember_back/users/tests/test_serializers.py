from django.test import TestCase

from users.models import User
from users.serializers import UserSerializer


class UsersSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="username",
            password="password",
            first_name="first_name",
            last_name="last_name",
            photo="photo1",
        )

    def test_valid_serializer(self):
        data = UserSerializer(self.user).data

        self.assertEqual(data.get("username"), "username")
        self.assertEqual(data.get("first_name"), "first_name")
        self.assertEqual(data.get("last_name"), "last_name")
        self.assertEqual(data.get("photo"), "photo1")
