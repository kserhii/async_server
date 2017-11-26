import sys
import logging
import asyncio

import aiohttp_autoreload
from aiohttp.web import Application

from server.handlers import web, api

__author__ = 'Serhii Kostel'

LOG_BASE_NAME = 'srv'
LOG_FORMAT = '%(levelname)-6.6s | %(name)-15s | %(asctime)s.%(msecs)03d | %(message)s'
LOG_DATE_FORMAT = '%d.%m %H:%M:%S'

log = logging.getLogger('srv.app')


# Routes

routes = {
    '/': [
        ('GET', '/', web.index, 'index'),
    ],
    '/api': [
        ('GET', '/user', api.user, 'user'),
    ]
}


# Application

class CreateAppError(Exception):
    pass


def create_app(config: 'dict') -> 'Application':
    """Create server application and all necessary services.

    :param config: server settings
    """
    logger_configure(
        level=config['LOG_LEVEL'],
        root_level=config['LOG_ROOT_LEVEL'])

    app = Application(debug=config['DEBUG'])
    app['config'] = config

    if config['DEBUG'] and not config['TESTING']:
        log.warning('Run in DEBUG mode!')
        aiohttp_autoreload.start()

    api_app = Application()
    app['api'] = api_app

    register_routes(api_app, routes['/api'])
    app.add_subapp('/api', api_app)

    register_routes(app, routes['/'])

    return app


def register_routes(app: 'Application', routes_table):
    """Add routes handlers of the server."""
    for method, path, handler, name in routes_table:
        app.router.add_route(method,  path, handler, name=name)


def logger_configure(level: 'str'='DEBUG', root_level: 'str'='DEBUG') -> 'None':
    """Configure console logger."""
    log_handler = logging.StreamHandler(stream=sys.stdout)

    log_formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    log_handler.setFormatter(log_formatter)

    # root logger
    logging.getLogger('').addHandler(log_handler)
    logging.getLogger('').setLevel(root_level)

    # local logger
    logging.getLogger(LOG_BASE_NAME).setLevel(level)


async def shutdown_tasks(app: 'Application') -> 'None':
    """Shutdown unfinished async tasks.

    :param app: web server application
    """
    log.info('Shutdown tasks')

    tasks = asyncio.Task.all_tasks(loop=app.loop)
    if tasks:
        for task in tasks:
            task.cancel()
        try:
            await asyncio.wait(tasks)
        except Exception:
            pass
