# -*- coding: utf-8 -*-
'''Модели для работы с тарифами балансировщиков'''
from pydantic import BaseModel, Field

from ..base import ResponseWithMeta


class BalancerPreset(BaseModel):
    '''Тариф балансировщика'''
    id: int = Field(..., description='UID тарифа')
    description: str = Field(..., description='Описание тарифа')
    description_short: str = Field(..., description='Краткое описание тарифа')
    bandwidth: int = Field(..., description='Пропускная способность')
    replica_count: int = Field(..., description='Количество реплик')
    request_per_second: str = Field(..., description='Количество запросов в секунду')
    price: int = Field(..., description='Цена тарифа')
    location: str = Field(..., description='Расположение тарифа')


class BalancerPresetsResponse(ResponseWithMeta):
    '''Список тарифов балансировщиков'''
    balancers_presets: list[BalancerPreset] = Field(..., description='Список тарифов балансировщиков')
