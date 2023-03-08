# -*- coding: utf-8 -*-
'''Модели для работы с доп. услугами выделенных серверов'''
from enum import Enum
from pydantic import Field

from ...time_utils import Period
from ...base import ResponseWithMeta, BaseData


class ServicePeriods(Enum):
    '''Периоды доп. услуг.

    Attributes:
        P1D: 1 день
        P1M: 1 месяц
        P3M: 3 месяца
        P6M: 6 месяцев
        P1Y: 1 год
        FOREVER: Вечно
    '''
    P1D = Period('P1D')
    P1M = Period('P1M')
    P3M = Period('P3M')
    P6M = Period('P6M')
    P1Y = Period('P1Y')
    FOREVER = 'forever'


class DedicatedServerService(BaseData):
    '''Доп. услуга выделенного сервера.

    Attributes:
        id (int): UID доп. услуги.
        price (int): Цена доп. услуги в рублях.
        period (ServicePeriods): Период доп. услуги.
        description (str): Описание доп. услуги.
        short_description (str): Краткое описание доп. услуги.
        name (str): Название доп. услуги.
    '''
    id: int = Field(..., description='UID доп. услуги.')
    price: int = Field(..., description='Цена доп. услуги в рублях.')
    period: ServicePeriods = Field(..., description='Период доп. услуги.')
    description: str = Field(..., description='Описание доп. услуги.')
    short_description: str = Field(...,
                                   description='Краткое описание доп. услуги.')
    name: str = Field(..., description='Название доп. услуги.')


class DedicatedServerServices(ResponseWithMeta):
    '''Массив доп. услуг выделенных серверов.

    Attributes:
        dedicated_server_additional_services (list[DedicatedServerService]): Массив доп. услуг выделенных серверов.
    '''
    dedicated_server_additional_services: list[DedicatedServerService] = Field(
        ..., description='Массив доп. услуг выделенных серверов.'
    )
