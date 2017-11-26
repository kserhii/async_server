import logging

from aiohttp import web

__author__ = 'Serhii Kostel'

log = logging.getLogger('srv.handler.web')


async def index(request: 'web.Request'):
    """Main page mock"""
    return web.Response(
        text='<h1>Here must be the Main Page!</h1>')
