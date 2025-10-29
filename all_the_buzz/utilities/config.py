import yaml

def config_file_reader(path):
    with open(path, "r") as file:
        data=yaml.safe_load(file) 
    return data