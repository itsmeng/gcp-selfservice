from google.cloud import iam_admin_v1
from typing import Dict, List
from google.api_core import exceptions as google_exceptions

def create_service_account_key(project_id, service_account_email):
    """
    Create a new service account key.
    
    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.
    
    Returns:
        dict: A dictionary containing the new key's private key, key ID, and service account email.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}"
        response = client.create_service_account_key(name=name)
        
        return {
            "private_key": response.private_key_data,
            "key_id": response.name.split('/')[-1],
            "service_account_email": service_account_email,
            "message": f"Access key for {name} created successfully"
        }
    except Exception as e:
        raise RuntimeError(f"Error creating service account key: {e}")

def delete_service_account_key(project_id, service_account_email, key_id):
    """
    Delete a service account key.
    
    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.
        key_id (str): The ID of the key to delete.
    
    Returns:
        dict: A dictionary containing a message about the operation result.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.delete_service_account_key(name=name)
        return {"message": f"Successfully deleted key {key_id}"}
    except google_exceptions.FailedPrecondition as e:
        return {"message": f"Failed to delete key {key_id}. The key may not exist: {str(e)}"}
    except Exception as e:
        return {"message": f"Error deleting service account key {key_id}: {str(e)}"}

def rotate_service_account_key(project_id, service_account_email, key_id):
    """
    Rotate a service account key by deleting the old one and creating a new one.
    
    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.
        key_id (str): The ID of the key to rotate.
    
    Returns:
        dict: The newly created service account key, or None if rotation failed.
    """
    if delete_service_account_key(project_id, service_account_email, key_id):
        return create_service_account_key(project_id, service_account_email)
    return None

def enable_service_account_key(project_id, service_account_email, key_id):
    """
    Enable a service account key.
    
    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.
        key_id (str): The ID of the key to enable.
    
    Returns:
        dict: A dictionary containing a message about the operation result.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.enable_service_account_key(name=name)
        return {"message": f"Successfully enabled key {key_id}"}
    except Exception as e:
        raise RuntimeError(f"Error enabling service account key: {e}")

def disable_service_account_key(project_id, service_account_email, key_id):
    """
    Disable a service account key.
    
    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.
        key_id (str): The ID of the key to disable.
    
    Returns:
        dict: A dictionary containing a message about the operation result.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.disable_service_account_key(name=name)
        return {"message": f"Successfully disabled key {key_id}"}
    except Exception as e:
        raise RuntimeError(f"Error disabling service account key: {e}")

def list_service_account_keys(project_id: str, service_account_email: str) -> List[str]:
    """
    List all keys for a given service account.

    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.

    Returns:
        List[str]: A list of key IDs for the service account.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}"
        response = client.list_service_account_keys(name=name)
        key_ids = []
        for key in response.keys:
            if str(key.key_type) != "KeyType.SYSTEM_MANAGED":
                key_id = key.name.split('/')[-1]
                key_ids.append(key_id)
        
        return key_ids
    
    except Exception as e:
        raise RuntimeError(f"Error listing service account keys: {e}")

def delete_all_service_account_keys(project_id: str, service_account_email: str) -> Dict[str, List[str]]:
    """
    Delete all keys for a given service account.

    Args:
        project_id (str): The GCP project ID.
        service_account_email (str): The service account email.

    Returns:
        Dict[str, List[str]]: A dictionary with a "message" key containing a list of deleted key IDs.
    """
    key_ids = list_service_account_keys(project_id, service_account_email)
    deleted_keys = []
    for key_id in key_ids:
        result = delete_service_account_key(project_id, service_account_email, key_id)
        if result.get("message", "").startswith("Successfully deleted"):
            deleted_keys.append(key_id)
    return {"message": f"deleted_keys: {deleted_keys}"}

def handle_iam_key_action(request_data: Dict[str, str]) -> Dict[str, str]:
    """
    Handle IAM key actions based on the provided request data.
    
    Args:
        request_data (Dict[str, str]): A dictionary containing the action details.
            Expected keys: 'action', 'project_id', 'service_account_email', 'key_id' (optional)
    
    Returns:
        Dict[str, Any]: A dictionary with the result of the IAM key action.
    
    Raises:
        ValueError: If an unknown action is provided.
    """
    action = request_data.get('action')
    project_id = request_data.get('project_id')
    service_account_email = request_data.get('service_account_email')
    key_id = request_data.get('key_id')

    action_map = {
        'create': create_service_account_key,
        'delete': delete_service_account_key,
        'rotate': rotate_service_account_key,
        'enable': enable_service_account_key,
        'disable': disable_service_account_key,
        'delete_all': delete_all_service_account_keys
    }
    
    if action not in action_map:
        raise ValueError(f"Unknown action: {action}")
    
    if action == 'create':
        result = action_map[action](project_id, service_account_email)
    elif action == 'delete_all':
        result = action_map[action](project_id, service_account_email)
    elif action in ['delete', 'rotate', 'enable', 'disable']:
        if not key_id:
            raise ValueError(f"Key ID is required for {action} action")
        result = action_map[action](project_id, service_account_email, key_id)
    else:
        raise ValueError(f"Unexpected action: {action}")
    return result
