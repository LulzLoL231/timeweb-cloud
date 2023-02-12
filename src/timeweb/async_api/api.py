# -*- coding: utf-8 -*-
'''Асинхронный клиент для Timeweb Cloud API'''
import logging

from httpx import AsyncClient

from .s3 import BucketsAPI
from .dbs import DatabasesAPI
from .tokens import TokensAPI
from .images import ImagesAPI
from .dedics import DedicsAPI
from .account import AccountAPI
from .ssh_keys import SSHKeysAPI
from .balancers import BalancersAPI


class Servers:
    '''API для работы с серверами.

    Attributes:
        dedics (DedicsAPI): API для работы с серверами.
    '''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация API.

        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        self.log = logging.getLogger('timeweb')
        self.dedics = DedicsAPI(token, client)


class AsyncTimeweb:
    '''Клиент для работы с API Timeweb Cloud

    Attributes:
        account (AccountAPI): API для работы с аккаунтом.
        tokens (TokensAPI): API для работы с токенами.
        ssh_keys (SSHKeysAPI): API для работы с SSH ключами.
        images (ImagesAPI): API для работы с образами.
        s3 (BucketsAPI): API для работы с S3-хранилищами.
        dbs (DatabasesAPI): API для работы с базами данных.
        servers (Servers): API для работы с серверами.
        balancers (BalancersAPI): API для работы с балансировщиками.
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
        self.images = ImagesAPI(token, client)
        self.s3 = BucketsAPI(token, client)
        self.dbs = DatabasesAPI(token, client)
        self.servers = Servers(token, client)
        self.balancers = BalancersAPI(token, client)
