# -*- coding: utf-8 -*-
'''Модели для работы с NS доменов.'''
from ipaddress import IPv4Address, IPv6Address

from ..base import ResponseWithMeta, BaseData


IPAddress = IPv4Address | IPv6Address


class NameServerItems(BaseData):
    '''Список Name-серверов.

    Attributes:
        host (str): Хост name-сервера.
        ips (list[IPAddress]): Список IP-адресов name-сервера
    '''
    host: str
    ips: list[IPAddress]


class NameServer(BaseData):
    '''Модель данных Name-сервера.

    Attributes:
        is_delegation_allowed (bool): Это логическое значение, которое показывает включена ли услуга разрешено ли делегирование домена.
        items (list[NameServerItems]): Список name-серверов
        task_status (str): Статус добавления name-сервера.
    '''
    is_delegation_allowed: bool
    items: list[NameServerItems]
    task_status: str


class NameServersResponse(ResponseWithMeta):
    '''Ответ со списком name-серверов.

    Attributes:
        name_servers (list[NameServer]): Список name-серверов
    '''
    name_servers: list[NameServer]
