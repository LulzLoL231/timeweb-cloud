# -*- coding: utf-8 -*-
'''Модели для работы с NS доменов.'''
from ipaddress import IPv4Address, IPv6Address

from ..base import ResponseWithMeta, BaseData


IPAddress = IPv4Address | IPv6Address


class NameServerItems(BaseData):
    '''Список Name-серверов'''
    host: str
    ips: list[IPAddress]


class NameServer(BaseData):
    '''Модель данных Name-сервера'''
    is_delegation_allowed: bool
    items: list[NameServerItems]
    task_status: str


class NameServersResponse(ResponseWithMeta):
    '''Ответ со списком name-серверов'''
    name_servers: list[NameServer]
