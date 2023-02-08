# -*- coding: utf-8 -*-
'''Модели для работы с S3 объектами'''
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta


class ObjectType(str, Enum):
    '''Тип объекта'''
    FILE = 'file'
    DIRECTORY = 'directory'


class ObjectOwner(BaseModel):
    '''Модель владельца объекта'''
    id: str = Field(..., description='ID владельца')
    display_name: str = Field(..., description='Имя владельца')


class Object(BaseModel):
    '''Модель объекта'''
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
    '''Модель ответа списка объектов'''
    files: list[Object] = Field(..., description='Список объектов')
