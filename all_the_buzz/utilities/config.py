import yaml
import os

class YamlReader:
    @staticmethod
    def read_yaml(base_dir: str, config_name: str):
        config_path = os.path.join(base_dir, 'configs', 'logging_config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print(type(config))