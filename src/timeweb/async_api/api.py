# -*- coding: utf-8 -*-
'''Асинхронный клиент для Timeweb Cloud API'''
import logging

from httpx import AsyncClient


class AsyncTimeweb:
    '''Клиент для работы с API Timeweb Cloud

    Attributes:
        account (AccountAPI): API для работы с аккаунтом.
    '''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
