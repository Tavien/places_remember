import json
from collections import OrderedDict

from users.models import User
from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework_gis.fields import GeoJsonDict

from remembers.models import RemembersModel
from remembers.serializers import RemembersSerializer


class RemembersSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.remember_1 = RemembersModel.objects.create(name='name_1',
                                                        description="description_1",
                                                        location_point=Point(7.15, 35.0),
                                                        user=self.user)
        self.remember_2 = RemembersModel.objects.create(name='name_2',
                                                        description="description_2",
                                                        location_point=Point(12.05, 1.10),
                                                        user=self.user)
        self.excepted_data = OrderedDict([('type', 'FeatureCollection'), ('features', [
            OrderedDict(
                [('id', self.remember_1.id), ('type', 'Feature'),
                 ('geometry', GeoJsonDict([('type', 'Point'), ('coordinates', [7.15, 35.0])])),
                 ('bbox', (7.15, 35.0, 7.15, 35.0)),
                 ('properties',
                  OrderedDict([('name', 'name_1'), ('description', 'description_1'), ('user', self.user.id)]))]),
            OrderedDict(
                [('id', self.remember_2.id), ('type', 'Feature'),
                 ('geometry', GeoJsonDict([('type', 'Point'), ('coordinates', [12.05, 1.10])])),
                 ('bbox', (12.05, 1.10, 12.05, 1.10)),
                 ('properties',
                  OrderedDict([('name', 'name_2'), ('description', 'description_2'), ('user', self.user.id)]))])])])

    def test_serializer_ok(self):
        """
        Basic serializer testing
        """
        data = RemembersSerializer([self.remember_1, self.remember_2], many=True).data

        self.assertEqual(self.excepted_data, data)
