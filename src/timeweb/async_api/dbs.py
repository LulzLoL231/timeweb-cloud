# -*- coding: utf-8 -*-
'''Методы API для работы с API образов.

Облачная база данных, или База данных как сервис (DBaaS) —
облачное решение для хранения структурированных данных и управления ими.
DBaaS обеспечивает полностью автоматизированную, гибкую и масштабируемую
платформу для работы с базами данных.

Документация: https://timeweb.cloud/api-docs#tag/Bazy-dannyh'''
import logging

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import dbs as schemas


class DatabasesAPI(BaseAsyncClient):
    '''Клиент для работы с API базами данных Timeweb Cloud'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_databases(self) -> schemas.DBArray:
        '''Получить список баз данных.
        Returns:
            schemas.DBArray: Список баз данных.
        '''
        dbs = await self._request(
            'GET', '/dbs'
        )
        return schemas.DBArray(**dbs.json())

    async def create(
        self,
        password: str,
        name: str,
        type: schemas.DBType | str,
        preset_id: int,
        login: str | None = None,
        hash_type: schemas.DBHashType | str | None = None,
        config_parameters: schemas.DBConfigParameters | None = None
    ) -> schemas.DatabaseResponse:
        '''Создать базу данных.
        Args:
            password (str): Пароль для доступа к базе данных.
            name (str): Название базы данных.
            type (schemas.DBType | str): Тип базы данных.
            preset_id (int): ID пресета.
            login (str | None, optional): Логин для доступа к базе данных.
                Defaults to None.
            hash_type (schemas.DBHashType | str | None, optional): Тип хэша.
                Defaults to None.
            config_parameters (schemas.DBConfigParameters | None, optional):
                Параметры конфигурации. Defaults to None.
        Returns:
            schemas.DatabaseResponse: Ответ от API.
        '''
        data = {
            'password': password,
            'name': name,
            'type': type,
            'preset_id': preset_id
        }
        if login:
            data['login'] = login
        if hash_type:
            if isinstance(hash_type, schemas.DBHashType):
                data['hash_type'] = hash_type.value
            else:
                data['hash_type'] = hash_type
        if config_parameters:
            data['config_parameters'] = config_parameters.dict()
        db = await self._request(
            'POST', '/dbs', json=data
        )
        return schemas.DatabaseResponse(**db.json())

    async def get(self, db_id: int) -> schemas.DatabaseResponse:
        '''Получить информацию о базе данных.

        Args:
            db_id (int): ID базы данных.

        Returns:
            schemas.DatabaseResponse: Ответ от API.
        '''
        db = await self._request(
            'GET', f'/dbs/{db_id}'
        )
        return schemas.DatabaseResponse(**db.json())

    async def update(
        self,
        db_id: int,
        password: str | None = None,
        name: str | None = None,
        preset_id: int | None = None,
        config_parameters: schemas.DBConfigParameters | None = None,
        is_external_ip: bool | None = None
    ) -> schemas.DatabaseResponse:
        '''Обновить базу данных.
        Args:
            db_id (int): ID базы данных.
            password (str | None, optional): Пароль для доступа к базе данных.
                Defaults to None.
            name (str | None, optional): Название базы данных. Defaults to None.
            preset_id (int | None, optional): ID пресета. Defaults to None.
            config_parameters (schemas.DBConfigParameters | None, optional):
                Параметры конфигурации. Defaults to None.
            is_external_ip (bool | None, optional): Внешний IP. Defaults to None.
        Returns:
            schemas.DatabaseResponse: Ответ от API.
        '''
        data: dict[str, str | int | dict] = {}
        if password:
            data['password'] = password
        if name:
            data['name'] = name
        if preset_id:
            data['preset_id'] = preset_id
        if config_parameters:
            data['config_parameters'] = config_parameters.dict()
        if is_external_ip is not None:
            data['is_external_ip'] = str(is_external_ip).lower()
        db = await self._request(
            'PATCH', f'/dbs/{db_id}', json=data
        )
        return schemas.DatabaseResponse(**db.json())

    async def delete(self, db_id: int) -> bool:
        '''Удалить базу данных.

        Args:
            db_id (int): ID базы данных.

        Returns:
            bool: True, если база данных успешно удалена.
        '''
        await self._request(
            'DELETE', f'/dbs/{db_id}'
        )
        return True

    async def get_backups(
        self, db_id: int, limit: int = 100, offset: int = 0
    ) -> schemas.BackupArray:
        '''Получить список бэкапов базы данных.

        Args:
            db_id (int): ID базы данных.
            limit (int, optional): Лимит. Defaults to 100.
            offset (int, optional): Смещение. Defaults to 0.

        Returns:
            schemas.BackupArray: Ответ от API.
        '''
        backups = await self._request(
            'GET', f'/dbs/{db_id}/backups', params={
                'limit': limit,
                'offset': offset
            }
        )
        return schemas.BackupArray(**backups.json())

    async def create_backup(self, db_id: int) -> schemas.BackupResponse:
        '''Создать бэкап базы данных.

        Args:
            db_id (int): ID базы данных.

        Returns:
            schemas.BackupResponse: Ответ от API.
        '''
        backup = await self._request(
            'POST', f'/dbs/{db_id}/backups'
        )
        return schemas.BackupResponse(**backup.json())

    async def delete_backup(self, db_id: int, backup_id: int) -> bool:
        '''Удалить бэкап базы данных.

        Args:
            db_id (int): ID базы данных.
            backup_id (int): ID бэкапа.

        Returns:
            bool: True, если бэкап успешно удален.
        '''
        await self._request(
            'DELETE', f'/dbs/{db_id}/backups/{backup_id}'
        )
        return True

    async def get_backup(self, db_id: int, backup_id: int) -> schemas.BackupResponse:
        '''Получить информацию о бэкапе базы данных.

        Args:
            db_id (int): ID базы данных.
            backup_id (int): ID бэкапа.

        Returns:
            schemas.BackupResponse: Ответ от API.
        '''
        backup = await self._request(
            'GET', f'/dbs/{db_id}/backups/{backup_id}'
        )
        return schemas.BackupResponse(**backup.json())

    async def recover_from_backup(self, db_id: int, backup_id: int) -> bool:
        '''Восстановить базу данных из бэкапа.

        Args:
            db_id (int): ID базы данных.
            backup_id (int): ID бэкапа.

        Returns:
            bool: True, если база данных успешно восстановлена.
        '''
        await self._request(
            'PUT', f'/dbs/{db_id}/backups/{backup_id}'
        )
        return True

    async def get_presets(self) -> schemas.PresetArray:
        '''Получить список пресетов.

        Returns:
            schemas.PresetArray: Ответ от API.
        '''
        presets = await self._request(
            'GET', '/presets/dbs'
        )
        return schemas.PresetArray(**presets.json())
