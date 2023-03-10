# -*- coding: utf-8 -*-
'''Модели для работы с IP-адресами облачного сервера'''
from enum import Enum
from ipaddress import IPv4Address, IPv6Address

from ...base import ResponseWithMeta, BaseData, BaseResponse


IPAddress = IPv4Address | IPv6Address


class IPType(str, Enum):
    '''Тип IP-адреса.

    Attributes:
        IPv4 (str): IP-адрес версии 4
        IPv6 (str): IP-адрес версии 6
    '''
    IPv4 = 'ipv4'
    IPv6 = 'ipv6'


class ServerIP(BaseData):
    '''IP-адрес облачного сервера.

    Attributes:
        type (IPType): Тип IP-адреса сети
        ip (IPAddress): IP-адрес сети
        ptr (str): Запись имени узла
        is_main (bool): Является ли сеть основной.
    '''
    type: IPType
    ip: IPAddress
    ptr: str
    is_main: bool


class ServerIPsResponse(ResponseWithMeta):
    '''Ответ со списком IP-адресов облачного сервера.

    Attributes:
        server_ips (list[ServerIP]): Список IP-адресов.
    '''
    server_ips: list[ServerIP]


class ServerIPResponse(BaseResponse):
    '''Ответ с IP-адресом облачного сервера.

    Attributes:
        server_ip (ServerIP): IP-адрес сервера.
    '''
    server_ip: ServerIP
