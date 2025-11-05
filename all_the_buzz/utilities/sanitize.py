import nh3
import re

'''
sanitize.py

This module contains a function for sanitizing external inputs to avoid 
code injection.

Functions:
    sanitize_json: function that uses the nh3 library to sanitize strings
    '''

def sanitize_json(content):
    """
    This function uses the nh3 library to clean inputs.
    
    Args:
        content: this is either a dictionary, list, or string that needs to be
            sanitized (if it's not of this type it will be just returned)
        
    Returns:
        either cleaned content if proper format or the original content input
        """
    if isinstance(content, dict):
        return {key:sanitize_json(value) for key, value in content.items()}
    elif isinstance(content, list):
        return [sanitize_json(value) for value in content]
    elif isinstance(content, str):
        text = nh3.clean(content, tags=set())
        text = re.sub(r"\{[^{}]*\}", "", text)
        text = re.sub(r"\$[a-zA-Z]+", "", text)
        return text
    else:
        return content
    

