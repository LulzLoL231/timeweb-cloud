# -*- coding: utf-8 -*-
'''Модели для работы с тарифами выделенных серверов'''
from pydantic import BaseModel, Field

from ...base import ResponseWithMeta


class DedicatedCPU(BaseModel):
    '''CPU выделенного сервера'''
    description: str = Field(..., description='Описание характеристик.')
    description_short: str = Field(
        ..., description='Краткое описание CPU.'
    )
    count: int = Field(..., description='Количество ядер CPU.')


class DedicatedDisk(BaseModel):
    '''Диск выделенного сервера'''
    description: str = Field(..., description='Описание характеристик.')
    count: int = Field(..., description='Количество дисков.')


class DedicatedMemory(BaseModel):
    '''Память выделенного сервера'''
    description: str = Field(..., description='Описание характеристик.')
    count: int = Field(..., description='Количество памяти.')
    size: int = Field(..., description='Размер памяти (Мб).')


class DedicatedServerPreset(BaseModel):
    '''Тариф выделенного сервера'''
    id: int = Field(..., description='UID тарифа.')
    description: str = Field(..., description='Описание тарифа.')
    is_ipmi_enabled: bool = Field(..., description='IPMI доступен.')
    price: int | None = Field(
        None, description='Цена тарифа.'
    )
    location: str = Field(..., description='Локация тарифа.')
    memory: DedicatedMemory = Field(..., description='Память.')
    disk: DedicatedDisk = Field(..., description='Диск.')
    cpu: DedicatedCPU = Field(..., description='CPU.')


class DedicatedServerPresets(ResponseWithMeta):
    '''Массив тарифов выделенных серверов'''
    dedicated_servers_presets: list[DedicatedServerPreset] = Field(
        ..., description='Массив тарифов выделенных серверов.'
    )
