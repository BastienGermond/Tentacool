from django.core.files.uploadedfile import SimpleUploadedFile

from backend.tests.utils import TestCaseBackend

from unittest.mock import patch
from backend.models import Blob
from rest_framework.test import APIClient


class TestBackendUpload(TestCaseBackend):
    def setUp(self):
        self.add_user('test', 'test')

    @patch('backend.views.get_storage_class')
    def test_upload_file(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.save.return_value = \
            test_filename

        # Add right permission to upload
        self.add_permission(self.user_test, Blob, 'add_blob')

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
        self.add_permission(self.user_test, Blob, 'add_blob')

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

        self.assertEqual(403, response.status_code)
