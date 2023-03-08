# -*- coding: utf-8 -*-
'''Модели для работы с тарифами выделенных серверов'''
from pydantic import Field

from ...base import ResponseWithMeta, BaseData


class DedicatedCPU(BaseData):
    '''CPU выделенного сервера.

    Attributes:
        description (str): Описание характеристик.
        description_short (str): Краткое описание CPU.
        count (int): Количество ядер CPU.
    '''
    description: str = Field(..., description='Описание характеристик.')
    description_short: str = Field(
        ..., description='Краткое описание CPU.'
    )
    count: int = Field(..., description='Количество ядер CPU.')


class DedicatedDisk(BaseData):
    '''Диск выделенного сервера.

    Attributes:
        description (str): Описание характеристик.
        count (int): Количество дисков.
    '''
    description: str = Field(..., description='Описание характеристик.')
    count: int = Field(..., description='Количество дисков.')


class DedicatedMemory(BaseData):
    '''Память выделенного сервера.

    Attributes:
        description (str): Описание характеристик.
        count (int): Количество памяти.
        size (int): Размер памяти (Мб).
    '''
    description: str = Field(..., description='Описание характеристик.')
    count: int = Field(..., description='Количество памяти.')
    size: int = Field(..., description='Размер памяти (Мб).')


class DedicatedServerPreset(BaseData):
    '''Тариф выделенного сервера.

    Attributes:
        id (int): UID тарифа.
        description (str): Описание тарифа.
        is_ipmi_enabled (bool): IPMI доступен.
        price (int | None): Цена тарифа.
        location (str): Локация тарифа.
        memory (DedicatedMemory): Память.
        disk (DedicatedDisk): Диск.
        cpu (DedicatedCPU): CPU.
    '''
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
    '''Массив тарифов выделенных серверов.

    Attributes:
        dedicated_servers_presets (list[DedicatedServerPreset]): Массив тарифов выделенных серверов.
    '''
    dedicated_servers_presets: list[DedicatedServerPreset] = Field(
        ..., description='Массив тарифов выделенных серверов.'
    )
