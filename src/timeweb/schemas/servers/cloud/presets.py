# -*- coding: utf-8 -*-
'''Модели для работы с тарифами облачного сервера'''
from decimal import Decimal

from ...base import ResponseWithMeta, BaseData


class CloudPreset(BaseData):
    '''Тариф облачного сервера.

    Attributes:
        id (int): Уникальный идентификатор тарифа сервера.
        location (str): Локация сервера.
        price (Decimal): Стоимость в рублях.
        cpu (int): Количество ядер процессора.
        cpu_frequency (str): Частота процессора.
        ram (int): Количество (в Мб) оперативной памяти.
        disk (int): Размер диска (в Мб).
        disk_type (str): Тип диска.
        bandwidth (int): Пропускная способность тарифа.
        description (str): Описание тарифа.
        description_short (str): Короткое описание тарифа.
        is_allowed_local_network (bool): Есть возможность подключения локальной сети
        tags (list[str]): Список тегов тарифа.
    '''
    id: int
    location: str
    price: Decimal
    cpu: int
    cpu_frequency: str
    ram: int
    disk: int
    disk_type: str
    bandwidth: int
    description: str
    description_short: str
    is_allowed_local_network: bool
    tags: list[str]


class CloudPresetsResponse(ResponseWithMeta):
    '''Ответ со списком тарифов облачного сервера.

    Attributes:
        server_presets (list[CloudPreset]): Список тарифов.
    '''
    server_presets: list[CloudPreset]
