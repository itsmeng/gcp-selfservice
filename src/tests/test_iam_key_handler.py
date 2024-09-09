import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from service_account_key.iam_key_handler import (
    create_service_account_key,
    delete_service_account_key,
    rotate_service_account_key,
    enable_service_account_key,
    disable_service_account_key
)

class TestIAMKeyHandler(unittest.TestCase):

    @patch('service_account_key.iam_key_handler.iam_admin_v1.IAMClient')
    def test_create_service_account_key(self, mock_iam_client):
        mock_client = MagicMock()
        mock_iam_client.return_value = mock_client
        mock_response = MagicMock()
        mock_response.private_key_data = b'private_key_data'
        mock_response.name = 'projects/project_id/serviceAccounts/email@example.com/keys/key_id'
        mock_client.create_service_account_key.return_value = mock_response

        result = create_service_account_key('project_id', 'email@example.com')
        print(result)

        mock_client.create_service_account_key.assert_called_once_with(name='projects/project_id/serviceAccounts/email@example.com')
        self.assertEqual(result['private_key'], b'private_key_data')
        self.assertEqual(result['key_id'], 'key_id')
        self.assertEqual(result['service_account_email'], 'email@example.com')

    @patch('service_account_key.iam_key_handler.iam_admin_v1.IAMClient')
    def test_delete_service_account_key(self, mock_iam_client):
        mock_client = MagicMock()
        mock_iam_client.return_value = mock_client

        result = delete_service_account_key('project_id', 'email@example.com', 'key_id')

        mock_client.delete_service_account_key.assert_called_once_with(name='projects/project_id/serviceAccounts/email@example.com/keys/key_id')
        self.assertTrue(result)

    @patch('service_account_key.iam_key_handler.delete_service_account_key')
    @patch('service_account_key.iam_key_handler.create_service_account_key')
    def test_rotate_service_account_key(self, mock_create, mock_delete):
        mock_delete.return_value = True
        mock_create.return_value = {'new': 'key'}

        result = rotate_service_account_key('project_id', 'email@example.com', 'key_id')

        mock_delete.assert_called_once_with('project_id', 'email@example.com', 'key_id')
        mock_create.assert_called_once_with('project_id', 'email@example.com')
        self.assertEqual(result, {'new': 'key'})

    @patch('service_account_key.iam_key_handler.iam_admin_v1.IAMClient')
    def test_enable_service_account_key(self, mock_iam_client):
        mock_client = MagicMock()
        mock_iam_client.return_value = mock_client

        result = enable_service_account_key('project_id', 'email@example.com', 'key_id')

        mock_client.enable_service_account_key.assert_called_once_with(name='projects/project_id/serviceAccounts/email@example.com/keys/key_id')
        self.assertTrue(result)

    @patch('service_account_key.iam_key_handler.iam_admin_v1.IAMClient')
    def test_disable_service_account_key(self, mock_iam_client):
        mock_client = MagicMock()
        mock_iam_client.return_value = mock_client

        result = disable_service_account_key('project_id', 'email@example.com', 'key_id')


        mock_client.disable_service_account_key.assert_called_once_with(name='projects/project_id/serviceAccounts/email@example.com/keys/key_id')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
