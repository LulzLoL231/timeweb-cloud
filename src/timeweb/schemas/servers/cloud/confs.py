# -*- coding: utf-8 -*-
'''Модели для работы с конфигураторами облачных серверов'''
from ...base import ResponseWithMeta, BaseData


class ConfiguratorRequirements(BaseData):
    '''Требования для конфигуратора сервера.

    Attributes:
        cpu_min (int): Минимальное количество ядер процессора.
        cpu_step (int): Размер шага ядер процессора.
        cpu_max (int): Максимальное количество ядер процессора.
        ram_min (int): Минимальное количество оперативной памяти (в Мб).
        ram_step (int): Размер шага оперативной памяти.
        ram_max (int): Максимальное количество оперативной памяти (в Мб).
        disk_min (int): Минимальный размер диска (в Мб).
        disk_step (int): Размер шага диска
        disk_max (int): Максимальный размер диска (в Мб).
        network_bandwidth_min (int): Минимальныая пропускная способноть интернет-канала (в Мб)
        network_bandwidth_step (int): Размер шага пропускной способноти интернет-канала (в Мб)Максимальная пропускная способноть интернет-канала (в Мб)
        network_bandwidth_max (int): Максимальная пропускная способноть интернет-канала (в Мб)
    '''
    cpu_min: int
    cpu_step: int
    cpu_max: int
    ram_min: int
    ram_step: int
    ram_max: int
    disk_min: int
    disk_step: int
    disk_max: int
    network_bandwidth_min: int
    network_bandwidth_step: int
    network_bandwidth_max: int


class ServerConfigurator(BaseData):
    '''Конфигуратор сервера.

    Attributes:
        id (int): Уникальный идентификатор конфигуратора сервера.
        location (str): Локация сервера.
        disk_type (str): Тип диска.
        is_allowed_local_network (bool): Есть возможность подключения локальной сети
        cpu_frequency (str): Частота процессора.
        requirements (ConfiguratorRequirements): Требования для конфигуратора сервера.
    '''
    id: int
    location: str
    disk_type: str
    is_allowed_local_network: bool
    cpu_frequency: str
    requirements: ConfiguratorRequirements


class ServerConfiguratorsResponse(ResponseWithMeta):
    '''Ответ со списком конфигураторов сервера.

    Attributes:
        server_configurators (list[ServerConfigurator]): Список конфигураторов.'''
    server_configurators: list[ServerConfigurator]
