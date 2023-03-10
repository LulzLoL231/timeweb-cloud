# -*- coding: utf-8 -*-
'''Модели для работы с ОС облачных серверов'''
from ...base import ResponseWithMeta, BaseData


class OSRequirements(BaseData):
    '''Требования для устнановки ОС.

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


class ServerOS(BaseData):
    '''ОС для облачного сервера.

    Attributes:
        id (int): Уникальный идентификатор операционной системы.
        family (str): Семейство операционной системы.
        name (str): Название операционной системы.
        version (str): Версия операционной системы.
        version_codename (str): Кодовое имя версии операционной системы.
        description (str): Описание операционной системы.
        requirements (OSRequirements): Требования к облачному серверу для установки операционной системы.
    '''
    id: int
    family: str
    name: str
    version: str
    version_codename: str
    description: str
    requirements: OSRequirements


class ServersOSResponse(ResponseWithMeta):
    '''Ответ со списком ОС доступных для установки на облачных серверах.

    Attributes:
        servers_os (list[ServerOS]): Список ОС.
    '''
    servers_os: list[ServerOS]
