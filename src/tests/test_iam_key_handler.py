import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.iam_service_account_key_management.key_handler import handle_iam_key_action

class TestIAMKeyHandler(unittest.TestCase):

    @patch('service_account_key.iam_key_handler.create_service_account_key')
    def test_create_service_account_key(self, mock_create):
        mock_create.return_value = {
            'private_key': b'private_key_data',
            'key_id': 'key_id',
            'service_account_email': 'email@example.com'
        }

        result = handle_iam_key_action({
            'action': 'create',
            'project_id': 'project_id',
            'service_account_email': 'email@example.com'
        })

        mock_create.assert_called_once_with('project_id', 'email@example.com')
        self.assertEqual(result, mock_create.return_value)

    @patch('service_account_key.iam_key_handler.delete_service_account_key')
    def test_delete_service_account_key(self, mock_delete):
        mock_delete.return_value = True

        result = handle_iam_key_action({
            'action': 'delete',
            'project_id': 'project_id',
            'service_account_email': 'email@example.com',
            'key_id': 'key_id'
        })

        mock_delete.assert_called_once_with('project_id', 'email@example.com', 'key_id')
        self.assertTrue(result)

    @patch('service_account_key.iam_key_handler.rotate_service_account_key')
    def test_rotate_service_account_key(self, mock_rotate):
        mock_rotate.return_value = {'new': 'key'}

        result = handle_iam_key_action({
            'action': 'rotate',
            'project_id': 'project_id',
            'service_account_email': 'email@example.com',
            'key_id': 'key_id'
        })

        mock_rotate.assert_called_once_with('project_id', 'email@example.com', 'key_id')
        self.assertEqual(result, {'new': 'key'})

    @patch('service_account_key.iam_key_handler.enable_service_account_key')
    def test_enable_service_account_key(self, mock_enable):
        mock_enable.return_value = True

        result = handle_iam_key_action({
            'action': 'enable',
            'project_id': 'project_id',
            'service_account_email': 'email@example.com',
            'key_id': 'key_id'
        })

        mock_enable.assert_called_once_with('project_id', 'email@example.com', 'key_id')
        self.assertTrue(result)

    @patch('service_account_key.iam_key_handler.disable_service_account_key')
    def test_disable_service_account_key(self, mock_disable):
        mock_disable.return_value = True

        result = handle_iam_key_action({
            'action': 'disable',
            'project_id': 'project_id',
            'service_account_email': 'email@example.com',
            'key_id': 'key_id'
        })

        mock_disable.assert_called_once_with('project_id', 'email@example.com', 'key_id')
        self.assertTrue(result)

    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            handle_iam_key_action({
                'action': 'invalid_action',
                'project_id': 'project_id',
                'service_account_email': 'email@example.com'
            })

if __name__ == '__main__':
    unittest.main()
