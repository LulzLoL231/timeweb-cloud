# -*- coding: utf-8 -*-
'''Модели для работы с S3 тарифами'''
from pydantic import BaseModel, Field

from ..base import ResponseWithMeta


class Preset(BaseModel):
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
