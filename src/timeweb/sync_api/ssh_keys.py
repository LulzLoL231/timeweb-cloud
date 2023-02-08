# -*- coding: utf-8 -*-
'''Методы API для работы с SSH ключами.

Для безопасного подключения к облачным серверам вы можете использовать SSH-ключи.
Их удобно сохранять в панели управления в разделе SSH-ключи, чтобы использовать при создании новых серверов.

Документация: https://timeweb.cloud/api-docs#tag/SSH-klyuchi'''
import logging

from httpx import Client

from .base import BaseClient
from ..schemas import ssh_keys as schemas


class SSHKeysAPI(BaseClient):
    '''Клиент для работы с API ssh-ключей Timeweb Cloud'''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    def get_keys(self) -> schemas.SSHKeysArray:
        '''Получение списка SSH-ключей.

        Returns:
            schemas.SSHKeysArray: Список SSH-ключей.
        '''
        keys = self._request('GET', '/ssh-keys')
        return schemas.SSHKeysArray(**keys.json())

    def create(
        self, name: str, body: str, is_default: bool
    ) -> schemas.CreateSSHKeyResponse:
        '''Создание SSH-ключа.

        Args:
            name (str): Название ключа.
            body (str): Тело ключа.
            is_default (bool): Установить ключ по умолчанию.

        Returns:
            schemas.CreateSSHKeyResponse: Созданный SSH-ключ.
        '''
        key = self._request(
            'POST',
            '/ssh-keys',
            json={
                'name': name,
                'body': body,
                'is_default': is_default,
            },
        )
        return schemas.CreateSSHKeyResponse(**key.json())

    def get(self, ssh_key_id: int) -> schemas.SSHKeyResponse:
        '''Получение SSH-ключа.

        Args:
            ssh_key_id (int): ID SSH-ключа.

        Returns:
            schemas.SSHKeyResponse: SSH-ключ.
        '''
        key = self._request('GET', f'/ssh-keys/{ssh_key_id}')
        return schemas.SSHKeyResponse(**key.json())

    def update(
        self,
        ssh_key_id: int,
        name: str | None = None,
        body: str | None = None,
        is_default: bool | None = None,
    ) -> schemas.SSHKeyResponse:
        '''Обновление SSH-ключа.

        Args:
            ssh_key_id (int): ID SSH-ключа.
            name (str | None, optional): Название ключа. Defaults to None.
            body (str | None, optional): Тело ключа. Defaults to None.
            is_default (bool | None, optional): Установить ключ по умолчанию. Defaults to None.

        Returns:
            schemas.SSHKeyResponse: Обновленный SSH-ключ.
        '''
        key = self._request(
            'PATCH',
            f'/ssh-keys/{ssh_key_id}',
            json={
                'name': name,
                'body': body,
                'is_default': is_default,
            },
        )
        return schemas.SSHKeyResponse(**key.json())

    def delete(self, ssh_key_id: int) -> bool:
        '''Удаление SSH-ключа.

        Args:
            ssh_key_id (int): ID SSH-ключа.

        Returns:
            bool: Успешность удаления.
        '''
        self._request('DELETE', f'/ssh-keys/{ssh_key_id}')
        return True

    def add_to_server(self, server_id: int, ssh_key_ids: list[int]) -> bool:
        '''Добавление SSH-ключей к серверу.

        Args:
            server_id (int): ID сервера.
            ssh_key_ids (list[int]): ID SSH-ключей.

        Returns:
            bool: Успешность добавления.
        '''
        self._request(
            'POST',
            f'/servers/{server_id}/ssh-keys',
            json={'ssh_key_ids': ssh_key_ids},
        )
        return True

    def delete_from_server(self, server_id: int, ssh_key_id: int) -> bool:
        '''Удаление SSH-ключа с сервера.

        Args:
            server_id (int): ID сервера.
            ssh_key_id (int): ID SSH-ключа.

        Returns:
            bool: Успешность удаления.
        '''
        self._request(
            'DELETE',
            f'/servers/{server_id}/ssh-keys/{ssh_key_id}',
        )
        return True
