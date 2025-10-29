import nh3

def sanitize_json(content):
    if isinstance(content, dict):
        return {key:sanitize_json(value) for key, value in content.items()}
    elif isinstance(content, list):
        return [sanitize_json(value) for value in content]
    elif isinstance(content, str):
        return nh3.clean(content)
    else:
        return content