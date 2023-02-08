# -*- coding: utf-8 -*-
# flake8: noqa
'''Timeweb Cloud API client'''
from .__meta import __version__, __author__
from .sync_api.api import Timeweb


__all__ = [
    'Timeweb',
    '__version__',
    '__author__',
]
