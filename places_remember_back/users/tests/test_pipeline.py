from django.test import TestCase

from users.models import User


class UsersPipelineTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_1", password="pass", photo="photo1")

    def test_get_photo_pipeline(self):
        self.assertEqual(self.user.photo, "photo1")
