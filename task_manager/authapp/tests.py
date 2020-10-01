from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TaskTestCase(APITestCase):
    task_list_url = reverse('taskapp:tasks')

    def setUp(self):
        self.user = self.client.post('/authapp/registration/', data={'username': 'test4@test.local', 'password': '123'})
        response = self.client.post('/authapp/login/', data={'username': 'test4@test.local', 'password': '123'})
        self.token = response.data['Authorization']

    def test_task_list(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        response = self.client.get(self.task_list_url, data={'task_name': '22', 'task_description': 'do something',
                                                             'task_status': 'N',
                                                             'task_finished_data': '2020-10-12 15:00'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

