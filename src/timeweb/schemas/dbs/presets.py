# -*- coding: utf-8 -*-
'''Модели для работы с тарифами баз данных'''
from pydantic import BaseModel, Field

from .dbs import DBType
from ..base import ResponseWithMeta


class Preset(BaseModel):
    '''Тариф базы данных'''
    id: int = Field(..., description='ID тарифа.')
    description: str = Field(..., description='Описание тарифа.')
    description_short: str = Field(
        ..., description='Краткое описание тарифа.'
    )
    cpu: int = Field(..., description='Количество CPU.')
    ram: int = Field(..., description='Количество RAM (Гб).')
    disk: int = Field(..., description='Количество дискового пространства (Гб).')
    type: DBType = Field(..., description='Тип базы данных.')
    price: int = Field(..., description='Цена тарифа.')
    location: str = Field(...,
                          description='Географическое расположение тарифа.')


class PresetArray(ResponseWithMeta):
    '''Массив тарифов'''
    databases_presets: list[Preset] = Field(..., description='Массив тарифов.')
