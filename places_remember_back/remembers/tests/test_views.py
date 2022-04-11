import json
from collections import OrderedDict

from users.models import User
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from remembers.models import RemembersModel
from remembers.serializers import RemembersSerializer


class RemembersApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user_2 = User.objects.create(username='test_username_2')
        self.user_3 = User.objects.create(username='test_username_3',
                                          is_staff=True)
        self.user_4 = User.objects.create(username='test_username_4')

        self.remember_1 = RemembersModel.objects.create(name='name_1',
                                                        description="description_1",
                                                        location_point=Point(7.15, 35.0),
                                                        user=self.user)
        self.remember_2 = RemembersModel.objects.create(name='name_2',
                                                        description="description_2",
                                                        location_point=Point(12.05, 1.10),
                                                        user=self.user)
        self.remember_3 = RemembersModel.objects.create(name='name_3',
                                                        description="description_2",
                                                        location_point=Point(2.15, 1.00),
                                                        user=self.user)
        self.remember_4 = RemembersModel.objects.create(name='name_5',
                                                        description="description_5",
                                                        location_point=Point(50.15, 3.00),
                                                        user=self.user_2)

    def test_get_list(self):
        self.client.force_login(self.user)

        url = reverse('remembers:remember-list')

        response = self.client.get(url)
        serializer_data = RemembersSerializer([self.remember_1, self.remember_2,
                                               self.remember_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_list_without_auth(self):
        url = reverse('remembers:remember-list')
        response = self.client.get(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                   code='not_authenticated')}, response.data)

    def test_get_empty_list(self):
        self.client.force_login(self.user_4)
        url = reverse('remembers:remember-list')
        response = self.client.get(url)
        excepted_data = OrderedDict([('type', 'FeatureCollection'), ('features', [])])

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(excepted_data, response.data)

    def test_get_search(self):
        self.client.force_login(self.user)

        url = reverse('remembers:remember-list')
        response = self.client.get(url, data={'search': 'description_2'})
        serializer_data = RemembersSerializer([self.remember_2, self.remember_3],
                                              many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordered(self):
        self.client.force_login(self.user)

        url = reverse('remembers:remember-list')
        response = self.client.get(url, data={'ordering': '-name'})
        serializer_data = RemembersSerializer([self.remember_3, self.remember_2,
                                               self.remember_1], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        pass

    def test_get_elem(self):
        self.client.force_login(self.user)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.get(url)
        serializer_data = RemembersSerializer(self.remember_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_elem_not_owner(self):
        self.client.force_login(self.user_2)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='Not found.', code='not_found')}, response.data)

    def test_get_elem_not_owner_but_admin(self):
        self.client.force_login(self.user_3)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.get(url)
        serializer_data = RemembersSerializer(self.remember_1).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.client.force_login(self.user)

        self.assertEqual(4, RemembersModel.objects.all().count())
        url = reverse('remembers:remember-list')
        data = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    12.02,
                    20.21
                ]
            },
            "properties": {
                "name": "test",
                "description": "desc",
                "user": self.user.id
            }
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, RemembersModel.objects.all().count())
        self.assertEqual(self.user, RemembersModel.objects.last().user)

    def test_update(self):
        self.client.force_login(self.user)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        data = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    12.02,
                    20.21
                ]
            },
            "properties": {
                "name": "test_update",
                "description": "desc",
                "user": self.user.id
            }
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.remember_1.refresh_from_db()
        self.assertEqual('test_update', self.remember_1.name)

    def test_update_not_owner(self):
        self.client.force_login(self.user_4)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        data = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    12.02,
                    20.21
                ]
            },
            "properties": {
                "name": "test_update",
                "description": "desc",
                "user": self.user_4.id
            }
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.remember_1.refresh_from_db()
        self.assertEqual('name_1', self.remember_1.name)

    def test_update_not_owner_but_admin(self):
        self.client.force_login(self.user_3)

        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        data = {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    12.02,
                    20.21
                ]
            },
            "properties": {
                "name": "test_update",
                "description": "desc",
                "user": self.user.id
            }
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.remember_1.refresh_from_db()
        self.assertEqual('test_update', self.remember_1.name)

    def test_delete(self):
        self.client.force_login(self.user)

        self.assertEqual(4, RemembersModel.objects.all().count())
        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, RemembersModel.objects.all().count())

    def test_delete_not_owner(self):
        self.client.force_login(self.user_2)

        self.assertEqual(4, RemembersModel.objects.all().count())
        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
        self.assertEqual(4, RemembersModel.objects.all().count())

    def test_delete_not_owner_but_admin(self):
        self.client.force_login(self.user_3)

        self.assertEqual(4, RemembersModel.objects.all().count())
        url = reverse('remembers:remember-detail', args=(self.remember_1.id,))
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, RemembersModel.objects.all().count())
