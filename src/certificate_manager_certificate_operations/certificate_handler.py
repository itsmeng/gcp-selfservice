from google.cloud import certificate_manager_v1
from google.protobuf import field_mask_pb2
from typing import Dict, List

def certificate_manager_certificate_create_managed(request_data: Dict) -> Dict:
    """Create a new managed certificate."""
    project_id = request_data['project_id']
    name = request_data['name']
    client = certificate_manager_v1.CertificateManagerClient()
    parent = f"projects/{project_id}/locations/global"
    certificate = certificate_manager_v1.Certificate(
        name=name,
        description=request_data['description'],
        scope=request_data['scope'],
        managed=certificate_manager_v1.Certificate.ManagedCertificate (
            domains=request_data['domains'] ##Must be a list 
        )
    )
    try:
        operation = client.create_certificate(parent=parent, certificate_id=name, certificate=certificate)
        result = operation.result()
        return {"message": f"Managed certificate {result.name} created successfully"}
    except Exception as e:
        return {"error": f"Error creating managed certificate: {str(e)}"}

def certificate_manager_certificate_create_self_uploaded(request_data: Dict) -> Dict:
    """Create a new self-uploaded certificate."""
    project_id = request_data['project_id']
    name = request_data['name']
    client = certificate_manager_v1.CertificateManagerClient()
    parent = f"projects/{project_id}/locations/global"
    certificate = certificate_manager_v1.Certificate(
        name=name,
        description=request_data['description'],
        scope=request_data['scope'],
        self_managed=certificate_manager_v1.Certificate.SelfManagedCertificate(
            pem_certificate=request_data['certificate'],
            pem_private_key=request_data['private_key']
        )
    )
    try:
        operation = client.create_certificate(parent=parent, certificate_id=name, certificate=certificate)
        result = operation.result()
        return {"message": f"Self-uploaded certificate {result.name} created successfully"}
    except Exception as e:
        return {"error": f"Error creating self-uploaded certificate: {str(e)}"}

def certificate_manager_certificate_delete(request_data: Dict) -> Dict:
    """Delete a certificate."""
    project_id = request_data['project_id']
    name = request_data['name']
    client = certificate_manager_v1.CertificateManagerClient()
    certificate_name = f"projects/{project_id}/locations/global/certificates/{name}"
    try:
        operation = client.delete_certificate(name=certificate_name)
        operation.result()
        return {"message": f"Certificate {name} deleted successfully"}
    except Exception as e:
        return {"error": f"Error deleting certificate: {str(e)}"}

def certificate_manager_certificate_get(request_data: Dict) -> Dict:
    """Get details of a certificate."""
    project_id = request_data['project_id']
    name = request_data['name']
    client = certificate_manager_v1.CertificateManagerClient()
    certificate_name = f"projects/{project_id}/locations/global/certificates/{name}"
    try:
        certificate = client.get_certificate(name=certificate_name)
        return str(certificate)
    except Exception as e:
        return {"error": f"Error getting certificate details: {str(e)}"}

def certificate_manager_certificate_update(request_data: Dict) -> Dict:
    """
    Update a certificate in Google Cloud Certificate Manager.
    
    For managed certificates:
    - Can update both description and domains.
    
    For self-uploaded certificates:
    - Can only update the description.

    Args:
        request_data (Dict): A dictionary containing:
            - project_id (str): The GCP project ID.
            - name (str): The name of the certificate to update.
            - description (str, optional): New description for the certificate.
            - domains (list, optional): New list of domains for managed certificates.

    Returns:
        Dict: A dictionary with a success message or error details.
    """
    project_id = request_data['project_id']
    name = request_data['name']
    client = certificate_manager_v1.CertificateManagerClient()
    certificate_name = f"projects/{project_id}/locations/global/certificates/{name}"

    try:
        # Get the current certificate
        current_cert = client.get_certificate(name=certificate_name)

        # Initialize update mask paths
        update_mask_paths = []

        # Update description if provided
        if 'description' in request_data:
            current_cert.description = request_data['description']
            update_mask_paths.append('description')

        # Update domains if provided and certificate is managed
        if 'domains' in request_data and current_cert.managed:
            current_cert.managed.domains = request_data['domains']
            update_mask_paths.append('managed.domains')

        # If no updates are requested, return early
        if not update_mask_paths:
            return {"message": "No updates requested"}

        # Create update mask
        update_mask = field_mask_pb2.FieldMask(paths=update_mask_paths)

        # Update the certificate
        operation = client.update_certificate(certificate=current_cert, update_mask=update_mask)
        result = operation.result()

        return {"message": f"Certificate {result.name} updated successfully"}
    except Exception as e:
        return {"error": f"Error updating certificate: {str(e)}"}



def certificate_manager_certificate_handle_action(request_data: Dict[str, str]) -> Dict:
    """Handle Certificate Manager actions based on the provided request data."""
    action = request_data['action']

    action_map = {
        'create': certificate_manager_certificate_create_managed,
        'create_self_uploaded': certificate_manager_certificate_create_self_uploaded,
        'delete': certificate_manager_certificate_delete,
        'get': certificate_manager_certificate_get,
        'update': certificate_manager_certificate_update,
    }
    
    if action not in action_map:
        raise NotImplementedError(f"Unknown action: {action}")
    else:
        return action_map[action](request_data)


## payload sample
# response = certificate_handler.certificate_manager_certificate_handle_action({"action": "create_self_uploaded", "project_id": "project-x", "name": "dummycert1", "description": "dummycert", "scope": "DEFAULT", "certificate": cert, "private_key": private_key})
# #response = certificate_handler.certificate_manager_certificate_handle_action({"action": "create", "project_id": "project-x", "name": "dummycert2", "description": "dummycert", "scope": "DEFAULT", "domains" : ["example5.com"]})
# #response = certificate_handler.certificate_manager_certificate_handle_action({"action": "delete", "project_id": "project-x", "name": "dummycert1" })
# #response = certificate_handler.certificate_manager_certificate_handle_action({"action": "get", "project_id": "project-x", "name": "dummycert2" })
# response = certificate_handler.certificate_manager_certificate_handle_action({"action": "update", "project_id": "project-x", "name": "dummycert2", "description": "helloo world 2", "domains" : ["example777.com"] })