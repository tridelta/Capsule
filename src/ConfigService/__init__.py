from .secret import get_secret
import yaml

config = yaml.safe_load(open("ConfigService/config.local.yaml"))
PROJECT_ROOT = config["PROJECT_ROOT"]
