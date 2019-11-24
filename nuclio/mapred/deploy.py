import settings
import argparse
from model import Function, ConfigInfo, DeployInfo


def create_map_config_info():
    base = os.path.basename(settings.MAP_PATH)
    module_name = os.path.splitext(base)[0]
    return ConfigInfo(
        module_name, 
        settings.MAP_ENV, 
        settings.RMQ_URL,
        settings.EXCHANGE_NAME)

def create_map_config_info():
    base = os.path.basename(settings.MAP_PATH)
    module_name = os.path.splitext(base)[0]
    return ConfigInfo(
        module_name, 
        settings.MAP_ENV, 
        settings.RMQ_URL,
        settings.EXCHANGE_NAME)
    

def create_function(name, function_path, config_template_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mappers', '-m', type=int, default=5)
    parser.add_argument('--reducers', '-r', type=int, default=3)

    args = parser.parse_args()
