import logging

from aiohttp import web

__author__ = 'Serhii Kostel'

log = logging.getLogger('srv.handler.api')


async def user(request: 'web.Request'):
    """User API mock"""
    return web.Response(text='{"API": "mock"}')
