import yaml
"""
config.py

This module contains a function for loading config files.

Functions:
    - config_file_reader: function that reads config file
"""
def config_file_reader(path):
    """
    Function for reading config file in yaml format.
    
    Args:
        path: string that is path to config file
        
    Returns:
        data: dictionary containing config file information
        """
    with open(path, "r") as file:
        data=yaml.safe_load(file) 
    return data



