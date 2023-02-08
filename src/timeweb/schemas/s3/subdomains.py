# -*- coding: utf-8 -*-
'''Модели для работы с S3 трансфером'''
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from ..base import ResponseWithMeta


class DomainStatus(str, Enum):
    '''Статус SSL поддомена'''
    SSL_RELEASED = 'ssl_released'
    SSL_NOT_REQUESTED = 'ssl_not_requested'
    SSL_RE_RELEASE_ERROR = 'ssl_re_release_error'


class Domain(BaseModel):
    '''Модель SSL поддомена'''
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
    '''Модель ответа списка поддоменов'''
    subdomains: list[Domain] = Field(..., description='Список поддоменов')


class DomainAddStatus(str, Enum):
    '''Статус добавления поддомена'''
    SUCCESS = 'success'
    EMPTY_CNAME = 'empty_cname'
    DUPLICATE = 'duplicate'
    FAILED = 'failed'


class DomainAdd(BaseModel):
    '''Модель добавления поддомена'''
    subdomain: str = Field(..., description='Поддомен')
    status: DomainAddStatus = Field(..., description='Результат добавления')


class DomainsAddArray(ResponseWithMeta):
    '''Модель ответа добавления поддоменов'''
    subdomains: list[DomainAdd] = Field(..., description='Список поддоменов')
