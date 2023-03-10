# -*- coding: utf-8 -*-
'''Модели для работы с дисками облачного сервера'''
from ...base import ResponseWithMeta, BaseData, BaseResponse


class ServerDisk(BaseData):
    '''Диск облачного сервера.

    Attributes:
        id (int): Уникальный идентификатор диска.
        size (int): Размер диска (в Мб).
        used (int): Количество использованной памяти диска (в Мб).
        type (str): Тип диска.
        is_mounted (bool): Является ли диск примонтированным.
        is_system (bool): Является ли диск системным.
        system_name (str): Системное название диска.
        status (str): Статус диска.
    '''
    id: int
    size: int
    used: int
    type: str
    is_mounted: bool
    is_system: bool
    system_name: str
    status: str


class ServerDisksResponse(ResponseWithMeta):
    '''Ответ со списком дисков сервера.

    Attributes:
        server_disks (list[ServerDisk]): Список дисков.
    '''
    server_disks: list[ServerDisk]


class ServerDiskResponse(BaseResponse):
    '''Ответ с диском сервера.

    Attributes:
        server_disk (ServerDisk): Диск сервера.
    '''
    server_disk: ServerDisk
