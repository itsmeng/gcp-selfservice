


import socket
import logging
import os 
# Set up logging
logging.basicConfig(level=logging.INFO)

# Get the server hostname
server_hostname = socket.gethostname()
logging.info(f"Server hostname: {server_hostname}")

# Set variable based on server hostname
if server_hostname == "abc":
    logging.info(f"abc configuration")
    project_id = "abc123"
    region = "asia-southeast1"
    function_name = "function-1"    
else:
    logging.info(f"Default configuration")
    ## Value for other server ##
    project_id = "default-project"
    region = "asia-southeast1"
    function_name = "function-2"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "test.json"