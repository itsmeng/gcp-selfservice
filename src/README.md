# Cloud Functions Project Structure

This project contains cloud functions for managing various GCP resources. To maintain consistency and clarity, please follow the naming conventions and structure outlined below when adding new functionalities.

## Folder Naming Convention

Folders should be named using the following convention:

```
<service name>_<resource type>_<actions>
```

- `<service name>`: The GCP service being used (e.g., compute, iam)
- `<resource type>`: The specific resource being managed (e.g., instance, service_account_key)
- `<actions>`: A general term for the operations being performed (e.g., management)

### Examples:
- `compute_instance_management`
- `iam_service_account_key_management`

## File Naming Convention

Within each folder, use descriptive names for Python files that indicate their specific functionality:

- `main.py`: The entry point for the cloud function
- `<resource>_handler.py`: Contains the core operations for a specific resource

### Examples:
- `instance_handler.py`
- `service_account_key_handler.py`

## Code Structure

1. Each folder should contain:
   - `main.py`: Handles incoming requests and routes to appropriate functions
   - One or more operation files (e.g., `instance_handler.py`)
   - Any necessary utility or helper files

2. In operation files:
   - Group related functions together
   - Include a main handler function that routes to specific operations (e.g., `handle_vm_action`, `handle_iam_key_action`)

3. Use type hints and docstrings for all functions to improve readability and maintainability

## Adding New Functionality

When adding new functionality:

1. Determine if it fits into an existing folder or requires a new one
2. If creating a new folder, follow the naming convention
3. Create appropriate operation files
4. Update `main.py` to include the new operations
5. Add any necessary dependencies to `requirements.txt`

By following these guidelines, we can maintain a clean, organized, and easily navigable project structure as it grows and evolves.