import json
import os

_config = None


def load_config():
    global _config
    if _config is not None:
        return _config
    config_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(config_dir, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        _config = json.load(f)
    return _config


config = load_config()
