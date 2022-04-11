from django.contrib.gis.geos import Point
from django.test import TestCase

from remembers.models import RemembersModel
from users.models import User


class UsersModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.point = Point(7.15, 35.0)
        self.remember_1 = RemembersModel.objects.create(name='name_1',
                                                        description="description_1",
                                                        location_point=self.point,
                                                        user=self.user)

    def test_name(self):
        self.assertEqual(self.remember_1.name, 'name_1')

    def test_point(self):
        self.assertEqual(self.remember_1.location_point, self.point)

    def test_user(self):
        self.assertEqual(self.remember_1.user, self.user)
