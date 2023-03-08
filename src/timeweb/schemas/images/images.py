# -*- coding: utf-8 -*-
'''Модели для работы с образами'''
from uuid import UUID
from enum import Enum
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData


class ImageStatus(str, Enum):
    '''Статус образа

    Attributes:
        NEW (str): new
        CREATED (str): created
        FAILED (str): failed
        DELETED (str): deleted
    '''
    NEW = 'new'
    CREATED = 'created'
    FAILED = 'failed'
    DELETED = 'deleted'


class Image(BaseData):
    '''Модель образа

    Attributes:
        id (UUID | str): Уникальный идентификатор образа.
        status (ImageStatus): Статус образа.
        created_at (datetime): Дата и время создания образа.
        deleted_at (datetime | None): Дата и время удаления
        size (int): Размер образа в мегабайтах.
        name (str): Имя образа
        description (str): Описание образа.
        disk_id (int): Идентификатор связанного с образом диска.
        location (str | None): Локация, в которой создан образ
        os (str): Операционная система образа
        progress (int): Процент создания образа
    '''
    id: UUID | str = Field(..., description='Уникальный идентификатор образа.')
    status: ImageStatus = Field(..., description='Статус образа.')
    created_at: datetime = Field(...,
                                 description='Дата и время создания образа.')
    deleted_at: datetime | None = None
    size: int = Field(..., description='Размер образа в мегабайтах.')
    name: str
    description: str = Field(..., description='Описание образа.')
    disk_id: int = Field(
        ..., description='Идентификатор связанного с образом диска.'
    )
    location: str | None = Field(
        None, description='Локация, в которой создан образ'
    )
    os: str
    progress: int


class ImagesArray(ResponseWithMeta):
    '''Модель ответа с массивом образов

    Attributes:
        images (list[Image]): Массив образов
    '''
    images: list[Image] = Field(..., description='Массив образов.')


class ImageResponse(BaseResponse):
    '''Модель ответа на создание образа

    Attributes:
        image (Image): образ
    '''
    image: Image = Field(..., description='Объект образа.')


class URLType(str, Enum):
    '''Тип URL

    Attributes:
        TIMEWEB (str): Timeweb Cloud
        GOOGLE_DRIVE (str): Google Drive
        YANDEX (str): Yandex Drive
    '''
    TIMEWEB = 'timeweb'
    GOOGLE_DRIVE = 'google_drive'
    YANDEX = 'yandex'


class URLStatus(str, Enum):
    '''Статус URL

    Attributes:
        PROCESS (str): process
        FAILED (str): failed
        FINISHED (str): finished
        ALREADY_EXISTS (str): already_exists
    '''
    PROCESS = 'process'
    FAILED = 'failed'
    FINISHED = 'finished'
    ALREADY_EXISTS = 'already_exists'


class Download(BaseData):
    '''Модель ссылки на загрузку

    Attributes:
        id (UUID | str): Уникальный идентификатор ссылки.
        created_at (datetime): Дата и время создания ссылки.
        image (UUID | str): Идентификатор образа.
        type (URLType): Тип ссылки.
        url (str): Ссылка на скачивание.
        status (URLStatus): Статус создания.
        progress (int): Процент создания образа
    '''
    id: UUID | str = Field(..., description='Уникальный идентификатор ссылки.')
    created_at: datetime = Field(
        ..., description='Дата и время создания ссылки.'
    )
    image: UUID | str = Field(..., description='Идентификатор образа.')
    type: URLType = Field(..., description='Тип ссылки.')
    url: str = Field(..., description='Ссылка на скачивание.')
    status: URLStatus = Field(..., description='Статус создания.')
    progress: int


class DownloadsArray(ResponseWithMeta):
    '''Модель ответа ссылок на загрузку

    Attributes:
        downloads (list[Download]): Массив ссылок.
    '''
    downloads: list[Download] = Field(..., description='Массив ссылок.')


class DownloadResponse(BaseResponse):
    '''Модель ответа на создание ссылки на загрузку

    Attributes:
        download (Download): Объект ссылки на загрузку.
    '''
    download: Download = Field(..., description='Объект ссылки на загрузку.')
