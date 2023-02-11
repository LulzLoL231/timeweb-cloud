# -*- coding: utf-8 -*-
'''Модели для работы с доп. услугами выделенных серверов'''
from enum import Enum
from pydantic import BaseModel, Field

from ...time_utils import Period
from ...base import ResponseWithMeta


class ServicePeriods(Enum):
    '''Периоды доп. услуг'''
    P1D = Period('P1D')
    P1M = Period('P1M')
    P3M = Period('P3M')
    P6M = Period('P6M')
    P1Y = Period('P1Y')
    FOREVER = 'forever'


class DedicatedServerService(BaseModel):
    '''Доп. услуга выделенного сервера'''
    id: int = Field(..., description='UID доп. услуги.')
    price: int = Field(..., description='Цена доп. услуги в рублях.')
    period: ServicePeriods = Field(..., description='Период доп. услуги.')
    description: str = Field(..., description='Описание доп. услуги.')
    short_description: str = Field(..., description='Краткое описание доп. услуги.')
    name: str = Field(..., description='Название доп. услуги.')


class DedicatedServerServices(ResponseWithMeta):
    '''Массив доп. услуг выделенных серверов'''
    dedicated_server_additional_services: list[DedicatedServerService] = Field(
        ..., description='Массив доп. услуг выделенных серверов.'
    )
