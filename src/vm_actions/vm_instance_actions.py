from google.cloud import compute_v1

# Initialize clients
compute_client = compute_v1.InstancesClient()

def start_vm(project, zone, instance):
    """
    Start a VM instance.
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to start.
    
    Returns:
        dict: A dictionary containing a success message or error details.
    """
    try:
        compute_client.start(project=project, zone=zone, instance=instance)
        return {"message": f"VM {instance} start initiated"}
    except Exception as e:
        raise RuntimeError(f"Error starting VM: {e}")

def stop_vm(project, zone, instance):
    """
    Stop a VM instance.
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to stop.
    
    Returns:
        dict: A dictionary containing a success message or error details.
    """
    try:
        compute_client.stop(project=project, zone=zone, instance=instance)
        return {"message": f"VM {instance} stop initiated"}
    except Exception as e:
        raise RuntimeError(f"Error stopping VM: {e}")

def restart_vm(project, zone, instance):
    """
    Restart a VM instance by stopping and then starting it.
    
    Args:
        project (str): The GCP project ID.
        zone (str): The zone where the instance is located.
        instance (str): The name of the instance to restart.
    
    Returns:
        dict: A dictionary containing a success message or error details.
    """
    try:
        stop_vm(project, zone, instance)
        start_vm(project, zone, instance)
        return {"message": f"VM {instance} restart initiated"}
    except Exception as e:
        raise RuntimeError(f"Error restarting VM: {e}")

def handle_vm_action(request):
    """
    Main entry point for the Cloud Function.
    
    Args:
        request (flask.Request): The request object.
    
    Returns:
        tuple: A tuple containing a dictionary with the result and an HTTP status code.
    """
    action = request.json.get('action')
    project = request.json.get('project')
    zone = request.json.get('zone')
    instance = request.json.get('instance')
    
    action_map = {
        'start': start_vm,
        'stop': stop_vm,
        'restart': restart_vm
    }
    
    if action not in action_map:
        return {"error": "Invalid action specified"}, 400
    
    try:
        result = action_map[action](project, zone, instance)
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500

