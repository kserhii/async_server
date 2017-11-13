from pathlib import Path

import yaml

__author__ = 'Serhii Kostel'

CURRENT_DIR = Path(__file__).parent
DEFAULT_CONFIG_FILE = CURRENT_DIR / Path('config.yaml')


def load_config(config_file: 'str', **extra) -> 'dict':
    """Load project configuration from yaml file.

    File config.yaml contains default settings.

    If your want to create prod/dev/test configurations,
    just create yaml file in current folder and redefine
    only those fields that are changed.
    Specify name of the new config in "config" arg of the
    runserver.py script.

    :param str config_file: config yaml file with updated fields
        (e.g. dev or dev.yaml or /absolute/path/config/dev.yaml)
    :param extra: extra not None fields that can be redefined
        (e.g. PORT=4321)
    :return: configuration dict
    """
    with DEFAULT_CONFIG_FILE.open() as cf:
        conf = yaml.load(cf.read())

    if not config_file:
        raise ValueError('Configuration file not specified.')

    config_path = Path(config_file).with_suffix('.yaml')

    if not config_path.is_absolute():
        config_path = CURRENT_DIR / config_path

    if not config_path.exists():
        raise FileNotFoundError(
            f'Configuration file "{config_path}" not found!')

    with config_path.open() as ecf:
        extra_conf = yaml.load(ecf.read())

    conf.update(extra_conf)

    if extra:
        extra_fields = {
            key.upper(): val for key, val in extra.items()
            if val is not None}
        conf.update(extra_fields)

    return conf
