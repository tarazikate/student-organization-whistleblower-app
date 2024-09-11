from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from .models import UploadedFile
from django.contrib.auth.models import User, Group
from .views import index, file_upload_view, list_files_view


class UploadedFileTest(TestCase):
    def setUp(self):
        self.test_file = SimpleUploadedFile('test_file.txt', b'this is the file.')
        self.uploaded_file = UploadedFile.objects.create(file=self.test_file)

    def test_file_field(self):
        file_instance = UploadedFile.objects.get(file='test_file.txt')
        self.assertEqual(file_instance.file.name, 'test_file.txt')

from django.contrib.auth.models import User, Group

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.test_user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.test_user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.group = Group.objects.create(name='Site Admins')
        self.test_user1.groups.add(self.group)

    def test_redirect_when_user_is_not_authenticated(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/accounts/login/?next=/')

    def test_authenticated_user_is_not_redirected(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_admin_user_sees_admin_template(self):
        self.client.login(username='testuser1', password='testpassword1')
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'admin_user.html')

    def test_non_admin_user_sees_user_template(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'user.html')

