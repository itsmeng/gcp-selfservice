from google.cloud import compute_v1
from typing import Dict
import time

# Initialize clients
compute_client = compute_v1.InstancesClient()

def start_vm(project: str, zone: str, instance: str) -> Dict[str, str]:
    """
    Start a VM instance.
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to start.
    
    Returns:
        Dict[str, str]: A dictionary containing a success message.
    
    Raises:
        RuntimeError: If there's an error starting the VM.
    """
    try:
        compute_client.start(project=project, zone=zone, instance=instance)
        return {"message": f"VM {instance} start initiated"}
    except Exception as e:
        raise RuntimeError(f"Error starting VM: {e}")

def stop_vm(project: str, zone: str, instance: str) -> Dict[str, str]:
    """
    Stop a VM instance.
    
    Args: 
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to stop.
    
    Returns:
        Dict[str, str]: A dictionary containing a success message.
    
    Raises:
        RuntimeError: If there's an error stopping the VM.
    """
    try:
        compute_client.stop(project=project, zone=zone, instance=instance)
        return {"message": f"VM {instance} stop initiated"}
    except Exception as e:
        raise RuntimeError(f"Error stopping VM: {e}")

def restart_vm(project: str, zone: str, instance: str) -> Dict[str, str]:
    """
    Restart a VM instance by stopping and then starting it.
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to restart.
    
    Returns:
        Dict[str, str]: A dictionary containing a success message.
    
    Raises:
        RuntimeError: If there's an error restarting the VM.
    """
    try:
        stop_vm(project, zone, instance)
        
        # Wait for the VM to fully stop
        start_time = time.time()
        timeout = 540  # 9 minutes (considering max Cloud Function time of 10 minutes)
        while True:
            if time.time() - start_time > timeout:
                return {"message": f"Timeout waiting for VM {instance} to stop"}
            
            vm_info = compute_client.get(project=project, zone=zone, instance=instance)
            if vm_info.status == 'TERMINATED':
                break
            time.sleep(5)  # Wait for 5 seconds before checking again
            print(vm_info.status)
        
        start_vm(project, zone, instance)
        return {"message": f"VM {instance} restart initiated"}
    except Exception as e:
        raise RuntimeError(f"Error restarting VM: {e}")

def reset_vm(project: str, zone: str, instance: str) -> Dict[str, str]:
    """
    Reset a VM instance (hard reset).
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to reset.
    
    Returns:
        Dict[str, str]: A dictionary containing a success message.
    
    Raises:
        RuntimeError: If there's an error resetting the VM.
    """
    try:
        compute_client.reset(project=project, zone=zone, instance=instance)
        return {"message": f"VM {instance} reset initiated"}
    except Exception as e:
        raise RuntimeError(f"Error resetting VM: {e}")

def handle_vm_action(request_data: Dict[str, str]) -> Dict[str, str]:
    """
    Handle VM actions based on the provided request data.
    
    Args:
        request_data (Dict[str, str]): A dictionary containing the action details.
            Expected keys: 'action', 'project', 'zone', 'instance'
    
    Returns:
        Dict[str, str]: A dictionary with the result of the VM action.
    
    Raises:
        ValueError: If an unknown action is provided.
    """
    action = request_data.get('action')
    project = request_data.get('project')
    zone = request_data.get('zone')
    instance = request_data.get('instance')

    action_map = {
        'start': start_vm,
        'stop': stop_vm,
        'restart': restart_vm,
        'reset': reset_vm  # Add the new reset action
    }
    
    if action not in action_map:
        raise ValueError(f"Unknown action: {action}")
    
    result = action_map[action](project, zone, instance)
    return result

