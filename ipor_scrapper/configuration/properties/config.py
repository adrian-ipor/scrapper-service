import yaml
import pathlib
from dotenv import load_dotenv
from pyaml_env import parse_config
from loguru import logger

project_dir = pathlib.Path(__file__).parent.resolve().parent.parent
env_file = project_dir / '.env'
load_dotenv(env_file)
logger.info('path to env_file {}', env_file)


class ProductionConfig:

    def __init__(self):
        parent_path = pathlib.Path(__file__).parent.resolve()
        self.configuration_file = f"{parent_path}/configuration.yaml"

    def import_configuration(self):
        config = parse_config(self.configuration_file)
        return config

    def export_configuration(self, config):
        file = open(self.configuration_file, 'w+')
        yaml.dump(config, file, sort_keys=False)
