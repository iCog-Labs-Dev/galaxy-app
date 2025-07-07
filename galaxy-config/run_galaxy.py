import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lib')))
from galaxy.webapps.galaxy.app import app_factory
from galaxy.util.properties import load_app_properties

if __name__ == '__main__':
    # Create database directories
    os.makedirs("database/files", exist_ok=True)
    os.makedirs("database/job_working_directory", exist_ok=True)
    
    # Load configuration
    properties = load_app_properties(ini_file='config/galaxy.yml')
    
    # Create and run application
    app = app_factory(global_conf=properties)
    app.run(host='0.0.0.0', port=8080, debug=True)
