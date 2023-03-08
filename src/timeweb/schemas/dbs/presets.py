# -*- coding: utf-8 -*-
'''Модели для работы с тарифами баз данных'''
from decimal import Decimal

from pydantic import Field

from .dbs import DBType
from ..base import ResponseWithMeta, BaseData


class Preset(BaseData):
    '''Тариф базы данных

    Attributes:
        id (int): ID тарифа.
        description (str): Описание тарифа.
        description_short (str): Краткое описание тарифа.
        cpu (int): Количество CPU.
        ram (int): Количество RAM (Гб).
        disk (int): Количество дискового пространства (Гб).
        type (DBType): Тип базы данных.
        price (Decimal): Цена тарифа.
        location (str): Географическое расположение тарифа.
    '''
    id: int = Field(..., description='ID тарифа.')
    description: str = Field(..., description='Описание тарифа.')
    description_short: str = Field(
        ..., description='Краткое описание тарифа.'
    )
    cpu: int = Field(..., description='Количество CPU.')
    ram: int = Field(..., description='Количество RAM (Гб).')
    disk: int = Field(...,
                      description='Количество дискового пространства (Гб).')
    type: DBType = Field(..., description='Тип базы данных.')
    price: Decimal = Field(..., description='Цена тарифа.')
    location: str = Field(...,
                          description='Географическое расположение тарифа.')


class PresetArray(ResponseWithMeta):
    '''Массив тарифов

    Attributes:
        databases_presets (list[Preset]): Массив тарифов.
    '''
    databases_presets: list[Preset] = Field(..., description='Массив тарифов.')
