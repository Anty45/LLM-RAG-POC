from pathlib import Path

import yaml


def load_conf(path_to_conf: Path):
    with open(path_to_conf, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
