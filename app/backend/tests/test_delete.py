from backend.tests.utils import TestCaseBackend

from unittest.mock import patch
from backend.models import Blob
from rest_framework.test import APIClient


class TestBackendUpload(TestCaseBackend):
    def setUp(self):
        self.add_user('test', 'test')
        self.add_user('test2', 'test')
        Blob.objects.create(
            owner=self.user_test,
            filename='tests.txt',
            s3_name='test',
            content_type='plain/text',
        )

    @patch('backend.views.get_storage_class')
    def test_delete_file_success(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.exists.return_value = True
        get_storage_class.return_value.return_value.delete.return_value = True

        # Add right permission to delete
        self.add_permission(self.user_test, Blob, 'delete_blob')

        client = APIClient()
        self.assertTrue(client.login(username='test', password='test'))

        response = client.delete('/api/blobs/' + test_filename)
        self.assertEqual(200, response.status_code)

        self.assertFalse(Blob.objects.filter(filename=test_filename).exists())

    @patch('backend.views.get_storage_class')
    def test_not_the_owner(self, get_storage_class):
        test_filename = 'tests.txt'

        # Mock storage
        get_storage_class.return_value.return_value.exists.return_value = True
        get_storage_class.return_value.return_value.delete.return_value = True

        # Add right permission to delete
        self.add_permission(self.user_test2, Blob, 'delete_blob')

        client = APIClient()
        self.assertTrue(client.login(username='test2', password='test'))

        response = client.delete('/api/blobs/' + test_filename)
        self.assertEqual(403, response.status_code)

        self.assertTrue(Blob.objects.filter(filename=test_filename).exists())

    def test_doesn_t_exists(self):
        client = APIClient()
        self.assertTrue(client.login(username='test', password='test'))

        response = client.delete('/api/blobs/notafile/')
        self.assertEqual(404, response.status_code)
