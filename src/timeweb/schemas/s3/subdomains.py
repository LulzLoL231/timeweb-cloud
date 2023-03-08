# -*- coding: utf-8 -*-
'''Модели для работы с S3 трансфером'''
from enum import Enum
from datetime import datetime

from pydantic import Field

from ..base import ResponseWithMeta, BaseData


class DomainStatus(str, Enum):
    '''Статус SSL поддомена.

    Attributes:
        SSL_RELEASED (str): ssl_released
        SSL_NOT_REQUESTED (str): ssl_not_requested
        SSL_RE_RELEASE_ERROR (str): ssl_re_release_error
    '''
    SSL_RELEASED = 'ssl_released'
    SSL_NOT_REQUESTED = 'ssl_not_requested'
    SSL_RE_RELEASE_ERROR = 'ssl_re_release_error'


class Domain(BaseData):
    '''Модель SSL поддомена.

    Attributes:
        id (int): ID поддомена
        subdomain (str): Поддомен
        cert_released (datetime): Дата выдачи сертификата
        tries (int): Количество попыток перевыпустить SSL сертификат
        status (DomainStatus): Статус SSL поддомена
    '''
    id: int = Field(..., description='ID поддомена')
    subdomain: str = Field(..., description='Поддомен')
    cert_released: datetime = Field(
        ..., description='Дата выдачи сертификата'
    )
    tries: int = Field(
        ..., description='Количество попыток перевыпустить SSL сертификат'
    )
    status: DomainStatus = Field(
        ..., description='Статус SSL поддомена'
    )


class DomainsArray(ResponseWithMeta):
    '''Модель ответа списка поддоменов.

    Attributes:
        subdomains (list[Domain]): Список поддоменов
    '''
    subdomains: list[Domain] = Field(..., description='Список поддоменов')


class DomainAddStatus(str, Enum):
    '''Статус добавления поддомена.

    Attributes:
        SUCCESS (str): success
        EMPTY_CNAME (str): empty_cname
        DUPLICATE (str): duplicate
        FAILED (str): failed
    '''
    SUCCESS = 'success'
    EMPTY_CNAME = 'empty_cname'
    DUPLICATE = 'duplicate'
    FAILED = 'failed'


class DomainAdd(BaseData):
    '''Модель добавления поддомена.

    Attributes:
        subdomain (str): Поддомен
        status (DomainAddStatus): Результат добавления
    '''
    subdomain: str = Field(..., description='Поддомен')
    status: DomainAddStatus = Field(..., description='Результат добавления')


class DomainsAddArray(ResponseWithMeta):
    '''Модель ответа добавления поддоменов.

    Attributes:
        subdomains (list[DomainAdd]): Список поддоменов
    '''
    subdomains: list[DomainAdd] = Field(..., description='Список поддоменов')
