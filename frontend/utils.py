import yaml
from yaml.loader import SafeLoader

# Function to load the config file
def load_config(path='./config.yaml'):
    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

# Function to save the config file
def save_config(config, path='./config.yaml'):
    with open(path, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False)