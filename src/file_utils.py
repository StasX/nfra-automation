import os
import json
def read():
    machines=[]
    # Find real path of 
    current_file_path = os.path.realpath(__file__)
    current_directory_path = os.path.dirname(current_file_path)
    parent_directory_path = os.path.dirname(current_directory_path)
    configuration_file_path = parent_directory_path + "/configs/instances.json"
    # Check if configuration file already exists and load old configuration if user accept
    if  os.path.exists(configuration_file_path) and input("Do you want to load old configuration? for yes press Y: ").upper().strip() == "Y":
        with open(configuration_file_path, "r") as file:
            config_json = file.read()
            config = json.loads(config_json)
            machines = config
            file.close()
    return machines

def write(data,path):
    with open(path, "w") as file:
        file.write(json.dumps(data))
        file.close()
