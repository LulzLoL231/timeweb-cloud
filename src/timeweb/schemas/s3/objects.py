# -*- coding: utf-8 -*-
'''Модели для работы с S3 объектами'''
from enum import Enum
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseData


class ObjectType(str, Enum):
    '''Тип объекта.

    Attributes:
        FILE (str): Файл
        DIRECTORY (str): Папка
    '''
    FILE = 'file'
    DIRECTORY = 'directory'


class ObjectOwner(BaseData):
    '''Модель владельца объекта.

    Attributes:
        id (str): ID владельца
        display_name (str): Имя владельца
    '''
    id: str = Field(..., description='ID владельца')
    display_name: str = Field(..., description='Имя владельца')


class Object(BaseData):
    '''Модель объекта.

    Attributes:
        key (str): Название объекта
        last_modified (datetime): Дата последнего изменения объекта
        etag (str | None): ETag объекта
        size (int | None): Размер объекта (в байтах)
        storage_class (str | None): Класс хранилища
        checksum_algorithm (str | None): Алгоритм вычисления контрольной суммы
        owner (ObjectOwner | None): Владелец объекта
        type (ObjectType): Тип объекта
    '''
    key: str = Field(..., description='Название объекта')
    last_modified: datetime = Field(
        ..., description='Дата последнего изменения объекта'
    )
    etag: str | None = Field(None, description='ETag объекта')
    size: int | None = Field(None, description='Размер объекта (в байтах)')
    storage_class: str | None = Field(
        None, description='Класс хранилища'
    )
    checksum_algorithm: str | None = Field(
        None, description='Алгоритм вычисления контрольной суммы'
    )
    owner: ObjectOwner | None = Field(None, description='Владелец объекта')
    type: ObjectType = Field(..., description='Тип объекта')


class ObjectsArray(ResponseWithMeta):
    '''Модель ответа списка объектов.

    Attributes:
        files (list[Object]): Список объектов
    '''
    files: list[Object] = Field(..., description='Список объектов')
