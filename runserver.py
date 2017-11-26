#!venv/bin/python
"""
Simple Async Web Server

Usage:
    runserver.py [-h] [--config CONFIG] [--host] [--port]

Examples:
    ./runserver.py --help                     : show help
    ./runserver.py                            : default config.yaml, port - defined in config.yaml
    ./runserver.py --config=prod --port=8000  : prod.yaml, port=8000
"""

import logging

import click
from aiohttp import web

from server import app
from config import load_config

__author__ = 'Serhii Kostel'

SERVICE_NAME = 'Simple Async Web Server'

log = logging.getLogger('srv.run')


@click.command()
@click.option('--config', type=str, help='server configuration file name')
@click.option('--host', default='127.0.0.1', help='server host (default "127.0.0.1")')
@click.option('--port', default=None, type=int, help='server port')
def runserver(config, host, port):
    """Simple Async Web Server."""

    # Load configuration
    try:
        app_config = load_config(config_file=config, port=port)
    except (ValueError, FileNotFoundError) as err:
        log.critical(f'Config error: {err}\n'
                     'Run: \n    ./runserver.py --config=<config_file_name>')
        return

    # Create and run Application
    try:
        srv_app = app.create_app(config=app_config)
        srv_app.on_cleanup.append(app.shutdown_tasks)

    except KeyError:
        log.critical('Key field missing. Please check config file!', exc_info=True)
        return

    except app.CreateAppError as err:
        log.critical('Can\'t create "%s"\n\n%s\n', SERVICE_NAME, err)
        return

    log.info('Starting %s...', SERVICE_NAME)
    log.debug('Project config: %s', config)
    web.run_app(srv_app, host=host, port=app_config['PORT'])

    log.info('%s Stopped!', SERVICE_NAME)


if __name__ == '__main__':
    runserver()
