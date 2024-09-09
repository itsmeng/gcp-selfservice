from google.cloud import iam_admin_v1

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
            "service_account_email": service_account_email
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
        bool: True if deletion was successful, False otherwise.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.delete_service_account_key(name=name)
        return True
    except Exception as e:
        raise RuntimeError(f"Error deleting service account key: {e}")

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
        bool: True if enabling was successful, False otherwise.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.enable_service_account_key(name=name)
        return True
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
        bool: True if disabling was successful, False otherwise.
    """
    try:
        client = iam_admin_v1.IAMClient()
        name = f"projects/{project_id}/serviceAccounts/{service_account_email}/keys/{key_id}"
        client.disable_service_account_key(name=name)
        return True
    except Exception as e:
        raise RuntimeError(f"Error disabling service account key: {e}")
