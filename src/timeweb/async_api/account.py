# -*- coding: utf-8 -*-
'''Методы API для работы с аккаунтом.

Группа методов, которая позволяет получить информацию о вашем текущем аккаунте. Обратите внимание, что API предоставляет только базовый функционал для получения общей информации об аккаунте.

Все методы возвращают объекты, которые можно преобразовать в JSON с помощью метода json().

Документация: https://timeweb.cloud/api-docs#tag/Akkaunt'''
import logging
from ipaddress import IPv4Address

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import account as schemas


class AccountAPI(BaseAsyncClient):
    '''Клиент для работы с API аккаунта Timeweb Cloud'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_finances(self) -> schemas.AccountFinances:
        '''Получение информации о платежной информации.

        Returns:
            AccountFinances: Платежная информация.
        '''
        method = 'GET'
        url = '/account/finances'
        data = await self._request(method, url)
        return schemas.AccountFinances(**data.json())

    async def get_status(self) -> schemas.AccountStatus:
        '''Получение информации о статусе аккаунта.

        Returns:
            AccountStatus: Статус аккаунта.
        '''
        method = 'GET'
        url = '/account/status'
        data = await self._request(method, url)
        return schemas.AccountStatus(**data.json())

    async def get_access_restrictions(self) -> schemas.AccountAccess:
        '''Получение информации об ограничениях авторизации пользователя.

        Returns:
            AccountAccess: Информации об ограничениях авторизации пользователя.
        '''
        method = 'GET'
        url = '/auth/access'
        data = await self._request(method, url)
        return schemas.AccountAccess(**data.json())

    async def turn_countries_restrictions(self, enabled: bool) -> bool:
        '''Включение/отключение ограничений по странам.

        Args:
            enabled (bool): Включить/выключить.

        Returns:
            bool: Успешность выполнения.
        '''
        method = 'POST'
        url = '/auth/access/countries/enabled'
        await self._request(method, url, json={'is_enabled': enabled})
        return True

    async def get_countries(self) -> schemas.AccessCountries:
        '''Получение списка стран.

        Returns:
            AccessCountries: Список стран.
        '''
        method = 'GET'
        url = '/auth/access/countries'
        data = await self._request(method, url)
        return schemas.AccessCountries(**data.json())

    async def add_allowed_countries(self, countries: list[str]) -> schemas.AddAccessCountries:
        '''Добавление разрешенных стран.

        Args:
            countries (list[str]): Список стран.

        Returns:
            AccessCountries: Список стран.
        '''
        method = 'POST'
        url = '/auth/access/countries'
        data = await self._request(method, url, json={'countries': countries})
        return schemas.AddAccessCountries(**data.json())

    async def remove_allowed_countries(self, countries: list[str]) -> schemas.RemoveAccessCountries:
        '''Удаление разрешенных стран.

        Args:
            countries (list[str]): Список стран.

        Returns:
            RemoveAccessCountries: Список стран.
        '''
        method = 'DELETE'
        url = '/auth/access/countries'
        data = await self._request(method, url, json={'countries': countries})
        return schemas.RemoveAccessCountries(**data.json())

    async def turn_ips_restrictions(self, enabled: bool) -> bool:
        '''Включение/отключение ограничений по IP.

        Args:
            enabled (bool): Включить/выключить.

        Returns:
            bool: Успешность выполнения.
        '''
        method = 'POST'
        url = '/auth/access/ips/enabled'
        await self._request(method, url, json={'is_enabled': enabled})
        return True

    async def add_allowed_ips(self, ips: list[str | IPv4Address]) -> schemas.AddIP:
        '''Добавление разрешенных IP.

        Args:
            ips (list[str | IPv4Address]): Список IP.

        Returns:
            AddIP: Список IP.
        '''
        method = 'POST'
        url = '/auth/access/ips'
        data = await self._request(method, url, json={'ips': ips})
        return schemas.AddIP(**data.json())

    async def remove_allowed_ips(self, ips: list[str | IPv4Address]) -> schemas.RemoveIP:
        '''Удаление разрешенных IP.

        Args:
            ips (list[str | IPv4Address]): Список IP.

        Returns:
            RemoveIP: Список IP.
        '''
        method = 'DELETE'
        url = '/auth/access/ips'
        data = await self._request(method, url, json={'ips': ips})
        return schemas.RemoveIP(**data.json())
