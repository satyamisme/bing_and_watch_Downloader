# 15.02.24

# Import
import json, subprocess, os, requests, configparser

# Variable


# [ func ]
def get_final_redirect_url(url):
    """Get real redirect url"""

    try:
        response = requests.get(url, allow_redirects=True)
        final_url = response.url
        return final_url
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def read_json(path):
    """Read JSON file and return its content"""

    with open(path, "r") as file:
        config = json.load(file)
    return config

def save_json(json_obj, path):
    """Save JSON object to the specified file path"""

    with open(path, 'w') as file:
        json.dump(json_obj, file, indent=4)  # Adjust the indentation as needed

def clean_json(path):
    """Read JSON data from the file"""

    data = read_json(path)

    # Recursively replace all values with an empty string
    def recursive_empty_string(obj):
        if isinstance(obj, dict):
            return {key: recursive_empty_string(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [recursive_empty_string(item) for item in obj]
        else:
            return ""

    modified_data = recursive_empty_string(data)

    # Save the modified JSON data back to the file
    save_json(modified_data, path)

def async_run_executable(path, log=True):
    """Run async executable file"""

    try:
        # Get the current working directory
        current_directory = os.getcwd()

        # Extract the directory path from the executable path
        executable_directory = os.path.dirname(path)

        # Change the current working directory to the executable directory
        os.chdir(executable_directory)

        # Run the executable file using subprocess
        process = subprocess.Popen([path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the process to finish
        process.wait()
        
        # Capture the output and error
        output, error = process.communicate()
        
        # Print the output of the executable if logging is enabled
        if log:
            print("Output:", output.decode())
        
        # Print any errors if logging is enabled
        if error and log:
            print("Error:", error.decode())

    except Exception as e:
        print("Error (async_run_executable) :", str(e))

    finally:
        # Change back to the original working directory
        os.chdir(current_directory)

def get_site_name():
    """Reads the 'site' variable from the 'settings' section of the config.ini file """

    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join("Src", "config.ini")))
    return config['settings']['site']

