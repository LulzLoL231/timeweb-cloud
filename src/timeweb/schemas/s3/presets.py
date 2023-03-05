# -*- coding: utf-8 -*-
'''Модели для работы с S3 тарифами'''
from pydantic import Field

from ..base import ResponseWithMeta, BaseData


class Preset(BaseData):
    '''Модель тарифа S3-хранилища'''
    id: int = Field(..., description='ID тарифа')
    description: str = Field(..., description='Описание тарифа')
    description_short: str = Field(
        ..., description='Краткое описание тарифа'
    )
    disk: int = Field(..., description='Описание диска тарифа')
    price: int = Field(..., description='Цена тарифа')
    location: str = Field(..., description='Регион тарифа')


class StoragePresets(ResponseWithMeta):
    '''Модель ответа со списком тарифов S3-хранилищ'''
    storages_presets: list[Preset]
