# -*- coding: utf-8 -*-
'''Модели для работы с тарифами балансировщиков'''
from decimal import Decimal
from pydantic import Field

from ..base import ResponseWithMeta, BaseData


class BalancerPreset(BaseData):
    '''Тариф балансировщика

    Attributes:
        id (int): UID тарифа
        description (str): Описание тарифа
        description_short (str): Краткое описание тарифа
        bandwidth (int): Пропускная способность
        replica_count (int): Количество реплик
        request_per_second (str): Количество запросов в секунду
        price (Decimal): Цена тарифа
        location (str): Расположение тарифа
    '''
    id: int = Field(..., description='UID тарифа')
    description: str = Field(..., description='Описание тарифа')
    description_short: str = Field(..., description='Краткое описание тарифа')
    bandwidth: int = Field(..., description='Пропускная способность')
    replica_count: int = Field(..., description='Количество реплик')
    request_per_second: str = Field(...,
                                    description='Количество запросов в секунду')
    price: Decimal = Field(..., description='Цена тарифа')
    location: str = Field(..., description='Расположение тарифа')


class BalancerPresetsResponse(ResponseWithMeta):
    '''Список тарифов балансировщиков

    Attributes:
        balancers_presets (list[BalancerPreset]): Список тарифов балансировщиков
    '''
    balancers_presets: list[BalancerPreset] = Field(
        ..., description='Список тарифов балансировщиков')
