# -*- coding: utf-8 -*-
'''Синхронный клиент для Timeweb Cloud API'''
import logging

from httpx import Client

from .s3 import BucketsAPI
from .tokens import TokensAPI
from .images import ImagesAPI
from .account import AccountAPI
from .ssh_keys import SSHKeysAPI


class Timeweb:
    '''Клиент для работы с API Timeweb Cloud

    Attributes:
        account (AccountAPI): API для работы с аккаунтом.
        tokens (TokensAPI): API для работы с токенами.
        ssh_keys (SSHKeysAPI): API для работы с SSH ключами.
        images (ImagesAPI): API для работы с образами.
        s3 (BucketsAPI): API для работы с S3-хранилищами.
    '''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.

        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
        self.account = AccountAPI(token, client)
        self.tokens = TokensAPI(token, client)
        self.ssh_keys = SSHKeysAPI(token, client)
        self.images = ImagesAPI(token, client)
        self.s3 = BucketsAPI(token, client)
