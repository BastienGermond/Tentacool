from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock import patch
from backend.models import Blob
from rest_framework.test import APIClient


class TestBackendUpload(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test',
        )

    def add_permission(self, object, perm):
        content_type = ContentType.objects.get_for_model(object)
        permission = Permission.objects.get(
            content_type=content_type,
            codename=perm
        )
        self.user.user_permissions.add(permission)

    @patch('backend.views.get_storage_class')
    def test_upload_file(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.save.return_value = \
            test_filename

        # Add right permission to upload
        self.add_permission(Blob, 'add_blob')

        upload_file = SimpleUploadedFile(
            test_filename,
            b"Content of test.txt",
            content_type='text/plain'
        )

        client = APIClient()
        self.assertTrue(client.login(username='test', password='test'))

        response = client.put(
            '/api/blobs/' + test_filename,
            {'file': upload_file}
        )

        self.assertEqual(204, response.status_code)

        self.assertTrue(Blob.objects.filter(s3_name=test_filename).exists())

    @patch('backend.views.get_storage_class')
    def test_upload_without_file(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.save.return_value = \
            test_filename

        # Add right permission to upload
        self.add_permission(Blob, 'add_blob')

        client = APIClient()
        self.assertTrue(client.login(username='test', password='test'))

        response = client.put('/api/blobs/' + test_filename)

        self.assertEqual(400, response.status_code)

    @patch('backend.views.get_storage_class')
    def test_upload_file_insufficent_permission(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.save.return_value = \
            test_filename

        client = APIClient()
        self.assertTrue(client.login(username='test', password='test'))

        response = client.put('/api/blobs/' + test_filename)
        self.assertEqual(403, response.status_code)
