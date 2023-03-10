# -*- coding: utf-8 -*-
'''Модели для работы с ПО из маркетплейса облачных серверов'''
from ...base import ResponseWithMeta, BaseData


class SoftwareRequirements(BaseData):
    '''Требования для устнановки ПО.

    Attributes:
        cpu_min (int): Минимальной значение процессора.
        disk_min (int): Минимальное значение диска.
        ram_min (int): Минимальное значение оперативной памяти.
        bandwidth_min (int): Минимальное значение пропускной способности.
    '''
    cpu_min: int
    disk_min: int
    ram_min: int
    bandwidth_min: int


class ServersSoftware(BaseData):
    '''ПО из маркетплейса для сервера.

    Attributes:
        id (int): Уникальный идентификатор ПО из маркетплейса.
        name (str): Имя ПО из маркетплейса.
        os_ids (list[int]): Список id операционных систем, на которых доступна установка ПО.
        description (str): Описание ПО из маркетплейса.
        requirements (SoftwareRequirements): Требования к облачному серверу для установки ПО.
    '''
    id: int
    name: str
    os_ids: list[int]
    description: str
    requirements: SoftwareRequirements


class ServersSoftwareResponse(ResponseWithMeta):
    '''Ответ со списком ПО из маркетплейса.

    Attributes:
        servers_software (list[ServersSoftware]): Список ПО
    '''
    servers_software: list[ServersSoftware]
