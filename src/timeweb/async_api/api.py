# -*- coding: utf-8 -*-
'''Асинхронный клиент для Timeweb Cloud API'''
import logging

from httpx import AsyncClient

from .tokens import TokensAPI
from .account import AccountAPI
from .ssh_keys import SSHKeysAPI


class AsyncTimeweb:
    '''Клиент для работы с API Timeweb Cloud

    Attributes:
        account (AccountAPI): API для работы с аккаунтом.
        tokens (TokensAPI): API для работы с токенами.
        ssh_keys (SSHKeysAPI): API для работы с SSH ключами.
    '''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
        self.account = AccountAPI(token, client)
        self.tokens = TokensAPI(token, client)
        self.ssh_keys = SSHKeysAPI(token, client)
