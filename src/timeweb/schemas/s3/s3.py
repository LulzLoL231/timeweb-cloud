# -*- coding: utf-8 -*-
'''Модели для работы с S3'''
from enum import Enum

from pydantic import Field

from ..base import ResponseWithMeta, BaseResponse, BaseData, BaseDelete


class BucketStatus(str, Enum):
    '''Статус S3-хранилища.

    Attributes:
        NO_PAID (str): no_paid
        CREATED (str): created
        TRANSFER (str): transfer
    '''
    NO_PAID = 'no_paid'
    CREATED = 'created'
    TRANSFER = 'transfer'


class BucketType(str, Enum):
    '''Тип S3-хранилища.

    Attributes:
        PRIVATE (str): private
        PUBLIC (str): public
    '''
    PRIVATE = 'private'
    PUBLIC = 'public'


class BucketDiskStats(BaseData):
    '''Статистика диска S3-хранилища.

    Attributes:
        used (int): Использовано места (в Кб)
        size (int): Всего места (в Кб)
    '''
    used: int = Field(..., description='Использовано места (в Кб)')
    size: int = Field(..., description='Всего места (в Кб)')


class Bucket(BaseData):
    '''Модель S3-хранилища.

    Attributes:
        id (int): ID хранилища
        name (str): Имя хранилища
        dist_stats (BucketDiskStats): Статистика использования диска хранилища.
        type (BucketType): Тип хранилища
        preset_id (int | None): Идентификатор тарифа хранилища.
        status (BucketStatus): Статус хранилища
        object_amount (int): Количество объектов в хранилище.
        location (str): Регион хранилища
        hostname (str): Хост хранилища
        access_key (str): Ключ доступа к хранилищу
        secret_key (str): Секретный ключ доступа к хранилищу
    '''
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
    secret_key: str = Field(...,
                            description='Секретный ключ доступа к хранилищу')


class BucketResponse(BaseResponse):
    '''Модель ответа с S3-хранилищем.

    Attributes:
        bucket (Bucket): Хранилище.
    '''
    bucket: Bucket


class BucketArray(ResponseWithMeta):
    '''Модель ответа со списком S3-хранилищ.

    Attributes:
        buckets (list[Bucket]): Список хранилищ
    '''
    buckets: list[Bucket]


class BucketDelete(BaseResponse):
    '''Ответ с хэшом для подтверждения удаления S3-хранилища.

    Attributes:
        bucket_delete (BaseDelete): Хэш для удаления.
    '''
    bucket_delete: BaseDelete
