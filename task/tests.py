import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from task.models import Task


class TaskTest(APITestCase):
    def setUp(self):
        self.userModel = get_user_model()
        self.userCredentials = {
            'email': 'test@test.com',
            'password': 'password'
        }
        self.user = self._create_user(self.userCredentials['email'],
                                      self.userCredentials['password'])

    def test_get_all_tasks(self):
        # add other user tasks to check it's receive only the authenticated user's tasks
        other_user = self._create_user('test2@test.com', 'password')
        self._create_tasks(other_user, 5)

        self._create_tasks(self.user)
        self._authenticate()
        self.client.login(email='test@test.com', password='password')
        response = self.client.get(reverse('task-list-create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 5)

    def test_get_valid_single_task(self):
        tasks_id = self._create_tasks(self.user)
        self._authenticate()
        response = self.client.get(reverse('task-get-update-delete', kwargs={'pk': tasks_id[0]}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_get_valid_task_without_authentication(self):
        tasks_id = self._create_tasks(self.user)
        response = self.client.get(reverse('task-get-update-delete', kwargs={'pk': tasks_id[0]}))
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['detail'], 'Authentication credentials were not provided.')

    def test_get_single_task_that_belongs_to_other_user(self):
        other_user = self._create_user('test2@test.com', 'password')
        tasks_id = self._create_tasks(other_user, 1)
        self._authenticate()
        response = self.client.get(reverse('task-get-update-delete', kwargs={'pk': tasks_id[0]}))
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json['detail'], 'Not found.')

    def test_create_valid_task(self):
        self._authenticate()
        response = self.client.post(reverse('task-list-create'), {
            'title': 'My task',
            'status': 'DOING'
        })
        self.assertEqual(response.status_code, 201)

    def test_update_task(self):
        tasks = self._create_tasks(self.user, 1)
        self._authenticate()
        response = self.client.put(reverse('task-get-update-delete', kwargs={'pk': tasks[0]}), {
            'title': 'My task',
            'status': 'DONE',
            'description': 'This is my long description of the updated task'
        })
        self.assertEqual(response.status_code, 200)
        updated_task = Task.objects.get(pk=tasks[0])
        self.assertEqual(updated_task.title, 'My task')
        self.assertEqual(updated_task.status, 'DONE')
        self.assertEqual(updated_task.description, 'This is my long description of the updated task')

    def test_valid_delete_task(self):
        tasks = self._create_tasks(self.user, 1)
        self._authenticate()
        response = self.client.delete(reverse('task-get-update-delete', kwargs={'pk': tasks[0]}))
        self.assertEqual(response.status_code, 204)

    def _create_user(self, email, password):
        return self.userModel.objects.create_user(email=email, password=password, name='Test Tester')

    def _authenticate(self):
        response = self.client.post(reverse('user-login'), {
            'email': self.userCredentials['email'],
            'password': self.userCredentials['password']
        }, follow=True)
        tokens = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access']))
        return tokens

    def _create_tasks(self, user, no=5):
        ids = []
        for i in range(no):
            task = Task.objects.create(
                owned_by=user,
                title='Task {}'.format(i + 1),
                description='Some description',
                status="TODO"
            )
            ids.append(task.pk)
        return ids
