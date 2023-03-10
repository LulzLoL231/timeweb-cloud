# -*- coding: utf-8 -*-
'''Модели для работы со статистикой облачного сервера'''
from datetime import datetime

from ...base import BaseData, BaseResponse


class BaseStats(BaseData):
    '''Базовая модель статистики облачного сервера.

    Attributes:
        logged_at (datetime): Дата события в формате ISO 8061
    '''
    logged_at: datetime


class CPUStats(BaseStats):
    '''Статистика ЦП облачного сервера.

    Attributes:
        load (float): Нагрузка нагрузка на процессор. Возвращает значение от 0 до 1, где 1 это 100%
    '''
    load: float


class TrafficStats(BaseStats):
    '''Статистика интернет трафика облачного сервера

    Attributes:
        incoming (float): Входящий трафик сети в Мб/с
        outgoing (float): Исходящий трафик сети в Мб/с
    '''
    incoming: float
    outgoung: float


class DiskStats(BaseStats):
    '''Статистика основного диска.

    Attributes:
        write (float): Нагрузка на запись диска в Мб/с
        read (float): Нагрузка на чтение диска в Мб/с
    '''
    write: float
    read: float


class RAMStats(BaseStats):
    '''Статистика ОЗУ облачного сервера.

    Attributes:
        total (int): Общее количество оперативной памяти в Мб
        used (int): Количество потревляемой оперативной памяти в Мб
        used_cached (int): Количество закешированной оперативной памяти в Мб
        available (int): Количество доступной оперативной памяти в Мб
    '''
    total: int
    used: int
    used_cached: int
    available: int


class StatsResponse(BaseResponse):
    '''Ответ со статистикой облачного сервера.

    Attributes:
        cpu (CPUStats): Статистика ЦП облачного сервера.
        network_traffic (TrafficStats): Статистика интернет трафика облачного сервера
        disk (DiskStats): Статистика основного диска.
        ram (RAMStats): Статистика ОЗУ облачного сервера.
    '''
    cpu: CPUStats
    network_traffic: TrafficStats
    disk: DiskStats
    ram: RAMStats
