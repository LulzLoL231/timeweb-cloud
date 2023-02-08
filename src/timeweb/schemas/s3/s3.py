# -*- coding: utf-8 -*-
'''Модели для работы с S3'''
from enum import Enum

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta, BaseResponse


class BucketStatus(str, Enum):
    '''Статус S3-хранилища'''
    NO_PAID = 'no_paid'
    CREATED = 'created'
    TRANSFER = 'transfer'


class BucketType(str, Enum):
    '''Тип S3-хранилища'''
    PRIVATE = 'private'
    PUBLIC = 'public'


class BucketDiskStats(BaseModel):
    '''Статистика диска S3-хранилища'''
    used: int = Field(..., description='Использовано места (в Кб)')
    size: int = Field(..., description='Всего места (в Кб)')


class Bucket(BaseModel):
    '''Модель S3-хранилища'''
    id: int = Field(..., description='ID хранилища')
    name: str = Field(..., description='Имя хранилища')
    dist_stats: BucketDiskStats = Field(
        ..., description='Статистика использования диска хранилища.'
    )
    type: BucketType = Field(..., description='Тип хранилища')
    preset_id: int | None = Field(
        None, description='Идентификатор тарифа хранилища.'
    )
    status: BucketStatus = Field(..., description='Статус хранилища')
    object_amount: int = Field(
        ..., description='Количество объектов в хранилище.'
    )
    location: str = Field(..., description='Регион хранилища')
    hostname: str = Field(..., description='Хост хранилища')
    access_key: str = Field(..., description='Ключ доступа к хранилищу')
    secret_key: str = Field(..., description='Секретный ключ доступа к хранилищу')


class BucketResponse(BaseResponse):
    '''Модель ответа с S3-хранилищем'''
    bucket: Bucket


class BucketArray(ResponseWithMeta):
    '''Модель ответа со списком S3-хранилищ'''
    buckets: list[Bucket]
