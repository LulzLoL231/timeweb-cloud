# -*- coding: utf-8 -*-
'''Методы API для работы с API токенами.

Токены API — это это JWT-токены с помощью которых вы можете получить доступ к управлению через API вашей облачной инфраструктурой.

Документация: https://timeweb.cloud/api-docs#tag/Tokeny-API'''
import logging
from uuid import UUID
from typing import Literal
from datetime import datetime

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import tokens as schemas


class TokensAPI(BaseAsyncClient):
    '''Клиент для работы с API токенами Timeweb Cloud'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_tokens(self) -> schemas.APIKeysResponse:
        '''Получение списка выпущенных API токенов.

        Returns:
            schemas.APIKeysResponse: Список API токенов.
        '''
        keys = await self._request('GET', '/auth/api-keys')
        return schemas.APIKeysResponse(**keys.json())

    async def create(self, name: str, expire: datetime | str) -> schemas.CreateAPIKeyResponse:
        '''Создание API токена.

        Args:
            name (str): Название токена.
            expire (datetime | str): Дата истечения токена.

        Returns:
            schemas.CreateAPIKeyResponse: Созданный токен.
        '''
        data = {
            'name': name
        }
        if isinstance(expire, datetime):
            data['expire'] = expire.isoformat()
        else:
            data['expire'] = expire
        key = await self._request('POST', '/auth/api-keys', json=data)
        return schemas.CreateAPIKeyResponse(**key.json())

    async def rename(self, token_id: UUID | str, name: str) -> schemas.APIKeyResponse:
        '''Переименование API токена.

        Args:
            token_id (UUID | str): ID токена.
            name (str): Новое название токена.

        Returns:
            schemas.APIKeyResponse: Измененный токен.
        '''
        key = await self._request('PATCH', f'/auth/api-keys/{token_id}', json={
            'name': name,
        })
        return schemas.APIKeyResponse(**key.json())

    async def reissue(
        self, token_id: UUID | str, expire: datetime | str | None = None
    ) -> schemas.CreateAPIKeyResponse:
        '''Перевыпуск API токена.

        Args:
            token_id (UUID | str): ID токена.
            expire (datetime | str | None, optional): Дата истечения токена. Defaults to None.

        Returns:
            schemas.CreateAPIKeyResponse: Перевыпущенный токен.
        '''
        data = {}
        if expire is not None:
            if isinstance(expire, datetime):
                data['expire'] = expire.isoformat()
            else:
                data['expire'] = expire
        key = await self._request('PUT', f'/auth/api-keys/{token_id}', json=data)
        return schemas.CreateAPIKeyResponse(**key.json())

    async def delete(self, token_id: UUID | str) -> Literal[True]:
        '''Удаление API токена.

        Args:
            token_id (UUID | str): ID токена.

        Returns:
            Literal[True]: Токен удалён.
        '''
        await self._request('DELETE', f'/auth/api-keys/{token_id}')
        return True
