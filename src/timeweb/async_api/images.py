# -*- coding: utf-8 -*-
'''Методы API для работы с API образов.

Образы — это полная копия вашего облачного сервера в формате Qcow2,
со всеми настройками операционной системы, программного обеспечения
и всем содержимым сервера.

Документация: https://timeweb.cloud/api-docs#tag/Obrazy'''
import logging
from uuid import UUID
from datetime import datetime

from httpx import AsyncClient

from .base import BaseAsyncClient
from ..schemas import images as schemas


class ImagesAPI(BaseAsyncClient):
    '''Клиент для работы с API образов Timeweb Cloud'''

    def __init__(self, token: str, client: AsyncClient | None = None):
        '''Инициализация клиента.
        Args:
            token (str): API токен.
            client (AsyncClient | None, optional): HTTPX клиент. Defaults to None.
        '''
        super().__init__(token, client)
        self.log = logging.getLogger('timeweb')

    async def get_images(self, limit: int = 100, offset: int = 0) -> schemas.ImagesArray:
        '''Получение списка образов.

        Args:
            limit (int, optional): Количество элементов на странице. Defaults to 100.
            offset (int, optional): Смещение от начала списка. Defaults to 0.

        Returns:
            ImagesArray: Список образов.
        '''
        images = await self._request(
            'GET', 'images',
            params={'limit': limit, 'offset': offset}
        )
        return schemas.ImagesArray(**images.json())

    async def create(self, description: str, disk_id: int) -> schemas.ImageResponse:
        '''Создание образа.

        Args:
            description (str): Описание образа.
            disk_id (int): Идентификатор диска, для которого создается образ

        Returns:
            ImageResponse: Информация о созданном образе.
        '''
        image = await self._request(
            'POST', 'images',
            json={'description': description, 'disk_id': disk_id}
        )
        return schemas.ImageResponse(**image.json())

    async def get_image(self, image_id: UUID | str) -> schemas.ImageResponse:
        '''Получение информации об образе.

        Args:
            image_id (UUID | str): Идентификатор образа.

        Returns:
            ImageResponse: Информация об образе.
        '''
        image = await self._request('GET', f'images/{image_id}')
        return schemas.ImageResponse(**image.json())

    async def delete(self, image_id: UUID | str) -> bool:
        '''Удаление образа.

        Args:
            image_id (UUID | str): Идентификатор образа.

        Returns:
            bool: True, если образ успешно удален.
        '''
        await self._request('DELETE', f'images/{image_id}')
        return True

    async def update(self, image_id: UUID | str, description: str) -> schemas.ImageResponse:
        '''Обновление образа.

        Args:
            image_id (UUID | str): Идентификатор образа.
            description (str): Описание образа.

        Returns:
            ImageResponse: Информация об образе.
        '''
        image = await self._request(
            'PATCH', f'images/{image_id}',
            json={'description': description}
        )
        return schemas.ImageResponse(**image.json())

    async def get_download_urls(
        self, image_id: UUID | str, limit: int = 100, offset: int = 0
    ) -> schemas.DownloadsArray:
        '''Получение ссылок для скачивания образа.

        Args:
            image_id (UUID | str): Идентификатор образа.
            limit (int, optional): Количество элементов на странице. Defaults to 100.
            offset (int, optional): Смещение от начала списка. Defaults to 0.

        Returns:
            DownloadsArray: Список ссылок для скачивания образа.
        '''
        downloads = await self._request(
            'GET', f'images/{image_id}/download-url',
            params={'limit': limit, 'offset': offset}
        )
        return schemas.DownloadsArray(**downloads.json())

    async def create_download_url(
        self, image_id: UUID | str, type: schemas.URLType | str,
        filename: str, access_token: str,
        refresh_token: str | None = None,
        expiry: datetime | None = None,
        token_type: str = 'Bearer'
    ) -> schemas.DownloadResponse:
        '''Создание ссылки для скачивания образа.

        Args:
            image_id (UUID | str): Идентификатор образа.
            type (URLType | str): Тип ссылки.
            filename (str): Имя файла для загрузки в облачное хранилище.
            access_token (str): Токен доступа к API облачного хранилища.
            refresh_token (str, optional): Токен обновления доступов к API. Defaults to None.
            expiry (datetime, optional): Время истечения токена. Defaults to None.
            token_type (str, optional): Тип токена. Defaults to 'Bearer'.

        Returns:
            DownloadResponse: Информация о созданной ссылке.
        '''
        auth_data = {
            'access_token': access_token,
        }
        data: dict[str, str | dict] = {
            'filename': filename,
        }
        if isinstance(type, schemas.URLType):
            data['type'] = type.value
        else:
            data['type'] = type
        if refresh_token:
            auth_data['refresh_token'] = refresh_token
        if expiry:
            auth_data['expiry'] = expiry.isoformat()
        if token_type:
            auth_data['token_type'] = token_type
        data['auth'] = auth_data
        download = await self._request(
            'POST', f'images/{image_id}/download-url',
            json=data
        )
        return schemas.DownloadResponse(**download.json())

    async def get_image_download_url(
        self, image_id: UUID | str, image_url_id: UUID | str
    ) -> schemas.DownloadResponse:
        '''Получение ссылки для скачивания образа.

        Args:
            image_id (UUID | str): Идентификатор образа.
            image_url_id (UUID | str): Идентификатор ссылки.

        Returns:
            DownloadResponse: Информация о ссылке.
        '''
        download = await self._request(
            'GET', f'images/{image_id}/download-url/{image_url_id}'
        )
        return schemas.DownloadResponse(**download.json())

    async def delete_image_download_url(
        self, image_id: UUID | str, image_url_id: UUID | str
    ) -> bool:
        '''Удаление ссылки для скачивания образа.

        Args:
            image_id (UUID | str): Идентификатор образа.
            image_url_id (UUID | str): Идентификатор ссылки.

        Returns:
            bool: Результат удаления.
        '''
        await self._request(
            'DELETE', f'images/{image_id}/download-url/{image_url_id}'
        )
        return True
