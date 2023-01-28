# -*- coding: utf-8 -*-
import logging

from httpx import Client

from .account import AccountAPI


class Timeweb:
    '''Клиент для работы с API Timeweb Cloud

    Attributes:
        account (AccountAPI): API для работы с аккаунтом.
    '''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
        self.account = AccountAPI(token, client)
