# -*- coding: utf-8 -*-
'''Методы API для работы с API S3-хранилищ

S3-хранилище — это универсальное объектное хранилище, совместимое с Amazon S3 API,
в котором можно размещать любые типы статических данных.

Документация: https://timeweb.cloud/api-docs#tag/S3-hranilishe'''
import logging

from httpx import Client

from .base import BaseClient
from ..schemas import s3 as schemas


class BucketsAPI(BaseClient):
    '''Клиент для работы с API S3-хранилищ Timeweb Cloud'''

    def __init__(self, token: str, client: Client | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (Client | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    def get_buckets(self) -> schemas.BucketArray:
        '''Получение списка S3-хранилищ'''
        buckets = self._request('GET', '/storages/buckets')
        return schemas.BucketArray(**buckets.json())

    def create(
        self, name: str, type: schemas.BucketType | str,
        preset_id: int
    ) -> schemas.BucketResponse:
        '''Создание S3-хранилища
        Args:
            name (str): Название хранилища.
            type (schemas.BucketType | str): Тип хранилища.
            preset_id (int): ID пресета.
        '''
        bucket = self._request(
            'POST',
            '/storages/buckets',
            json={
                'name': name,
                'type': type,
                'preset_id': preset_id
            }
        )
        return schemas.BucketResponse(**bucket.json())

    def delete(self, bucket_id: int) -> bool:
        '''Удаление S3-хранилища
        Args:
            bucket_id (int): ID хранилища.
        '''
        self._request('DELETE', f'/storages/buckets/{bucket_id}')
        return True

    def update(
        self, bucket_id: int, preset_id: int | None = None,
        bucket_type: schemas.BucketType | str | None = None,
    ) -> schemas.BucketResponse:
        '''Обновление S3-хранилища
        Args:
            bucket_id (int): ID хранилища.
            preset_id (int | None, optional): ID пресета. Defaults to None.
            bucket_type (schemas.BucketType | str | None, optional): Тип хранилища. Defaults to None.
        '''
        data: dict[str, str | int | schemas.BucketType] = {}
        if preset_id is not None:
            data['preset_id'] = preset_id
        if bucket_type is not None:
            data['type'] = bucket_type
        bucket = self._request(
            'PATCH',
            f'/storages/buckets/{bucket_id}',
            json=data
        )
        return schemas.BucketResponse(**bucket.json())

    def get_storages_preset(self) -> schemas.StoragePresets:
        '''Получение списка пресетов хранилищ'''
        presets = self._request('GET', '/presets/storages')
        return schemas.StoragePresets(**presets.json())

    def get_storages_users(self) -> schemas.StorageUsers:
        '''Получение списка пользователей хранилищ'''
        users = self._request('GET', '/storages/users')
        return schemas.StorageUsers(**users.json())

    def set_user_secret_key(
        self, user_id: int, secret_key: str
    ) -> schemas.UserResponse:
        user = self._request(
            'PATCH',
            f'/storages/users/{user_id}',
            json={'secret_key': secret_key}
        )
        return schemas.UserResponse(**user.json())

    def get_transfer_status(
        self, bucket_id: int
    ) -> schemas.TransferResponse:
        '''Получение статуса переноса хранилища от стороннего S3 в Timeweb Cloud.

        Args:
            bucket_id (int): ID хранилища.

        Returns:
            schemas.TransferResponse: Статус переноса данных.
        '''
        transfer = self._request(
            'GET',
            f'/storages/buckets/{bucket_id}/transfer-status'
        )
        return schemas.TransferResponse(**transfer.json())

    def transfer(
        self, access_key: str, secret_key: str, location: str,
        is_force_path_style: str, endpoint: str, bucket_name: str,
        new_bucket_name: str
    ) -> bool:
        '''Перенос данных хранилища от стороннего S3 в Timeweb Cloud.

        Args:
            access_key (str): Идентификатор доступа стороннего s3 хранилища.
            secret_key (str): Пароль доступа стороннего s3 хранилища.
            location (str): Регион хранилища источника.
            is_force_path_style (str): Следует ли принудительно указывать URL-адреса для объектов S3.
            endpoint (str): URL s3 хранилища источника.
            bucket_name (str): Имя хранилища источника.
            new_bucket_name (str): Имя хранилища получателя.

        Returns:
            bool: True, если перенос успешно запущен.
        '''
        self._request(
            'POST',
            '/storages/transfer',
            json={
                'access_key': access_key,
                'secret_key': secret_key,
                'location': location,
                'is_force_path_style': is_force_path_style,
                'endpoint': endpoint,
                'bucket_name': bucket_name,
                'new_bucket_name': new_bucket_name
            }
        )
        return True

    def get_subdomains(self, bucket_id: int) -> schemas.DomainsArray:
        '''Получение списка поддоменов хранилища.

        Args:
            bucket_id (int): ID хранилища.

        Returns:
            schemas.DomainsArray: Список поддоменов.
        '''
        domains = self._request(
            'GET',
            f'/storages/buckets/{bucket_id}/subdomains'
        )
        return schemas.DomainsArray(**domains.json())

    def add_subdomains(
        self, bucket_id: int, subdomains: list[str]
    ) -> schemas.DomainsAddArray:
        '''Добавление поддоменов к хранилищу.

        Args:
            bucket_id (int): ID хранилища.
            subdomains (list[str]): Список поддоменов.

        Returns:
            schemas.DomainsAddArray: Список добавленных поддоменов.
        '''
        domains = self._request(
            'POST',
            f'/storages/buckets/{bucket_id}/subdomains',
            json={'subdomains': subdomains}
        )
        return schemas.DomainsAddArray(**domains.json())

    def delete_subdomains(
        self, bucket_id: int, subdomains: list[str]
    ) -> schemas.DomainsAddArray:
        '''Удаление поддоменов хранилища.

        Args:
            bucket_id (int): ID хранилища.
            subdomains (list[str]): Список поддоменов.

        Returns:
            schemas.DomainsAddArray: Список удаленных поддоменов.
        '''
        domains = self._request(
            'DELETE',
            f'/storages/buckets/{bucket_id}/subdomains',
            json={'subdomains': subdomains}
        )
        return schemas.DomainsAddArray(**domains.json())

    def get_objects_by_prefix(
        self, bucket_id: int, prefix: str | None = None,
        is_multipart: bool | None = None
    ) -> schemas.ObjectsArray:
        '''Получение списка объектов хранилища по префиксу.

        Args:
            bucket_id (int): ID хранилища.
            prefix (str | None): Префикс для поиска файла.
            is_multipart (bool | None): Обозначения multipart загрузки

        Example:
            >>> tw.s3.get_objects_by_prefix(1, prefix='test')

        Returns:
            schemas.ObjectsArray: Список объектов.
        '''
        params = {}
        if prefix is not None:
            params['prefix'] = prefix
        if is_multipart is not None:
            params['is_multipart'] = str(is_multipart).lower()
        objects = self._request(
            'GET',
            f'/storages/buckets/{bucket_id}/object-manager/list',
            params=params
        )
        return schemas.ObjectsArray(**objects.json())

    def rename_object(
        self, bucket_id: int, old_filename: str, new_filename: str
    ) -> bool:
        '''Переименование объекта.

        Args:
            bucket_id (int): ID хранилища.
            old_filename (str): Старое название файла или папки. Названия папок должны быть указаны с "/" в конце.
            new_filename (str): Новое название файла или папки. Названия папок должны быть указаны с "/" в конце.

        Returns:
            bool: True, если переименование успешно.
        '''
        self._request(
            'POST',
            f'/storages/buckets/{bucket_id}/object-manager/rename',
            json={'old_filename': old_filename, 'new_filename': new_filename}
        )
        return True

    def delete_object(
        self, bucket_id: int, is_multipart: bool, source: list[str]
    ) -> bool:
        '''Удаление объекта.

        Args:
            bucket_id (int): ID хранилища.
            is_multipart (bool): Обозначения multipart загрузки.
            source (list[str]): Список объектов для удаления.

        Returns:
            bool: True, если задание на удаление отправлено.
        '''
        self._request(
            'DELETE',
            f'/storages/buckets/{bucket_id}/object-manager/delete',
            json={'source': source}, params={'is_multipart': str(is_multipart).lower()}
        )
        return True

    def copy_object(
        self, bucket_id: int, destination: str, source: list[str]
    ) -> bool:
        '''Копирование объекта.

        Args:
            bucket_id (int): ID хранилища.
            destination (str): Путь копирования.
            source (list[str]): Список объектов для копирования.

        Returns:
            bool: True, если задание на копирование отправлено.
        '''
        self._request(
            'POST',
            f'/storages/buckets/{bucket_id}/object-manager/copy',
            json={'destination': destination, 'source': source}
        )
        return True

    def upload_object(
        self, bucket_id: int, path: str, filename: str, file: bytes
    ) -> bool:
        '''Загрузка объекта.

        Args:
            bucket_id (int): ID хранилища.
            path (str): Путь до директории в хранилище.
            filename (str): Название файла.
            file (bytes): Файл.

        Returns:
            bool: True, если файл успешно загружен.
        '''
        self._request(
            'POST',
            f'/storages/buckets/{bucket_id}/object-manager/upload',
            files={'files': (filename, file)},
            json={'path': path}
        )
        return True

    def make_dir(self, bucket_id: int, dir_name: str) -> bool:
        '''Создание директории.

        Args:
            bucket_id (int): ID хранилища.
            dir_name (str): Название директории.

        Returns:
            bool: True, если директория успешно создана.
        '''
        self._request(
            'POST',
            f'/storages/buckets/{bucket_id}/object-manager/mkdir',
            json={'dir_name': dir_name}
        )
        return True

    def add_subdomain_ssl(self, subdomain: str) -> bool:
        '''Добавление SSL сертификата для поддомена.

        Args:
            subdomain (str): Поддомен.

        Returns:
            bool: True, если SSL сертификат успешно добавлен.
        '''
        self._request(
            'POST',
            '/storages/certificates/generate',
            json={'subdomain': subdomain}
        )
        return True
