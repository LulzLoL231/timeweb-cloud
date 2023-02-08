# -*- coding: utf-8 -*-
# flake8: noqa
'''Timeweb Cloud API client'''
from .__meta import __version__, __author__
from .sync_api.api import Timeweb
from .async_api.api import AsyncTimeweb


__all__ = [
    'Timeweb',
    'AsyncTimeweb',
    '__version__',
    '__author__',
]
